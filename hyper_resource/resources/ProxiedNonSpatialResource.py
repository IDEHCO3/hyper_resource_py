import inspect

from hyper_resource.models import ProxiedNonSpatialResourceOperationController, ProxiedNonSpatialModel
from hyper_resource.resources.NonSpatialResource import NonSpatialResource


class ProxiedNonSpatialResource(NonSpatialResource):

    def __init__(self):  # , spatial_obj):
        super(ProxiedNonSpatialResource, self).__init__()
        self.operation_controller = ProxiedNonSpatialResourceOperationController()
        #self.object_model = ProxiedNonSpatialModel()

    def set_object_model(self, object):
        self.object_model = object

    def required_object_for_proxied_get(self, object, request, attributes_functions_str):
        attrs_funcs_arr = self.remove_last_slash(attributes_functions_str).split("/")[1:]
        result = self._execute_attribute_or_method(object, attrs_funcs_arr[0], attrs_funcs_arr[1:])

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
