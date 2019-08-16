from hyper_resource.resources.AbstractResource import *
from hyper_resource.resources.SpatialResource import SpatialResource
IMAGE_RESOURCE_TYPE = "Image"
FEATURE_RESOURCE_TYPE = FeatureModel
GEOBUF = 'Geobuf'


class FeatureResource(SpatialResource):
    def __init__(self):
        super(FeatureResource, self).__init__()

    def default_resource_type(self):
        return FEATURE_RESOURCE_TYPE

    def dict_by_accept_resource_type(self):
        dict = {
            CONTENT_TYPE_OCTET_STREAM: GEOBUF,
            CONTENT_TYPE_IMAGE_PNG: IMAGE_RESOURCE_TYPE
        }

        return dict

    def get_content_types_for_resource(self):
        return [
            CONTENT_TYPE_JSON,
            CONTENT_TYPE_OCTET_STREAM,
            CONTENT_TYPE_IMAGE_PNG,
            CONTENT_TYPE_GEOJSON
        ]

    # Must be overridden
    def initialize_context(self):
        pass

    def geometry_field_name(self):
        return self.serializer_class.Meta.geo_field

    def is_spatial_attribute(self, attribute_name):
        return self.model.geo_field_name() == attribute_name.lower()

    def operations_with_parameters_type(self):
        return self.object_model.operations_with_parameters_type()

    def get_object_from_operation_attributes_functions_str_with_url(self, attributes_functions_str, request=None):
        # r':/+' matches string like: ':' followed by at least 1 occurence of '/'
        # substitute any occurences of ':/' to '://' in 'attributes_functions_str'
        attributes_functions_str = re.sub(r':/+', '://', attributes_functions_str)
        arr_of_two_url_and_param = self.attributes_functions_splitted_by_url(attributes_functions_str)
        resp = requests.get(arr_of_two_url_and_param[1])
        if resp.status_code in[400, 401, 404]:
            return RequiredObject({},CONTENT_TYPE_JSON, self.object_model,  resp.status_code)
        if resp.status_code == 500:
            return RequiredObject({},CONTENT_TYPE_JSON, self.object_model,resp.status_code)
        j = resp.text

        if arr_of_two_url_and_param[2] is not None:
            attributes_functions_str = arr_of_two_url_and_param[0] + j + PARAM_SEPARATOR + arr_of_two_url_and_param[2]
        else:
            attributes_functions_str = arr_of_two_url_and_param[0] + j
        #external_etag = resp.headers['etag']
        #self.inject_e_tag(external_etag)
        return self.get_object_from_operation(attributes_functions_str)

    def get_object_from_operation(self, attributes_functions_str):
        att_funcs = attributes_functions_str.split('/')
        a_value = self._execute_attribute_or_method(self.object_model, att_funcs[0], att_funcs[1:])
        if a_value is None:
            return None
        if isinstance(a_value, GEOSGeometry):
            a_value = json.loads(a_value.geojson)
        elif isinstance(a_value, SpatialReference) or isinstance(a_value, OGRGeometry):
            a_value = { self.name_of_last_operation_executed: a_value.wkt.strip('\n')}
        elif isinstance(a_value, memoryview) or isinstance(a_value, buffer):
            a_value = a_value.hex()
        elif isinstance(a_value, bytes):
            a_value = a_value.decode()
        else:
            try:
                a_value = {self.name_of_last_operation_executed: str(json.loads(a_value))}
            except (json.decoder.JSONDecodeError, TypeError):
                a_value = {self.name_of_last_operation_executed: a_value}
        return a_value

    def get_object_from_transform_spatial_operation(self, attributes_functions_str):
        pass

    def operation_name_method_dic(self):
        dict = super(FeatureResource, self).operation_name_method_dic()
        dict.update({
            self.operation_controller.area_operation_name:              self.required_object_for_spatial_operation,
            self.operation_controller.boundary_operation_name:          self.required_object_for_spatial_operation,
            self.operation_controller.buffer_operation_name:            self.required_object_for_spatial_operation,
            self.operation_controller.centroid_operation_name:          self.required_object_for_spatial_operation,
            self.operation_controller.contains_operation_name:          self.required_object_for_spatial_operation,
            self.operation_controller.convex_hull_operation_name:       self.required_object_for_spatial_operation,
            self.operation_controller.coord_seq_operation_name:         self.required_object_for_spatial_operation,
            self.operation_controller.coords_operation_name:            self.required_object_for_spatial_operation,
            self.operation_controller.count_operation_name:             self.required_object_for_spatial_operation,
            self.operation_controller.crosses_operation_name:           self.required_object_for_spatial_operation,
            self.operation_controller.crs_operation_name:               self.required_object_for_spatial_operation,
            self.operation_controller.difference_operation_name:        self.required_object_for_spatial_operation,
            self.operation_controller.dims_operation_name:              self.required_object_for_spatial_operation,
            self.operation_controller.disjoint_operation_name:          self.required_object_for_spatial_operation,
            self.operation_controller.distance_operation_name:          self.required_object_for_spatial_operation,
            self.operation_controller.empty_operation_name:             self.required_object_for_spatial_operation,
            self.operation_controller.envelope_operation_name:          self.required_object_for_spatial_operation,
            self.operation_controller.equals_operation_name:            self.required_object_for_spatial_operation,
            self.operation_controller.equals_exact_operation_name:      self.required_object_for_spatial_operation,
            self.operation_controller.ewkb_operation_name:              self.required_object_for_spatial_operation,
            self.operation_controller.ewkt_operation_name:              self.required_object_for_spatial_operation,
            self.operation_controller.extent_operation_name:            self.required_object_for_spatial_operation,
            self.operation_controller.geojson_operation_name:           self.required_object_for_spatial_operation,
            self.operation_controller.geom_type_operation_name:         self.required_object_for_spatial_operation,
            self.operation_controller.geom_typeid_operation_name:       self.required_object_for_spatial_operation,
            self.operation_controller.get_coords_operation_name:        self.required_object_for_spatial_operation,
            self.operation_controller.get_srid_operation_name:          self.required_object_for_spatial_operation,
            self.operation_controller.get_x_operation_name:             self.required_object_for_spatial_operation,
            self.operation_controller.get_y_operation_name:             self.required_object_for_spatial_operation,
            self.operation_controller.get_z_operation_name:             self.required_object_for_spatial_operation,
            self.operation_controller.has_cs_operation_name:            self.required_object_for_spatial_operation,
            self.operation_controller.hasz_operation_name:              self.required_object_for_spatial_operation,
            self.operation_controller.hex_operation_name:               self.required_object_for_spatial_operation,
            self.operation_controller.hexewkb_operation_name:           self.required_object_for_spatial_operation,
            self.operation_controller.index_operation_name:             self.required_object_for_spatial_operation,
            self.operation_controller.intersection_operation_name:      self.required_object_for_spatial_operation,
            self.operation_controller.intersects_operation_name:        self.required_object_for_spatial_operation,
            self.operation_controller.interpolate_operation_name:       self.required_object_for_spatial_operation,
            self.operation_controller.json_operation_name:              self.required_object_for_spatial_operation,
            self.operation_controller.kml_operation_name:               self.required_object_for_spatial_operation,
            self.operation_controller.length_operation_name:            self.required_object_for_spatial_operation,
            self.operation_controller.normalize_operation_name:         self.required_object_for_spatial_operation,
            self.operation_controller.num_coords_operation_name:        self.required_object_for_spatial_operation,
            self.operation_controller.num_geom_operation_name:          self.required_object_for_spatial_operation,
            self.operation_controller.num_points_operation_name:        self.required_object_for_spatial_operation,
            self.operation_controller.ogr_operation_name:               self.required_object_for_spatial_operation,
            self.operation_controller.overlaps_operation_name:          self.required_object_for_spatial_operation,
            self.operation_controller.point_on_surface_operation_name:  self.required_object_for_spatial_operation,
            self.operation_controller.relate_operation_name:            self.required_object_for_spatial_operation,
            self.operation_controller.relate_pattern_operation_name:    self.required_object_for_spatial_operation,
            self.operation_controller.ring_operation_name:              self.required_object_for_spatial_operation,
            self.operation_controller.simple_operation_name:            self.required_object_for_spatial_operation,
            self.operation_controller.simplify_operation_name:          self.required_object_for_spatial_operation,
            self.operation_controller.srid_operation_name:              self.required_object_for_spatial_operation,
            self.operation_controller.srs_operation_name:               self.required_object_for_spatial_operation,
            self.operation_controller.sym_difference_operation_name:    self.required_object_for_spatial_operation,
            self.operation_controller.touches_operation_name:           self.required_object_for_spatial_operation,
            self.operation_controller.transform_operation_name:         self.required_object_for_spatial_operation,
            self.operation_controller.union_operation_name:             self.required_object_for_spatial_operation,
            self.operation_controller.valid_operation_name:             self.required_object_for_spatial_operation,
            self.operation_controller.valid_reason_operation_name:      self.required_object_for_spatial_operation,
            self.operation_controller.within_operation_name:            self.required_object_for_spatial_operation,
            self.operation_controller.wkb_operation_name:               self.required_object_for_spatial_operation,
            self.operation_controller.wkt_operation_name:               self.required_object_for_spatial_operation,
            self.operation_controller.x_operation_name:                 self.required_object_for_spatial_operation,
            self.operation_controller.y_operation_name:                 self.required_object_for_spatial_operation,
            self.operation_controller.z_operation_name:                 self.required_object_for_spatial_operation,
        })
        return dict

    def operation_name_context_dic(self):
        dict = super(FeatureResource, self).operation_name_context_dic()
        dict.update({
            self.operation_controller.area_operation_name:              self.required_context_for_non_spatial_return_operation,
            self.operation_controller.boundary_operation_name:          self.required_context_for_operation,
            self.operation_controller.buffer_operation_name:            self.required_context_for_operation,
            self.operation_controller.centroid_operation_name:          self.required_context_for_operation,
            self.operation_controller.contains_operation_name:          self.required_context_for_non_spatial_return_operation,
            self.operation_controller.convex_hull_operation_name:       self.required_context_for_operation,
            self.operation_controller.coord_seq_operation_name:         self.required_context_for_non_spatial_return_operation,
            self.operation_controller.coords_operation_name:            self.required_context_for_non_spatial_return_operation,
            self.operation_controller.count_operation_name:             self.required_context_for_non_spatial_return_operation,
            self.operation_controller.crosses_operation_name:           self.required_context_for_non_spatial_return_operation,
            self.operation_controller.crs_operation_name:               self.required_context_for_non_spatial_return_operation,
            self.operation_controller.difference_operation_name:        self.required_context_for_operation,
            self.operation_controller.dims_operation_name:              self.required_context_for_non_spatial_return_operation,
            self.operation_controller.disjoint_operation_name:          self.required_context_for_non_spatial_return_operation,
            self.operation_controller.distance_operation_name:          self.required_context_for_non_spatial_return_operation,
            self.operation_controller.empty_operation_name:             self.required_context_for_non_spatial_return_operation,
            self.operation_controller.envelope_operation_name:          self.required_context_for_operation,
            self.operation_controller.equals_operation_name:            self.required_context_for_non_spatial_return_operation,
            self.operation_controller.equals_exact_operation_name:      self.required_context_for_non_spatial_return_operation,
            self.operation_controller.ewkb_operation_name:              self.required_context_for_operation,
            self.operation_controller.ewkt_operation_name:              self.required_context_for_non_spatial_return_operation,
            self.operation_controller.extent_operation_name:            self.required_context_for_non_spatial_return_operation,
            self.operation_controller.geojson_operation_name:           self.required_context_for_non_spatial_return_operation,
            self.operation_controller.geom_type_operation_name:         self.required_context_for_non_spatial_return_operation,
            self.operation_controller.geom_typeid_operation_name:       self.required_context_for_non_spatial_return_operation,
            self.operation_controller.has_cs_operation_name:            self.required_context_for_non_spatial_return_operation,
            self.operation_controller.hasz_operation_name:              self.required_context_for_non_spatial_return_operation,
            self.operation_controller.hex_operation_name:               self.required_context_for_operation,
            self.operation_controller.hexewkb_operation_name:           self.required_context_for_operation,
            self.operation_controller.intersection_operation_name:      self.required_context_for_operation,
            self.operation_controller.intersects_operation_name:        self.required_context_for_non_spatial_return_operation,
            self.operation_controller.interpolate_operation_name:       self.required_context_for_operation,
            self.operation_controller.json_operation_name:              self.required_context_for_non_spatial_return_operation,
            self.operation_controller.kml_operation_name:               self.required_context_for_non_spatial_return_operation,
            self.operation_controller.length_operation_name:            self.required_context_for_non_spatial_return_operation,
            self.operation_controller.normalize_operation_name:         self.required_context_for_operation,
            self.operation_controller.num_coords_operation_name:        self.required_context_for_non_spatial_return_operation,
            self.operation_controller.num_geom_operation_name:          self.required_context_for_non_spatial_return_operation,
            self.operation_controller.num_points_operation_name:        self.required_context_for_non_spatial_return_operation,
            self.operation_controller.ogr_operation_name:               self.required_context_for_non_spatial_return_operation,
            self.operation_controller.overlaps_operation_name:          self.required_context_for_non_spatial_return_operation,
            self.operation_controller.point_on_surface_operation_name:  self.required_context_for_operation,
            self.operation_controller.relate_operation_name:            self.required_context_for_non_spatial_return_operation,
            self.operation_controller.relate_pattern_operation_name:    self.required_context_for_non_spatial_return_operation,
            self.operation_controller.ring_operation_name:              self.required_context_for_non_spatial_return_operation,
            self.operation_controller.simple_operation_name:            self.required_context_for_non_spatial_return_operation,
            self.operation_controller.simplify_operation_name:          self.required_context_for_operation,
            self.operation_controller.srid_operation_name:              self.required_context_for_non_spatial_return_operation,
            self.operation_controller.srs_operation_name:               self.required_context_for_non_spatial_return_operation,
            self.operation_controller.sym_difference_operation_name:    self.required_context_for_operation,
            self.operation_controller.touches_operation_name:           self.required_context_for_non_spatial_return_operation,
            self.operation_controller.transform_operation_name:         self.required_context_for_operation,
            self.operation_controller.union_operation_name:             self.required_context_for_operation,
            self.operation_controller.valid_operation_name:             self.required_context_for_non_spatial_return_operation,
            self.operation_controller.valid_reason_operation_name:      self.required_context_for_non_spatial_return_operation,
            self.operation_controller.within_operation_name:            self.required_context_for_non_spatial_return_operation,
            self.operation_controller.wkb_operation_name:               self.required_context_for_operation,
            self.operation_controller.wkt_operation_name:               self.required_context_for_non_spatial_return_operation,
            self.operation_controller.x_operation_name:                 self.required_context_for_non_spatial_return_operation,
            self.operation_controller.y_operation_name:                 self.required_context_for_non_spatial_return_operation,
            self.operation_controller.z_operation_name:                 self.required_context_for_non_spatial_return_operation,
        })
        return dict

    def operation_name_return_type_dic(self):
        dicti = super(FeatureResource, self).operation_name_return_type_dic()
        dicti.update({
            self.operation_controller.area_operation_name:              self.return_type_for_generic_spatial_operation,
            self.operation_controller.boundary_operation_name:          self.return_type_for_specialized_operation,
            self.operation_controller.buffer_operation_name:            self.return_type_for_specialized_operation,
            self.operation_controller.centroid_operation_name:          self.return_type_for_generic_spatial_operation,
            self.operation_controller.contains_operation_name:          self.return_type_for_generic_spatial_operation,
            self.operation_controller.convex_hull_operation_name:       self.return_type_for_generic_spatial_operation,
            self.operation_controller.coord_seq_operation_name:         self.return_type_for_generic_spatial_operation,
            self.operation_controller.coords_operation_name:            self.return_type_for_generic_spatial_operation,
            self.operation_controller.count_operation_name:             self.return_type_for_generic_spatial_operation,
            self.operation_controller.crosses_operation_name:           self.return_type_for_generic_spatial_operation,
            self.operation_controller.crs_operation_name:               self.return_type_for_generic_spatial_operation,
            self.operation_controller.difference_operation_name:        self.return_type_for_specialized_operation,
            self.operation_controller.dims_operation_name:              self.return_type_for_generic_spatial_operation,
            self.operation_controller.disjoint_operation_name:          self.return_type_for_generic_spatial_operation,
            self.operation_controller.distance_operation_name:          self.return_type_for_generic_spatial_operation,
            self.operation_controller.empty_operation_name:             self.return_type_for_generic_spatial_operation,
            self.operation_controller.envelope_operation_name:          self.return_type_for_specialized_operation,
            self.operation_controller.equals_operation_name:            self.return_type_for_generic_spatial_operation,
            self.operation_controller.equals_exact_operation_name:      self.return_type_for_generic_spatial_operation,
            self.operation_controller.ewkb_operation_name:              self.return_type_for_geometric_representation_operation,
            self.operation_controller.ewkt_operation_name:              self.return_type_for_generic_spatial_operation,
            self.operation_controller.extent_operation_name:            self.return_type_for_generic_spatial_operation,
            self.operation_controller.geojson_operation_name:           self.return_type_for_geometric_representation_operation,
            self.operation_controller.geom_type_operation_name:         self.return_type_for_generic_spatial_operation,
            self.operation_controller.geom_typeid_operation_name:       self.return_type_for_generic_spatial_operation,
            self.operation_controller.get_coords_operation_name:        self.return_type_for_generic_spatial_operation,
            self.operation_controller.get_srid_operation_name:          self.return_type_for_generic_spatial_operation,
            self.operation_controller.get_x_operation_name:             self.return_type_for_generic_spatial_operation,
            self.operation_controller.get_y_operation_name:             self.return_type_for_generic_spatial_operation,
            self.operation_controller.get_z_operation_name:             self.return_type_for_generic_spatial_operation,
            self.operation_controller.has_cs_operation_name:            self.return_type_for_generic_spatial_operation,
            self.operation_controller.hasz_operation_name:              self.return_type_for_generic_spatial_operation,
            self.operation_controller.hex_operation_name:               self.return_type_for_geometric_representation_operation,
            self.operation_controller.hexewkb_operation_name:           self.return_type_for_geometric_representation_operation,
            self.operation_controller.index_operation_name:             self.return_type_for_generic_spatial_operation,
            self.operation_controller.intersection_operation_name:      self.return_type_for_specialized_operation,
            self.operation_controller.intersects_operation_name:        self.return_type_for_generic_spatial_operation,
            self.operation_controller.interpolate_operation_name:       self.return_type_for_generic_spatial_operation,
            self.operation_controller.json_operation_name:              self.return_type_for_geometric_representation_operation,
            self.operation_controller.kml_operation_name:               self.return_type_for_generic_spatial_operation,
            self.operation_controller.length_operation_name:            self.return_type_for_generic_spatial_operation,
            self.operation_controller.normalize_operation_name:         self.return_type_for_generic_spatial_operation,
            self.operation_controller.num_coords_operation_name:        self.return_type_for_generic_spatial_operation,
            self.operation_controller.num_geom_operation_name:          self.return_type_for_generic_spatial_operation,
            self.operation_controller.num_points_operation_name:        self.return_type_for_generic_spatial_operation,
            self.operation_controller.ogr_operation_name:               self.return_type_for_generic_spatial_operation,
            self.operation_controller.overlaps_operation_name:          self.return_type_for_generic_spatial_operation,
            self.operation_controller.point_on_surface_operation_name:  self.return_type_for_generic_spatial_operation,
            self.operation_controller.relate_operation_name:            self.return_type_for_generic_spatial_operation,
            self.operation_controller.relate_pattern_operation_name:    self.return_type_for_generic_spatial_operation,
            self.operation_controller.ring_operation_name:              self.return_type_for_generic_spatial_operation,
            self.operation_controller.simple_operation_name:            self.return_type_for_generic_spatial_operation,
            self.operation_controller.simplify_operation_name:          self.return_type_for_specialized_operation,
            self.operation_controller.srid_operation_name:              self.return_type_for_generic_spatial_operation,
            self.operation_controller.srs_operation_name:               self.return_type_for_generic_spatial_operation,
            self.operation_controller.sym_difference_operation_name:    self.return_type_for_specialized_operation,
            self.operation_controller.touches_operation_name:           self.return_type_for_generic_spatial_operation,
            self.operation_controller.transform_operation_name:         self.return_type_for_specialized_operation,
            self.operation_controller.union_operation_name:             self.return_type_for_specialized_operation,
            self.operation_controller.valid_operation_name:             self.return_type_for_generic_spatial_operation,
            self.operation_controller.valid_reason_operation_name:      self.return_type_for_generic_spatial_operation,
            self.operation_controller.within_operation_name:            self.return_type_for_generic_spatial_operation,
            self.operation_controller.wkb_operation_name:               self.return_type_for_geometric_representation_operation,
            self.operation_controller.wkt_operation_name:               self.return_type_for_geometric_representation_operation,
            self.operation_controller.x_operation_name:                 self.return_type_for_generic_spatial_operation,
            self.operation_controller.y_operation_name:                 self.return_type_for_generic_spatial_operation,
            self.operation_controller.z_operation_name:                 self.return_type_for_generic_spatial_operation,
        })
        return dicti

    def operation_name_resource_type_dic(self):
        dicti = super(FeatureResource, self).operation_name_resource_type_dic()
        dicti.update({
            self.operation_controller.area_operation_name:              self.resource_type_by_operation,
            self.operation_controller.boundary_operation_name:          self.resource_type_by_operation,
            self.operation_controller.buffer_operation_name:            self.resource_type_by_operation,
            self.operation_controller.centroid_operation_name:          self.resource_type_by_operation,
            self.operation_controller.contains_operation_name:          self.resource_type_by_operation,
            self.operation_controller.convex_hull_operation_name:       self.resource_type_by_operation,
            self.operation_controller.coord_seq_operation_name:         self.resource_type_by_operation,
            self.operation_controller.coords_operation_name:            self.resource_type_by_operation,
            self.operation_controller.count_operation_name:             self.resource_type_by_operation,
            self.operation_controller.crosses_operation_name:           self.resource_type_by_operation,
            self.operation_controller.crs_operation_name:               self.resource_type_by_operation,
            self.operation_controller.difference_operation_name:        self.resource_type_by_operation,
            self.operation_controller.dims_operation_name:              self.resource_type_by_operation,
            self.operation_controller.disjoint_operation_name:          self.resource_type_by_operation,
            self.operation_controller.distance_operation_name:          self.resource_type_by_operation,
            self.operation_controller.empty_operation_name:             self.resource_type_by_operation,
            self.operation_controller.envelope_operation_name:          self.resource_type_by_operation,
            self.operation_controller.equals_operation_name:            self.resource_type_by_operation,
            self.operation_controller.equals_exact_operation_name:      self.resource_type_by_operation,
            self.operation_controller.ewkb_operation_name:              self.resource_type_by_operation,
            self.operation_controller.ewkt_operation_name:              self.define_resource_representation_by_str_return_type_operation,
            self.operation_controller.extent_operation_name:            self.resource_type_by_operation,
            self.operation_controller.geojson_operation_name:           self.define_resource_representation_by_str_return_type_operation,
            self.operation_controller.geom_type_operation_name:         self.resource_type_by_operation,
            self.operation_controller.geom_typeid_operation_name:       self.resource_type_by_operation,
            self.operation_controller.get_coords_operation_name:        self.resource_type_by_operation,
            self.operation_controller.get_srid_operation_name:          self.resource_type_by_operation,
            self.operation_controller.get_x_operation_name:             self.resource_type_by_operation,
            self.operation_controller.get_y_operation_name:             self.resource_type_by_operation,
            self.operation_controller.get_z_operation_name:             self.resource_type_by_operation,
            self.operation_controller.has_cs_operation_name:            self.resource_type_by_operation,
            self.operation_controller.hasz_operation_name:              self.resource_type_by_operation,
            self.operation_controller.hex_operation_name:               self.define_resource_representation_by_hex_operation,
            self.operation_controller.hexewkb_operation_name:           self.resource_type_by_operation,
            self.operation_controller.index_operation_name:             self.resource_type_by_operation,
            self.operation_controller.intersection_operation_name:      self.resource_type_by_operation,
            self.operation_controller.intersects_operation_name:        self.resource_type_by_operation,
            self.operation_controller.interpolate_operation_name:       self.resource_type_by_operation,
            self.operation_controller.json_operation_name:              self.define_resource_representation_by_str_return_type_operation,
            self.operation_controller.kml_operation_name:               self.resource_type_by_operation,
            self.operation_controller.length_operation_name:            self.resource_type_by_operation,
            self.operation_controller.normalize_operation_name:         self.resource_type_by_operation,
            self.operation_controller.num_coords_operation_name:        self.resource_type_by_operation,
            self.operation_controller.num_geom_operation_name:          self.resource_type_by_operation,
            self.operation_controller.num_points_operation_name:        self.resource_type_by_operation,
            self.operation_controller.ogr_operation_name:               self.define_resource_representation_by_str_return_type_operation,
            self.operation_controller.overlaps_operation_name:          self.resource_type_by_operation,
            self.operation_controller.point_on_surface_operation_name:  self.resource_type_by_operation,
            self.operation_controller.relate_operation_name:            self.resource_type_by_operation,
            self.operation_controller.relate_pattern_operation_name:    self.resource_type_by_operation,
            self.operation_controller.ring_operation_name:              self.resource_type_by_operation,
            self.operation_controller.simple_operation_name:            self.resource_type_by_operation,
            self.operation_controller.simplify_operation_name:          self.resource_type_by_operation,
            self.operation_controller.srid_operation_name:              self.resource_type_by_operation,
            self.operation_controller.srs_operation_name:               self.resource_type_by_operation,
            self.operation_controller.sym_difference_operation_name:    self.resource_type_by_operation,
            self.operation_controller.touches_operation_name:           self.resource_type_by_operation,
            self.operation_controller.transform_operation_name:         self.resource_type_by_operation,
            self.operation_controller.union_operation_name:             self.resource_type_by_operation,
            self.operation_controller.valid_operation_name:             self.resource_type_by_operation,
            self.operation_controller.valid_reason_operation_name:      self.resource_type_by_operation,
            self.operation_controller.within_operation_name:            self.resource_type_by_operation,
            self.operation_controller.wkb_operation_name:               self.resource_type_by_operation,
            self.operation_controller.wkt_operation_name:               self.define_resource_representation_by_str_return_type_operation,
            self.operation_controller.x_operation_name:                 self.resource_type_by_operation,
            self.operation_controller.y_operation_name:                 self.resource_type_by_operation,
            self.operation_controller.z_operation_name:                 self.resource_type_by_operation,
        })
        return dicti

    def required_object_for_simple_path(self, request):
        if self.is_image_content_type(request):
            return self.required_object_for_image(self.object_model, request)
        serialized_data = self.serializer_class(self.object_model, context={'request': request}).data

        if self.accept_is_binary(request):
            serialized_data = geobuf.encode(serialized_data)

        return RequiredObject(serialized_data, self.content_type_by_accept(request), self.object_model, 200, self.e_tag)

    def required_object_for_only_attributes(self, request, attributes_functions_str):
        if self.is_image_content_type(request):
            object = self.get_object_by_only_attributes(attributes_functions_str)
            return self.required_object_for_image(object, request)

        return super(FeatureResource, self).required_object_for_only_attributes(request, attributes_functions_str)

    '''
    def required_object_for_transform_operation(self, request, attributes_functions_str):
        self.get_object_from_transform_spatial_operation(attributes_functions_str)
    '''

    def define_head_content_type(self, request, attributes_functions_str):
        if self.is_simple_path(attributes_functions_str):
            return self.content_type_by_accept(request)
        if self.path_has_only_attributes(attributes_functions_str):
            return self.content_type_by_attributes(request, attributes_functions_str)

        return self.content_type_for_operation(request, attributes_functions_str)

    def default_content_type_for(self, resource_type):
        if issubclass(resource_type, GEOSGeometry):
            return self.default_content_type()
        return super(FeatureResource, self).default_content_type_for(resource_type)

    def resource_type_content_type_dict(self):
        contypes_dict = super(FeatureResource, self).resource_type_content_type_dict()
        contypes_dict.update({
            GEOSGeometry: [CONTENT_TYPE_GEOJSON, CONTENT_TYPE_IMAGE_PNG, CONTENT_TYPE_OCTET_STREAM],
            SpatialReference: [CONTENT_TYPE_JSON, CONTENT_TYPE_OCTET_STREAM]
        })
        return contypes_dict

    def available_content_types_for(self, resource_type):
        try:
            if issubclass(resource_type, GEOSGeometry):
                return [CONTENT_TYPE_GEOJSON, CONTENT_TYPE_IMAGE_PNG, CONTENT_TYPE_OCTET_STREAM]
        except TypeError:
            if issubclass(type(resource_type), GeometryField):
                return [CONTENT_TYPE_GEOJSON, CONTENT_TYPE_IMAGE_PNG, CONTENT_TYPE_OCTET_STREAM]

        return super(FeatureResource, self).available_content_types_for(resource_type)

    def content_type_by_attributes(self, request, attributes_str):
        attrs_list = self.remove_last_slash(attributes_str).split(LIST_ELEMENTS_SEPARATOR)
        contype_accept = self.content_type_by_accept(request)

        if self.geometry_field_name() in attrs_list:
            geometric_field = self.field_for(self.geometry_field_name())
            if contype_accept in self.available_content_types_for(geometric_field):
                return contype_accept
            return self.default_content_type_for(geometric_field)

        return super(FeatureResource, self).content_type_by_attributes(request, attributes_str)

    def content_type_for_operation(self, request, attributes_functions_str):
        contype_accept = self.content_type_by_accept(request)
        operation_return_type = self.operation_controller.state_machine(attributes_functions_str)

        if contype_accept in self.available_content_types_for(operation_return_type):
            return contype_accept
        return self.default_content_type_for(operation_return_type)

    def required_object_for_spatial_operation(self, request, attributes_functions_str):
        if self.path_has_url(attributes_functions_str.lower()):
            result = self.get_object_from_operation_attributes_functions_str_with_url(attributes_functions_str, request)
        else:
            result = self.get_object_from_operation(self.remove_last_slash(attributes_functions_str))

        operation_contype = self.content_type_for_operation(request, attributes_functions_str)

        if operation_contype == CONTENT_TYPE_IMAGE_PNG:
            return self.required_object_for_image( GEOSGeometry(json.dumps(result)), request)

        elif isinstance(result, memoryview) or isinstance(result, buffer) or isinstance(result, bytes):
            return RequiredObject(result, CONTENT_TYPE_IMAGE_PNG, self.object_model, 200)

        else:
            return RequiredObject(result, operation_contype, self.object_model, 200)

    def get_objects_from_join_operation(self, request, attributes_functions_str):
        join_operation = self.build_join_operation(request, attributes_functions_str)

        if type(join_operation.right_join_data) is list:
            return self.join_feature_on_list_response(join_operation)
        return self.join_feature_on_dict_response(join_operation)

    def join_feature_on_dict_response(self, join_operation):
        if  join_operation.left_join_data['properties'][ join_operation.left_join_attr ] != join_operation.right_join_data[ join_operation.right_join_attr ]:
            return None # the datas isn't 'joinable'

        join_operation.left_join_data["properties"]["__joined__"] = []
        join_operation.left_join_data["properties"]["__joined__"].append(join_operation.right_join_data)
        return deepcopy(join_operation.left_join_data)

    def join_feature_on_list_response(self, join_operation):
        join_operation.left_join_data['properties']['__joined__'] = []

        for dicti in join_operation.right_join_data:
            if join_operation.left_join_data['properties'][join_operation.left_join_attr] == dicti[join_operation.right_join_attr]:
                join_operation.left_join_data['properties']['__joined__'].append(dicti)

        if len(join_operation.left_join_data['properties']['__joined__']) == 0:
            return None
        return join_operation.left_join_data

    def get_context_for_join_operation(self, request, attributes_functions_str):
        geometric_uri, join_attr, alphanumeric_uri = self.split_join_uri(request, attributes_functions_str)
        return self.get_dict_from_response( requests.options(geometric_uri) )

        #todo: code for 'join' full context - DO NOT DELETE
        '''
        resource_type = self.resource_type_or_default_resource_type(request)
        context = self.context_resource.get_resource_type_identification(resource_type)
        context["hydra:supportedOperations"] = self.context_resource.supportedOperationsFor(self.object_model, resource_type)
        context["@context"] = self.context_resource.get_context_to_operation(self.operation_controller.join_operation_name)["@context"]
        context["@context"].update( self.get_merged_acontext_from_join_operation(request, attributes_functions_str) )

        return context
        '''

    #todo: code for 'join' full context - DO NOT DELETE
    def get_merged_acontext_from_join_operation(self, request, attributes_functions_str):
        geometric_uri, join_attr, alphanumeric_uri = self.split_join_uri(request, attributes_functions_str)

        geometric_acontext = self.get_dict_from_response( requests.options(geometric_uri) )["@context"]
        alphanumeric_acontext = self.get_dict_from_response( requests.options(alphanumeric_uri) )["@context"]

        alpha_acontext_renamed_keys = {}
        for k, v in alphanumeric_acontext.items():
            if k in geometric_acontext.keys():
                alpha_acontext_renamed_keys[alphanumeric_uri + "/" + k] = v
            else:
                alpha_acontext_renamed_keys[k] = v

        geometric_acontext.update(alpha_acontext_renamed_keys)

        return geometric_acontext
        #if set(geometric_context.keys()).intersection( set(alphanumeric_context.keys()) ):

    #todo: code for 'join' full context - DO NOT DELETE
    def add_context_to_joined_external_attributes(self, external_attributes_context):
        pass

    def get_context_for_operation(self, request, attributes_functions_str):
        operation_name = self.get_operation_name_from_path(attributes_functions_str)

        operation_return_type = self.operation_controller.state_machine(attributes_functions_str)
        if issubclass(GEOSGeometry, operation_return_type) or issubclass(GeometryField, operation_return_type):
            operation_return_type = self.dict_string_to_geom_type()[self.initial_geom_type]

        context = self.context_resource.get_resource_id_and_type_by_operation_return_type(operation_name, operation_return_type)
        context['@context'] = self.context_resource.get_subClassOf_term_definition()
        context[HYPER_RESOURCE_SUPPORTED_OPERATIONS_LABEL] = self.context_resource.supportedOperationsFor(self.object_model, operation_return_type)
        return context

    def required_context_for_non_spatial_return_operation(self, request, attributes_functions_str):
        context = self.get_context_for_non_spatial_return_operation(request, attributes_functions_str)
        return RequiredObject(context, HYPER_RESOURCE_CONTENT_TYPE, self.object_model, 200)

    def required_context_for_simple_path(self, request):
        resource_representation = self.resource_type_or_default_resource_type(request)

        if self.content_type_by_accept(request) == CONTENT_TYPE_IMAGE_PNG:
            return RequiredObject(self.context_resource.context_for_image(), HYPER_RESOURCE_CONTENT_TYPE, self.object_model, 200)

        return RequiredObject(self.context_resource.context(resource_representation), HYPER_RESOURCE_CONTENT_TYPE,self.object_model, 200)

    def get_context_by_only_attributes(self, request, attributes_functions_str):
        context = super(FeatureResource, self).get_context_by_only_attributes(request, attributes_functions_str)
        if self.geometry_field_name() in context["@context"].keys():
            context["@context"].pop(self.geometry_field_name())
        return context

    def get_context_for_non_spatial_return_operation(self, request, attributes_functions_str):
        context = self.get_context_for_operation(request, attributes_functions_str)
        operation_name = self.get_operation_name_from_path(attributes_functions_str)
        context["@context"].update(self.context_resource.get_operation_return_type_term_definition(operation_name))
        return context

    def return_type_by_only_attributes(self, attributes_functions_str):
        attrs = self.remove_last_slash(attributes_functions_str).split(",")
        if len(attrs) > 1:
            if self.geometry_field_name() in attrs:
                return "Feature"
            return object

        object_model = self.get_object(self.kwargs)
        attr_val = getattr(object_model, attrs[0])

        if attrs[0] == self.geometry_field_name():
            return attr_val.geom_type
        return type(attr_val)

    def return_type_for_specialized_operation(self, attributes_functions_str):
        '''
        Return type depends on specific geometry type
        '''
        model_object = self.get_object(self.kwargs)
        geom_val = getattr(model_object, self.geometry_field_name())
        operation_name = self.get_operation_name_from_path(attributes_functions_str)

        if self.path_has_url(attributes_functions_str):
            _ , url_external_resource, parameters_list = self.attributes_functions_splitted_by_url(attributes_functions_str)
            response = requests.get(url_external_resource)

            if response.status_code in[400, 401, 404, 500]:
                return None #operation_params = GEOSGeometry(Point([0, 0]))

            operation_params = [response.text]
            if parameters_list is not None:
                operation_params.append(parameters_list)

        else:
            operation_params = self.remove_last_slash(attributes_functions_str).split("/")[1:]
        return type( self._execute_attribute_or_method(geom_val, operation_name, operation_params) )

    def return_type_for_generic_spatial_operation(self, attributes_functions_str):
        operation_name = self.get_operation_name_from_path(attributes_functions_str)
        return self.operation_controller.dict_all_operation_dict()[operation_name].return_type

    # wkb, ewkb, hex, hexewkb, wkt, ogr, json, geojson, ogr operations returns an binary or text representation of an geometry
    def return_type_for_geometric_representation_operation(self, attributes_functions_str):
        model_object = self.get_object(self.kwargs)
        geom_val = getattr(model_object, self.geometry_field_name())
        return type(geom_val)

    def get_object_serialized_by_only_attributes(self, attributes_functions_str, object):
        attrs_arr = self.remove_last_slash(attributes_functions_str).split(',')
        serialized_object = {}

        for attr_name, attr_val in object.items():
            if attr_name == self.geometry_field_name():
                serialized_object[attr_name] = json.loads(object[attr_name].geojson)
            else:
                serialized_object[attr_name] = object[attr_name]

        if self.geometry_field_name() in attrs_arr:
            if len(attrs_arr) > 1:
                return self.dict_as_geojson(serialized_object)
            else:
                return serialized_object[self.geometry_field_name()]
        return serialized_object

    def get_operation_name_from_path(self, attributes_functions_str):
        arr_att_funcs = self.remove_last_slash(attributes_functions_str).lower().split('/')

        # join operation has priority
        if self.path_has_join_operation(attributes_functions_str):
            return self.operation_controller.join_operation_name
        else:
            first_part_name =  arr_att_funcs[0]

        if first_part_name not in self.operation_controller.operations_dict():
            return None
        return first_part_name

    def basic_get(self, request, *args, **kwargs):
        self.object_model = self.get_object(kwargs)
        self.current_object_state = self.object_model
        self.set_basic_context_resource(request)

        attributes_functions_str = kwargs.get(self.attributes_functions_name_template())

        if self.is_simple_path(attributes_functions_str):
            return self.required_object_for_simple_path(request)

        if self.path_has_only_attributes(attributes_functions_str):
            return self.required_object_for_only_attributes(request, attributes_functions_str)

        res = self.get_required_object_from_method_to_execute(request, attributes_functions_str)
        if res is None:
            return self.required_object_for_invalid_sintax(attributes_functions_str)
        return res

    def basic_options(self, request, *args, **kwargs):
        self.object_model = self.model_class()()
        self.set_basic_context_resource(request)
        attributes_functions_str = self.kwargs.get("attributes_functions", None)

        dicti = self.dic_with_only_identitier_field(kwargs)
        self.initial_geom_type = self.model_class().objects.get(**dicti).geom_type()

        if self.is_simple_path(attributes_functions_str):
            return self.required_context_for_simple_path(request)
        if self.path_has_only_attributes(attributes_functions_str):
            return self.required_context_for_only_attributes(request, attributes_functions_str)

        res = self.get_required_context_from_method_to_execute(request, attributes_functions_str)
        if res is None:
            return self.required_object_for_invalid_sintax(attributes_functions_str)
        return res

    def default_content_type(self):
        return CONTENT_TYPE_GEOJSON#self.temporary_content_type if self.temporary_content_type is not None else CONTENT_TYPE_GEOJSON

    def resource_type_by_only_attributes(self, request, attributes_functions_str):
        attrs_functs_arr = self.remove_last_slash(attributes_functions_str).split(LIST_ELEMENTS_SEPARATOR)
        r_type = self.resource_type_or_default_resource_type(request)
        if r_type != self.default_resource_type():
            return r_type if self.geometry_field_name() in attrs_functs_arr else bytes

        if len(attrs_functs_arr) == 1:
            # the field type has priority over default resource type
            return type(self.field_for(attrs_functs_arr[0]))

        return r_type if self.geometry_field_name() in attrs_functs_arr else 'Thing'

    def dict_string_to_geom_type(self):
        return {
            'Point': Point,
            'LineString': LineString,
            'Polygon': Polygon,
            'MultiPoint': MultiPoint,
            'MultiLineString': MultiLineString,
            'MultiPolygon': MultiPolygon
        }

    def default_value_for_field(self, field):
        try:
            geometries_dict = {
                "GEOMETRY": GEOSGeometry("POINT(0 0)"),
                "POINT": GEOSGeometry("POINT(0 0)"),
                "LINESTRING": GEOSGeometry("LINESTRING (30 10, 10 30, 40 40)"),
                "POLYGON": GEOSGeometry("POLYGON ((35 10, 45 45, 15 40, 10 20, 35 10),(20 30, 35 35, 30 20, 20 30))"),
                "MULTIPOINT": GEOSGeometry("MULTIPOINT (10 40, 40 30, 20 20, 30 10)"),
                "MULTILINESTRING": GEOSGeometry("MULTILINESTRING ((10 10, 20 20, 10 40),(40 40, 30 30, 40 20, 30 10))"),
                'MULTIPOLYGON': GEOSGeometry("MULTIPOLYGON (((40 40, 20 45, 45 30, 40 40)),((20 35, 10 30, 10 10, 30 5, 45 20, 20 35),(30 20, 20 15, 20 25, 30 20)))"),
            }
            return geometries_dict[field.geom_type]
        except (KeyError, AttributeError):
            if issubclass(field, GEOSGeometry):
                geometries_dict = {
                    GEOSGeometry: GEOSGeometry("POINT(0 0)"),
                    Point: GEOSGeometry("POINT(0 0)"),
                    LineString: GEOSGeometry("LINESTRING (30 10, 10 30, 40 40)"),
                    Polygon: GEOSGeometry("POLYGON ((35 10, 45 45, 15 40, 10 20, 35 10),(20 30, 35 35, 30 20, 20 30))"),
                    MultiPoint: GEOSGeometry("MULTIPOINT (10 40, 40 30, 20 20, 30 10)"),
                    MultiLineString: GEOSGeometry("MULTILINESTRING ((10 10, 20 20, 10 40),(40 40, 30 30, 40 20, 30 10))"),
                    MultiPolygon: GEOSGeometry("MULTIPOLYGON (((40 40, 20 45, 45 30, 40 40)),((20 35, 10 30, 10 10, 30 5, 45 20, 20 35),(30 20, 20 15, 20 25, 30 20)))"),
                }
                return geometries_dict[field]
        return super(FeatureResource, self).default_value_for_field(field)

    def return_type_for_operation(self, object, attribute_or_function_name, parameters):
        attribute_or_function_name_striped = self.remove_last_slash(attribute_or_function_name)
        self.name_of_last_operation_executed = attribute_or_function_name_striped

        if  attribute_or_function_name_striped in self.operation_controller.dict_all_operation_dict():
            return self.get_operation_type_called(attribute_or_function_name_striped).return_type

        return self.default_value_for_field( self.field_for(attribute_or_function_name) )

    def resource_type_by_operation(self, request, attributes_functions_str):
        operation_return_type = self.operation_controller.state_machine(attributes_functions_str)
        res_type_by_accept = self.resource_type_or_default_resource_type(request)

        if operation_return_type == GEOSGeometry:
            return res_type_by_accept
        elif type(operation_return_type) is not str and issubclass(operation_return_type, GEOSGeometry):
            return res_type_by_accept if res_type_by_accept != self.default_resource_type() else operation_return_type
        else:
            res_type_by_accept = bytes if res_type_by_accept == 'Geobuf' else res_type_by_accept

        return operation_return_type if res_type_by_accept == self.default_resource_type() else res_type_by_accept

    def define_resource_representation_by_wkt_operation(self, request, attributes_functions_str):
        '''
        WKT returns an string representation of a geometry
        '''
        resource_representation_by_accept = self.resource_type_or_default_resource_type(request)
        if resource_representation_by_accept == self.default_resource_type():
            return str

    def define_resource_representation_by_ewkt_operation(self, request, attributes_functions_str):
        '''
        EWKT returns an string representation of a geometry
        '''
        resource_representation_by_accept = self.resource_type_or_default_resource_type(request)
        if resource_representation_by_accept == self.default_resource_type():
            return str

    def define_resource_representation_by_hex_operation(self, request, attributes_functions_str):
        '''
        EWKT returns an string representation of a geometry
        '''
        resource_representation_by_accept = self.resource_type_or_default_resource_type(request)
        if resource_representation_by_accept == self.default_resource_type():
            return bytes

    def define_resource_representation_by_str_return_type_operation(self, request, attributes_functions_str):
        '''
        WKT, ORG, EWKT, GEOJSON, JSON operations returns an string representation of a geometry
        '''
        resource_representation_by_accept = self.resource_type_or_default_resource_type(request)
        if resource_representation_by_accept == self.default_resource_type():
            return str

    def get(self, request, format=None, *args, **kwargs):
        self.change_request_if_image_png_into_IRI(request)
        #self.iri_metadata = self.model_class().objects.first().iri_metadata
        return super(FeatureResource,self).get(request, *args, **self.kwargs)