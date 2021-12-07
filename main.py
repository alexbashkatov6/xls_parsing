import pandas as pd
from pandas.core.frame import DataFrame
import xml.etree.ElementTree as ET
from collections import OrderedDict
import re

DEBUG_MODE = False


class Route:
    def __init__(self, line_in_excel):
        self._line_in_excel = line_in_excel
        self.route_tag = None
        self._route_type = None
        self._signal_tag = None
        self._signal_type = None
        self._route_pointer_value = None
        self._trace_begin = None
        self.trace_points = ""
        self._trace_variants = None
        self._trace_end = None
        self._end_selectors = None
        self._route_points_before_route = None
        self.next_dark = "K"
        self.next_stop = "K"
        self.next_on_main = "K"
        self.next_on_main_green = "K"
        self.next_on_side = "K"
        self.next_also_on_main = "K"
        self.next_also_on_main_green = "K"
        self.next_also_on_side = "K"

    def signal_light_checker(self, value, column_name):
        if self.route_type == "PpoShuntingRoute":
            return
        assert value in ["K", "ZH", "Z", "ZHM", "ZM", "DZH", "DZHM"], \
            "Not supported light value {} in line {} column {}".format(value, self.line_in_excel, column_name)

    @property
    def line_in_excel(self):
        return self._line_in_excel

    @property
    def route_type(self):
        return self._route_type

    @route_type.setter
    def route_type(self, value):
        assert value in ["PpoTrainRoute", "PpoShuntingRoute"], "Not valid route type {} in line {}"\
            .format(value, self.line_in_excel)
        self._route_type = value

    @property
    def signal_tag(self):
        return self._signal_tag

    @signal_tag.setter
    def signal_tag(self, value):
        # ! implement here check signal in list of available values
        self._signal_tag = value

    @property
    def signal_type(self):
        return self._signal_type

    @signal_type.setter
    def signal_type(self, value):
        assert value in ["PpoTrainSignal", "PpoShuntingSignal"], "Not valid signal type {} in line {}"\
            .format(value, self.line_in_excel)
        self._signal_type = value

    @property
    def route_pointer_value(self):
        return self._route_pointer_value

    @route_pointer_value.setter
    def route_pointer_value(self, value):
        if value == "":
            self._route_pointer_value = None
            return
        assert int(value) > 0, "Route pointer value should be int > 0, given value is {} in line {}"\
            .format(value, self.line_in_excel)
        self._route_pointer_value = value

    @property
    def trace_begin(self):
        return self._trace_begin

    @trace_begin.setter
    def trace_begin(self, value):
        # ! implement here check trace_begin in list of available values
        self._trace_begin = value

    @property
    def trace_variants(self):
        return self._trace_variants

    @trace_variants.setter
    def trace_variants(self, value):
        if value == "":
            self._trace_variants = None
            return
        # ! implement here check trace_variants in list of available values
        self._trace_variants = value

    @property
    def trace_points(self):
        return self._trace_points

    @trace_points.setter
    def trace_points(self, value: str):
        points_found = re.findall(r"[+-]\d{1,3}S?[OB]?", value)
        val_copy = value
        for point in points_found:
            val_copy = val_copy.replace(point, "", 1)
        assert (not val_copy) or val_copy.isspace(), \
            "Pointers list {} is not valid in line {}".format(value, self.line_in_excel)
        # ! implement here check points in list of available values
        self._trace_points = value

    @property
    def trace_end(self):
        return self._trace_end

    @trace_end.setter
    def trace_end(self, value):
        # ! implement here check trace_end in list of available values
        self._trace_end = value

    @property
    def end_selectors(self):
        return self._end_selectors

    @end_selectors.setter
    def end_selectors(self, value):
        # ! implement here check end_selectors in list of available values
        self._end_selectors = value

    @property
    def route_points_before_route(self):
        return self._route_points_before_route

    @route_points_before_route.setter
    def route_points_before_route(self, value):
        if value == "":
            self._route_points_before_route = None
            return
        # ! implement here check route_points_before_route in list of available values
        self._route_points_before_route = value

    @property
    def next_dark(self):
        return self._next_dark

    @next_dark.setter
    def next_dark(self, value):
        self.signal_light_checker(value, "next_dark")
        self._next_dark = value

    @property
    def next_stop(self):
        return self._next_stop

    @next_stop.setter
    def next_stop(self, value):
        self.signal_light_checker(value, "next_stop")
        self._next_stop = value

    @property
    def next_on_main(self):
        return self._next_on_main

    @next_on_main.setter
    def next_on_main(self, value):
        self.signal_light_checker(value, "next_on_main")
        self._next_on_main = value

    @property
    def next_on_main_green(self):
        return self._next_on_main_green

    @next_on_main_green.setter
    def next_on_main_green(self, value):
        self.signal_light_checker(value, "next_on_main_green")
        self._next_on_main_green = value

    @property
    def next_on_side(self):
        return self._next_on_side

    @next_on_side.setter
    def next_on_side(self, value):
        self.signal_light_checker(value, "next_on_side")
        self._next_on_side = value

    @property
    def next_also_on_main(self):
        return self._next_also_on_main

    @next_also_on_main.setter
    def next_also_on_main(self, value):
        self.signal_light_checker(value, "next_also_on_main")
        self._next_also_on_main = value

    @property
    def next_also_on_main_green(self):
        return self._next_also_on_main_green

    @next_also_on_main_green.setter
    def next_also_on_main_green(self, value):
        self.signal_light_checker(value, "next_also_on_main_green")
        self._next_also_on_main_green = value

    @property
    def next_also_on_side(self):
        return self._next_also_on_side

    @next_also_on_side.setter
    def next_also_on_side(self, value):
        self.signal_light_checker(value, "next_also_on_side")
        self._next_also_on_side = value


routes = []

# 1. File xlsx to list of routes

if DEBUG_MODE:
    print(bool("0"))
    print(re.findall(r"[+-]\d{1,3}S?[OB]?", "-309 -1SB +1 +3 +5 +305 +303"))
else:
    dataframe: DataFrame = pd.read_excel('TrainRoute.xlsx')
    dataframe = dataframe.fillna("")
    for row in dataframe.iterrows():
        row_index = int(row[0])
        route = Route(row_index + 2)
        for column in dataframe.columns:
            assert hasattr(route, column), "Not hasattr {} {}".format(route, column)
            setattr(route, column, dataframe.at[row_index, column])
        routes.append(route)

for route in routes:
    print("route", route.route_tag)

# 2. List of routes to xml


# tree = ET.parse('test.xml')
# root = tree.getroot()
# print(root.tag, root.attrib)
# for child in root:
#     print(child.tag, child.attrib)
# print(root[0][1].text)
# for neighbor in root.iter('neighbor'):
#     print(neighbor.attrib)
# for country in root.findall('country'):
#     rank = country.find('rank').text
#     name = country.get('name')
#     print(name, rank)
# for rank in root.iter('rank'):
#     new_rank = int(rank.text) + 2
#     rank.text = str(new_rank)
#     rank.set('updated', 'yes')
#
# tree.write('output.xml')
#
# a = ET.Element('a')
# b = ET.SubElement(a, 'b')
# c = ET.SubElement(a, 'c')
# d = ET.SubElement(c, 'd')
# ET.dump(a)

# if DEBUG_MODE:


