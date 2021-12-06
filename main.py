import pandas as pd
import xml.etree.ElementTree as ET
from collections import OrderedDict


def signal_light_checker(value, line):
    assert value in ["K", "ZH", "Z", "ZHM", "ZM", "DZH", "DZHM"], \
        "Not supported light value {} in line {}".format(value, line)


class Route:
    def __init__(self, line_in_excel):
        self._line_in_excel = line_in_excel
        self.route_tag = None
        self._route_type = None
        self._signal_tag = None
        self._signal_type = None
        self._route_pointer_value = None
        self._trace_begin = None
        self._trace_points = ""
        self._trace_variants = None
        self._trace_end = None
        self._end_selectors = None
        self._route_points_before_route = None
        self._next_dark = "K"
        self._next_stop = "K"
        self._next_on_main = "K"
        self._next_on_main_green = "K"
        self._next_on_side = "K"
        self._next_also_on_main = "K"
        self._next_also_on_main_green = "K"
        self._next_also_on_side = "K"

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
        # check signal in list of available values
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
        assert int(value) > 0, "Route pointer value should be int > 0, given value is {} in line {}"\
            .format(value, self.line_in_excel)
        self._route_pointer_value = value


routes = []

# xlsx to universal dict

dataframe = pd.read_excel('TrainRoute.xlsx')
print(dataframe)


# universal dict to xml
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

