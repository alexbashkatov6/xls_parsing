import pandas as pd
from pandas.core.frame import DataFrame
import xml.etree.ElementTree as ElTr
import xml.dom.minidom
from collections import OrderedDict
import re

DEBUG_MODE = False


class Route:
    def __init__(self, line_in_excel):
        self._line_in_excel = line_in_excel
        self.id = line_in_excel-1
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
    dataframe: DataFrame = pd.read_excel('TrainRoute.xlsx', dtype='string')
    dataframe = dataframe.fillna("")
    for row in dataframe.iterrows():
        row_index = int(row[0])
        route = Route(row_index + 2)
        for column in dataframe.columns:
            assert hasattr(route, column), "Not hasattr {} {}".format(route, column)
            setattr(route, column, dataframe.at[row_index, column])
        routes.append(route)

for route in routes:
    if not (route.route_points_before_route is None):
        print("route", route.route_points_before_route)

# 2. List of routes to xml


def form_route_element(signal_element, route) -> ElTr.Element:
    if route.route_type == "PpoTrainRoute":
        route_element = ElTr.SubElement(signal_element, 'TrRoute')
    else:
        route_element = ElTr.SubElement(signal_element, 'ShRoute')
    route_element.set("Tag", route.route_tag)
    route_element.set("Type", route.route_type)
    if route.route_pointer_value:
        route_element.set("ValueRoutePointer", route.route_pointer_value)
    trace_element = ElTr.SubElement(route_element, 'Trace')
    trace_element.set("Start", route.trace_begin)
    trace_element.set("OnCoursePoints", route.trace_points)
    trace_element.set("Finish", route.trace_end)
    if route.route_type == "PpoTrainRoute" and route.trace_variants:
        trace_element.set("Variants", route.trace_variants)
    selectors_element = ElTr.SubElement(route_element, 'OperatorSelectors')
    selectors_element.set("Ends", route.end_selectors)
    if route.route_type == "PpoTrainRoute":
        dependence_element = ElTr.SubElement(route_element, 'SignalingDependence')
        dependence_element.set("Dark", route.next_dark)
        dependence_element.set("Stop", route.next_stop)
        dependence_element.set("OnMain", route.next_on_main)
        dependence_element.set("OnMainGreen", route.next_on_main_green)
        dependence_element.set("OnSide", route.next_on_side)
        dependence_element.set("OnMainALSO", route.next_also_on_main)
        dependence_element.set("OnMainGrALSO", route.next_also_on_main_green)
        dependence_element.set("OnSideALSO", route.next_also_on_side)
        if route.route_points_before_route:
            before_route_element = ElTr.SubElement(route_element, 'PointsAnDTrack')
            before_route_element.set("Points", route.route_points_before_route)
    return route_element


if DEBUG_MODE:
    a = ElTr.Element('a')
    b = ElTr.SubElement(a, 'b')
    c = ElTr.SubElement(a, 'c')
    d = ElTr.SubElement(c, 'd')
    xmlstr = xml.dom.minidom.parseString(ElTr.tostring(a)).toprettyxml()
    with open('output.xml', 'w', encoding='utf-8') as out:
        out.write(xmlstr)
else:
    train_routes_dict = OrderedDict()
    shunt_trs_routes_dict = OrderedDict()
    shunt_shs_routes_dict = OrderedDict()
    for route in routes:
        st = route.signal_tag
        if route.route_type == "PpoTrainRoute":
            if st not in train_routes_dict:
                train_routes_dict[st] = []
            train_routes_dict[st].append(route)
        elif route.signal_type == "PpoTrainSignal":
            if st not in shunt_trs_routes_dict:
                shunt_trs_routes_dict[st] = []
            shunt_trs_routes_dict[st].append(route)
        else:
            if st not in shunt_shs_routes_dict:
                shunt_shs_routes_dict[st] = []
            shunt_shs_routes_dict[st].append(route)

    # print(len(unique_signals_list), unique_signals_list)
    # print(len(train_signals_list), train_signals_list)
    # print(len(shunting_signals_list), shunting_signals_list)
    train_route_element = ElTr.Element('Routes')
    shunt_route_element = ElTr.Element('Routes')
    # print("len train signal", len(train_routes_dict))
    # print("len shunt train signal", len(shunt_trs_routes_dict))
    for train_signal in train_routes_dict:
        signal_element = ElTr.SubElement(train_route_element, 'TrainSignal')
        signal_element.set("Tag", train_signal)
        signal_element.set("Type", "PpoTrainSignal")
        for route in train_routes_dict[train_signal]:
            form_route_element(signal_element, route)
        if train_signal in shunt_trs_routes_dict:
            for route in shunt_trs_routes_dict[train_signal]:
                form_route_element(signal_element, route)
    for shunt_signal in shunt_shs_routes_dict:
        signal_element = ElTr.SubElement(shunt_route_element, 'ShuntingSignal')
        signal_element.set("Tag", shunt_signal)
        signal_element.set("Type", "PpoShuntingSignal")
        for route in shunt_shs_routes_dict[shunt_signal]:
            form_route_element(signal_element, route)

    # for shunt_train_signal in shunt_trs_routes_dict:
    #     print("shunt_train_signal", shunt_train_signal)

    xmlstr_train = xml.dom.minidom.parseString(ElTr.tostring(train_route_element)).toprettyxml()
    with open('train_routes.xml', 'w', encoding='utf-8') as out:
        out.write(xmlstr_train)
    xmlstr_shunt = xml.dom.minidom.parseString(ElTr.tostring(shunt_route_element)).toprettyxml()
    with open('shunt_routes.xml', 'w', encoding='utf-8') as out:
        out.write(xmlstr_shunt)

