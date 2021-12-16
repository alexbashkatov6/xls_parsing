import pandas as pd
from pandas.core.frame import DataFrame
import xml.etree.ElementTree as ElTr
import xml.dom.minidom
from collections import OrderedDict
import re


class Route:
    def __init__(self, line_in_excel):
        self._line_in_excel = line_in_excel
        self.id = str(line_in_excel-1)
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
        # self._crossroad_1_id = None
        # self._crossroad_1_delay_open = None
        # self._crossroad_1_start_notif = None
        # self._crossroad_1_delay_start_notif = None
        # self._crossroad_2_id = None
        # self._crossroad_2_delay_open = None
        # self._crossroad_2_start_notif = None
        # self._crossroad_2_delay_start_notif = None
        # self._crossroad_3_id = None
        # self._crossroad_3_delay_open = None
        # self._crossroad_3_start_notif = None
        # self._crossroad_3_delay_start_notif = None

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
        if value:
            value += " "
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
        self._route_points_before_route = value+" "

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

dataframe: DataFrame = pd.read_excel('TrainRoute.xlsx', dtype='string')
dataframe = dataframe.fillna("")
for row in dataframe.iterrows():
    row: tuple
    row_index = int(row[0])
    route = Route(row_index + 2)
    for column in dataframe.columns:
        assert hasattr(route, column), "Not hasattr {} {}".format(route, column)
        setattr(route, column, dataframe.at[row_index, column])
    routes.append(route)


# 2. List of routes to xml

def form_route_element(signal_element_, route_) -> ElTr.Element:
    if route_.route_type == "PpoTrainRoute":
        route_element = ElTr.SubElement(signal_element_, 'TrRoute')
    else:
        route_element = ElTr.SubElement(signal_element_, 'ShRoute')
    route_element.set("Tag", route_.route_tag)
    route_element.set("Type", route_.route_type)
    route_element.set("Id", route_.id)
    if route_.route_pointer_value:
        route_element.set("ValueRoutePointer", route_.route_pointer_value)
    trace_element = ElTr.SubElement(route_element, 'Trace')
    trace_element.set("Start", route_.trace_begin)
    trace_element.set("OnCoursePoints", route_.trace_points)
    trace_element.set("Finish", route_.trace_end)
    if route_.trace_variants:
        trace_element.set("Variants", route_.trace_variants)
    selectors_element = ElTr.SubElement(route_element, 'OperatorSelectors')
    selectors_element.set("Ends", route_.end_selectors)
    if route_.route_type == "PpoTrainRoute":
        dependence_element = ElTr.SubElement(route_element, 'SignalingDependence')
        dependence_element.set("Dark", route_.next_dark)
        dependence_element.set("Stop", route_.next_stop)
        dependence_element.set("OnMain", route_.next_on_main)
        dependence_element.set("OnMainGreen", route_.next_on_main_green)
        dependence_element.set("OnSide", route_.next_on_side)
        dependence_element.set("OnMainALSO", route_.next_also_on_main)
        dependence_element.set("OnMainGrALSO", route_.next_also_on_main_green)
        dependence_element.set("OnSideALSO", route_.next_also_on_side)
        if route_.route_points_before_route:
            before_route_element = ElTr.SubElement(route_element, 'PointsAnDTrack')
            before_route_element.set("Points", route_.route_points_before_route)
    return route_element


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

train_route_element = ElTr.Element('Routes')
shunt_route_element = ElTr.Element('Routes')
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


xmlstr_train = xml.dom.minidom.parseString(ElTr.tostring(train_route_element)).toprettyxml()
with open('TrainRoute.xml', 'w', encoding='utf-8') as out:
    out.write(xmlstr_train)
xmlstr_shunt = xml.dom.minidom.parseString(ElTr.tostring(shunt_route_element)).toprettyxml()
with open('ShuntingRoute.xml', 'w', encoding='utf-8') as out:
    out.write(xmlstr_shunt)
