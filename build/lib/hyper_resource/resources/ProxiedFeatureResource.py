import inspect
import json

from hyper_resource.models import ProxiedSpatialOperationController, ProxiedFeatureModel
from hyper_resource.resources.AbstractResource import RequiredObject
from hyper_resource.resources.FeatureResource import FeatureResource
from hyper_resource.utils import *
from django.contrib.gis.geos import GEOSGeometry


class ProxiedFeatureResource(FeatureResource):

    def __init__(self):#, spatial_obj):
        super(ProxiedFeatureResource, self).__init__()
        self.operation_controller = ProxiedSpatialOperationController()
        #self.object_model = ProxiedFeatureModel()

    def set_object_model(self, object):
        self.object_model = object

    def set_serializer_class(self, serializer_class):
        self.serializer_class = serializer_class

    def array_of_operation_name(self):
        return list(self.operation_controller.geometry_operations_dict().keys())

    def get_operation_type_called(self, attributes_functions_str):
        operation_name = self.get_operation_name_from_path(attributes_functions_str)
        return self.operation_controller.geometry_operations_dict()[operation_name]

    def content_type_for_operation(self, request, attributes_functions_str):
        attributes_functions_str = self.remove_last_slash(attributes_functions_str)
        contype_accept = self.content_type_by_accept(request)

        if self.path_has_url(attributes_functions_str):
            attrs_fucs_arr = self.attribute_functions_str_with_url_splitted_by_slash(attributes_functions_str)
        else:
            attrs_fucs_arr = self.remove_last_slash(attributes_functions_str).split("/")

        # todo: use self.object_model or a simple object (with CharFields setted to "" and IntegerFields setted to 1)
        result = self.get_operation_return_type(self.object_model, attrs_fucs_arr[0], attrs_fucs_arr[1:])

        result_type = result if inspect.isclass(result) else type(result)
        if contype_accept in self.available_content_types_for(result_type):
            return contype_accept
        return self.default_content_type_for(result_type)

    def required_object_for_proxied_get(self, object, request, attributes_functions_str):
        attrs_funcs_arr = self.remove_last_slash(attributes_functions_str).split("/")
        result = self._execute_attribute_or_method(object, attrs_funcs_arr[0], attrs_funcs_arr[1:])

        if self.is_image_content_type(request):
            return self.required_object_for_image(result, request)

        if not isinstance(result, GEOSGeometry):
            result = {self.name_of_last_operation_executed: result}

        return RequiredObject(json.loads(result.geojson), self.content_type_for_operation(request, attributes_functions_str), self.object_model, 200)

    def _execute_attribute_or_method(self, object, attribute_or_method_name, array_of_attribute_or_method_name):
        parameters = []

        if attribute_or_method_name in self.operation_controller.geometry_operations_dict():
            if self.operation_controller.operation_has_parameters(object, attribute_or_method_name):
                parameters = array_of_attribute_or_method_name[0].split(PARAM_SEPARATOR) if len(array_of_attribute_or_method_name) > 0 else []
                array_of_attribute_or_method_name = array_of_attribute_or_method_name[1:]

        obj = self._value_from_object(object, attribute_or_method_name, parameters)

        if len(array_of_attribute_or_method_name) == 0:
            return obj

        return self._execute_attribute_or_method(obj, array_of_attribute_or_method_name[0], array_of_attribute_or_method_name[1:])

    def get_operation_return_type(self, object, attribute_or_method_name, array_of_attribute_or_method_name):
        parameters = []

        if attribute_or_method_name in self.operation_controller.geometry_operations_dict():
            if self.operation_controller.operation_has_parameters(object, attribute_or_method_name):
                parameters = array_of_attribute_or_method_name[0].split(PARAM_SEPARATOR) if len(
                    array_of_attribute_or_method_name) > 0 else []
                array_of_attribute_or_method_name = array_of_attribute_or_method_name[1:]

        result = self.return_type_for_operation(object, attribute_or_method_name, parameters)

        if len(array_of_attribute_or_method_name) == 0:
            return result

        if inspect.isclass(result):
            obj = self.default_value_for_field(result)
        else:
            obj = result
        return self.get_operation_return_type(obj, array_of_attribute_or_method_name[0], array_of_attribute_or_method_name[1:])

    def return_type_for_operation(self, object, attribute_or_function_name, parameters):
        attribute_or_function_name_striped = self.remove_last_slash(attribute_or_function_name)
        self.name_of_last_operation_executed = attribute_or_function_name_striped

        if attribute_or_function_name_striped in self.operation_controller.geometry_operations_dict():
            return self.get_operation_type_called(attribute_or_function_name_striped).return_type

        return type(self.field_for(attribute_or_function_name))