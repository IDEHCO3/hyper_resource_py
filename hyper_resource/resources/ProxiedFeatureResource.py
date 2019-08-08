import inspect

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
        attrs_funcs_arr = self.remove_last_slash(attributes_functions_str).split("/")[1:]
        result = self._execute_attribute_or_method(object, attrs_funcs_arr[0], attrs_funcs_arr[1:])

        #todo: will be usefull for determinate requiredObject content=type
        #self.name_of_last_operation_executed

        contype_accept = self.content_type_by_accept(request)
        #self.content_type_by_operation(self.name_of_last_operation_executed)
        #self.content_type_for_operation()

        if self.is_image_content_type(request):
            return self.required_object_for_image(result, request)

        if not isinstance(result, GEOSGeometry):
            result = {self.name_of_last_operation_executed: result}

        return RequiredObject(result, self.content_type_by_accept(request),self.object_model, 200)