# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.contrib.gis.db.models import GeometryField
from django.contrib.gis.db.models import LineStringField
from django.contrib.gis.db.models import MultiLineStringField
from django.contrib.gis.db.models import MultiPointField
from django.contrib.gis.db.models import MultiPolygonField
from django.contrib.gis.db.models import PointField
from django.contrib.gis.db.models import PolygonField
from django.contrib.gis.gdal import OGRGeometry
from django.contrib.gis.gdal import SpatialReference
from django.contrib.gis.geos import GEOSGeometry, Point, Polygon, MultiPolygon,LineString, MultiLineString, MultiPoint, GeometryCollection
from datetime import date, datetime
from time import *
from copy import deepcopy

from django.contrib.gis.geos.prepared import PreparedGeometry
from django.db.models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse

from hyper_resource.models import *
from hyper_resource.resources import FeatureResource
from hyper_resource.resources.AbstractResource import *
from hyper_resource.resources.AbstractCollectionResource import GROUP_BY_SUM_PROPERTY_NAME
from django.db.models.fields import NOT_PROVIDED

from hyper_resource.resources.FeatureResource import FEATURE_RESOURCE_TYPE
from hyper_resource.utils import IMAGE_RESOURCE_TYPE

HYPER_RESOURCE_SUPPORTED_OPERATIONS_LABEL = "hydra:supportedOperations" #todo: change to something like "hyper:supportedOperations" when created hyper vocab

class Reflection:

    def superclass(a_class):
        return a_class.__base__

    def supeclasses(a_class):
        return a_class.__bases__

    def operation_names(a_class):
        return [method for method in dir ( a_class ) if
                callable ( getattr ( a_class, method ) ) and a_class.is_not_private ( method )]


def vocabularyDict():
    dict = {}
    dict[BooleanField] = 'http://schema.org/Boolean'
    dict[bool] = 'https://schema.org/Boolean'
    dict[True] = 'https://schema.org/Boolean'
    dict[False] = 'https://schema.org/Boolean'
    dict[FloatField] = 'https://schema.org/Float'
    dict[float] = 'https://schema.org/Float'
    dict[ForeignKey] = 'http://schema.org/URL'
    dict[IntegerField] = 'https://schema.org/Integer'
    dict[BigIntegerField] = "https://schema.org/Integer"
    dict[DecimalField] = 'https://schema.org/Float'
    dict[AutoField]= 'https://schema.org/identifier'
    dict[int] = 'https://schema.org/Integer'
    dict[CharField] = 'https://schema.org/Text'
    dict[TextField] = 'https://schema.org/Text'
    dict[str] = 'https://schema.org/Text'
    dict[DateField] = 'http://schema.org/Date'
    dict[date] = 'http://schema.org/Date'
    dict[DateTimeField] = 'http://schema.org/DateTime'
    dict[datetime] = 'http://schema.org/DateTime'
    dict[TimeField] = 'http://schema.org/Time'
    dict[Model] = 'https://purl.org/geojson/vocab#Feature'
    dict[tuple]= 'https://schema.org/ItemList'
    dict[list]= 'https://schema.org/ItemList'

    dict[Q] = 'http://extension.schema.org/expression'
    dict[bytes] = 'https://extension.schema.org/binary'
    dict[object] = 'https://schema.org/Thing'
    dict['Collection'] = 'http://www.w3.org/ns/hydra/core#Collection'
    dict['Link'] = "http://www.w3.org/ns/hydra/core#Link"
    dict[GROUP_BY_SUM_PROPERTY_NAME] = 'https://schema.org/Float'
    dict["hydra"] = "http://www.w3.org/ns/hydra/core#"

    dict['nome'] = 'https://schema.org/name'
    dict['name'] = 'https://schema.org/name'
    dict['nomeAbrev'] = 'https://schema.org/alternateName'
    dict['responsible'] = 'http://schema.org/accountablePerson'
    dict['usuario'] = 'http://schema.org/Person'
    dict['user'] = 'http://schema.org/Person'

    dict['FeatureCollection'] = 'https://purl.org/geojson/vocab#FeatureCollection'
    dict[FeatureCollection] = 'https://purl.org/geojson/vocab#FeatureCollection'
    dict['Feature'] = 'https://purl.org/geojson/vocab#Feature'
    dict[FeatureModel] = 'https://purl.org/geojson/vocab#Feature'
    dict[FeatureResource] = 'https://purl.org/geojson/vocab#Feature'
    dict[GeometryField] = 'https://purl.org/geojson/vocab#geometry'
    dict[PointField] = 'https://purl.org/geojson/vocab#Point'
    dict[LineStringField] = 'https://purl.org/geojson/vocab#LineString'
    dict[PolygonField] = 'https://purl.org/geojson/vocab#Polygon'
    dict[MultiPolygonField] = 'https://purl.org/geojson/vocab#MultiPolygon'
    dict[MultiLineStringField] = 'https://purl.org/geojson/vocab#MultiLineString'
    dict[MultiPointField] = 'https://purl.org/geojson/vocab#MultiPoint'

    dict[MultiPolygon] = 'https://purl.org/geojson/vocab#MultiPolygon'
    dict['MultiPolygon'] = 'https://purl.org/geojson/vocab#MultiPolygon'
    dict[Polygon] = 'https://purl.org/geojson/vocab#Polygon'
    dict['Polygon'] = 'https://purl.org/geojson/vocab#Polygon'
    dict[LineString] = 'https://purl.org/geojson/vocab#LineString'
    dict['LineString'] = 'https://purl.org/geojson/vocab#LineString'
    dict[Point] = 'https://purl.org/geojson/vocab#Point'
    dict['Point'] = 'https://purl.org/geojson/vocab#Point'
    dict[GEOSGeometry] = 'https://purl.org/geojson/vocab#geometry'
    dict['GEOSGeometry'] = 'https://purl.org/geojson/vocab#geometry'
    dict[OGRGeometry] = 'https://purl.org/geojson/vocab#geometry'
    dict['OGRGeometry'] = 'https://purl.org/geojson/vocab#geometry'
    dict[MultiLineString] = 'https://purl.org/geojson/vocab#MultiLineString'
    dict['MultiLineString'] = 'https://purl.org/geojson/vocab#MultiLineString'
    dict[MultiPoint] = 'https://purl.org/geojson/vocab#MultiPoint'
    dict['MultiPoint'] = 'https://purl.org/geojson/vocab#MultiPoint'
    dict[GeometryCollection] = 'https://purl.org/geojson/vocab#GeometryCollection'
    dict['GeometryCollection'] = 'https://purl.org/geojson/vocab#GeometryCollection'
    dict[SpatialReference] = 'https://purl.org/geojson/vocab#SpatialReference'
    dict['SpatialReference'] = 'https://purl.org/geojson/vocab#SpatialReference'

    #collection
    dict['filter'] = 'http://opengis.org/operations/filter'
    dict['filter'] = 'http://ggt-des.ibge.gov.br/api/operations-list/collection-operation-interface-list/1/'
    dict['map'] = 'http://opengis.org/operations/map'
    dict['annotate'] = 'http://opengis.org/operations/annotate'
    dict['group-by'] = "http://ggt-des.ibge.gov.br/api/operations-list/collection-operation-interface-list/6/"
    dict['group-by-sum'] = 'http://ggt-des.ibge.gov.br/api/operations-list/collection-operation-interface-list/10/'
    dict['group-by-count'] = 'http://ggt-des.ibge.gov.br/api/operations-list/collection-operation-interface-list/7/'
    dict['distinct'] = 'http://ggt-des.ibge.gov.br/api/operations-list/collection-operation-interface-list/5/'
    dict['count-resource'] = 'http://ggt-des.ibge.gov.br/api/operations-list/collection-operation-interface-list/count-resource/'
    dict['resource-quantity'] = "https://schema.org/Integer"
    dict['collect'] = 'http://ggt-des.ibge.gov.br/api/operations-list/collection-operation-interface-list/2/'
    dict['join'] = 'http://ggt-des.ibge.gov.br/api/operations-list/object-operations-interface-list/1/'
    dict['projection'] = 'http://ggt-des.ibge.gov.br/api/operations-list/object-operations-interface-list/2/'
    dict['make_line'] = 'http://ggt-des.ibge.gov.br/api/operations-list/spatial-collection-operation-interface-list/30'
    dict['count_elements'] = 'http://opengis.org/operations/count_elements'
    #dict['offset_limit'] = 'http://opengis.org/operations/offset_limit'
    dict['offset-limit'] = "http://ggt-des.ibge.gov.br/api/operations-list/collection-operation-interface-list/4"
    dict['distance_lte'] = 'http://opengis.org/operations/distance_lte'
    #dict['area'] = 'http://opengis.org/operations/area'
    dict['area'] = "http://ggt-des.ibge.gov.br/api/operations-list/spatial-operation-interface-list/77"
    #dict['boundary'] = 'http://opengis.org/operations/boundary'
    dict['boundary'] = 'http://ggt-des.ibge.gov.br/api/operations-list/spatial-operation-interface-list/78'
    #dict['buffer'] = 'http://opengis.org/operations/buffer'
    dict['buffer'] = 'http://ggt-des.ibge.gov.br/api/operations-list/spatial-operation-interface-list/79'
    dict['centroid'] = 'http://opengis.org/operations/centroid'
    dict['contains'] = 'http://opengis.org/operations/contains'
    dict['convex_hull'] = 'http://opengis.org/operations/convex_hull'
    dict['coord_seq'] = 'http://opengis.org/operations/coord_seq'
    dict['coords'] = 'https://purl.org/geojson/vocab#coordinates'
    dict['count'] = 'http://opengis.org/operations/count'
    dict['crosses'] = 'http://opengis.org/operations/crosses'
    dict['crs'] = 'http://opengis.org/operations/crs'
    dict['difference'] = 'http://opengis.org/operations/difference'
    dict['dims'] = 'http://opengis.org/operations/dims'
    dict['disjoint'] = 'http://opengis.org/operations/disjoint'
    dict['distance'] = 'http://opengis.org/operations/distance'
    dict['empty'] = 'http://opengis.org/operations/empty'
    dict['envelope'] = 'http://opengis.org/operations/envelope'
    dict['equals'] = 'http://opengis.org/operations/equals'
    dict['equals_exact'] = 'http://opengis.org/operations/equals_exact'
    dict['ewkb'] = 'http://opengis.org/operations/ewkb'
    dict['ewkt'] = 'http://opengis.org/operations/ewkt'
    dict['extend'] = 'http://opengis.org/operations/extend'
    dict['extent'] = 'http://opengis.org/operations/extent'
    dict['geojson'] = 'http://opengis.org/operations/geojson'
    dict['geom_type'] = 'http://opengis.org/operations/geom_type'
    dict['geom_typeid'] = 'http://opengis.org/operations/geom_typeid'
    dict['get_coords'] = 'http://opengis.org/operations/get_coords'
    dict['get_srid'] = 'http://opengis.org/operations/get_srid'
    dict['get_x'] = 'http://opengis.org/operations/get_x'
    dict['get_y'] = 'http://opengis.org/operations/get_y'
    dict['get_z'] = 'http://opengis.org/operations/get_z'
    dict['has_cs'] = 'http://opengis.org/operations/has_cs'
    dict['hasz'] = 'http://opengis.org/operations/hasz'
    dict['hex'] = 'http://opengis.org/operations/hex'
    dict['hexewkb'] = 'http://opengis.org/operations/hexewkb'
    dict['index'] = 'http://opengis.org/operations/index'
    dict['intersection'] = 'http://opengis.org/operations/intersection'
    dict['intersects'] = 'http://opengis.org/operations/intersects'
    dict['interpolate'] = 'http://opengis.org/operations/interpolate'
    dict['json'] = 'http://opengis.org/operations/json'
    dict['kml'] = 'http://opengis.org/operations/kml'
    dict['length'] = 'http://opengis.org/operations/length'
    dict['normalize'] = 'http://opengis.org/operations/normalize'
    dict['num_coords'] = 'http://opengis.org/operations/num_coords'
    dict['num_geom'] = 'http://opengis.org/operations/num_geom'
    dict['num_s'] = 'http://opengis.org/operations/num_s'
    dict['num_points']  = 'http://opengis.org/operations/num_points'
    dict['point_on_surface'] = 'http://opengis.org/operations/point_on_surface'
    dict['ogr'] = 'http://opengis.org/operations/ogr'
    dict['overlaps'] = 'http://opengis.org/operations/overlaps'
    dict['_on_surface'] = 'http://opengis.org/operations/_on_surface'
    dict['pop'] = 'http://opengis.org/operations/pop'
    dict['prepared'] = 'http://opengis.org/operations/prepared'
    dict['relate'] = 'http://opengis.org/operations/relate'
    dict['relate_pattern'] = 'http://opengis.org/operations/relate_pattern'
    dict['ring'] = 'http://opengis.org/operations/ring'
    dict['set_coords'] = 'http://opengis.org/operations/set_coords'
    dict['set_srid'] = 'http://opengis.org/operations/set_srid'
    dict['set_x'] = 'http://opengis.org/operations/set_x'
    dict['set_y'] = 'http://opengis.org/operations/set_y'
    dict['set_z'] = 'http://opengis.org/operations/set_z'
    dict['simple'] = 'http://opengis.org/operations/simple'
    dict['simplify'] = 'http://opengis.org/operations/simplify'
    dict['srid'] = 'http://opengis.org/operations/srid'
    dict['srs'] = 'http://opengis.org/operations/srs'
    dict['sym_difference'] = 'http://opengis.org/operations/sym_difference'
    dict['touches'] = 'http://opengis.org/operations/touches'
    dict['transform'] = 'http://opengis.org/operations/transform'
    dict['tuple'] = 'http://opengis.org/operations/tuple'
    dict['union'] = 'http://opengis.org/operations/union'
    dict['valid'] = 'http://opengis.org/operations/valid'
    dict['valid_reason'] = 'http://opengis.org/operations/valid_reason'
    dict['within'] = 'http://opengis.org/operations/within'
    dict['wkb'] = 'http://opengis.org/operations/wkb'
    dict['wkt'] = 'http://opengis.org/operations/wkt'
    dict['x'] = 'http://opengis.org/operations/x'
    dict['y'] = 'http://opengis.org/operations/y'
    dict['z'] = 'http://opengis.org/operations/z'

    dict['distance_gt'] = 'http://opengis.org/operations/distance_gt'
    dict['overlaps-right'] = 'http://opengis.org/operations/overlaps-right'
    dict['contained'] = 'http://opengis.org/operations/contained'
    dict['distance_lt'] = 'http://opengis.org/operations/distance_lt'
    dict['dwithin'] = 'http://opengis.org/operations/dwithin'
    dict['bboverlaps'] = 'http://opengis.org/operations/bboverlaps'
    dict['bbcontains'] = 'http://opengis.org/operations/bbcontains'
    dict['distance_gte'] = 'http://opengis.org/operations/distance_gte'
    dict['overlaps-below'] = 'http://opengis.org/operations/overlaps-below'
    dict['overlaps-above'] = 'http://opengis.org/operations/overlaps-above'
    dict['overlaps-left'] = 'http://opengis.org/operations/overlaps-left'
    dict['contains-properly'] = 'http://opengis.org/operations/contains-properly'
    dict['isvalid'] = 'http://opengis.org/operations/isvalid'
    dict['right'] = 'http://opengis.org/operations/right'
    dict['exact'] = 'http://opengis.org/operations/exact'
    dict['covers'] = 'http://opengis.org/operations/covers'
    dict['strictly_below'] = 'http://opengis.org/operations/strictly_below'
    dict['left'] = 'http://opengis.org/operations/left'
    dict['same_as'] = 'http://opengis.org/operations/same_as'
    dict['coveredby'] = 'http://opengis.org/operations/coveredby'
    dict['strictly_above'] = 'http://opengis.org/operations/strictly_above'
    dict['operation'] = 'http://www.w3.org/ns/hydra/core#operation'
    dict[property] = 'http://www.w3.org/ns/hydra/core#property'
    dict['EntryPoint'] = 'http://www.w3.org/ns/hydra/core#entrypoint'
    dict['Tiff'] = "https://schema.org/ImageObject"
    dict[GDALRaster] = "https://schema.org/ImageObject"
    dict[RasterField] = "https://schema.org/ImageObject"

    return dict

def OperationVocabularyDict():
    dic = {}
    #dic[int] = ["http://ggt-des.ibge.gov.br/api/operations-list/integer-operations-interface/"]
    #dic[AutoField] = ["http://ggt-des.ibge.gov.br/api/operations-list/integer-operations-interface/"]
    #dic[IntegerField] = ["http://ggt-des.ibge.gov.br/api/operations-list/integer-operations-interface/"]

    dic[str] = ["http://ggt-des.ibge.gov.br/api/operations-list/string-operation-interface-list"]
    dic['str'] = ["http://ggt-des.ibge.gov.br/api/operations-list/string-operation-interface-list"]
    dic[CharField] = ["http://ggt-des.ibge.gov.br/api/operations-list/string-operation-interface-list"]

    dic[date] = ["http://ggt-des.ibge.gov.br/api/operations-list/date-operation-interface-list"]

    dic[GEOSGeometry] = ["http://ggt-des.ibge.gov.br/api/operations-list/spatial-operation-interface-list"]
    dic[GeometryField] = ["http://ggt-des.ibge.gov.br/api/operations-list/spatial-operation-interface-list"]
    dic[GeometryCollection] = ["http://ggt-des.ibge.gov.br/api/operations-list/spatial-operation-interface-list"]
    dic[PointField] = ["http://ggt-des.ibge.gov.br/api/operations-list/spatial-operation-interface-list"]
    dic[Point] = ["http://ggt-des.ibge.gov.br/api/operations-list/spatial-operation-interface-list"]
    dic[MultiPointField] = ["http://ggt-des.ibge.gov.br/api/operations-list/spatial-operation-interface-list"]
    dic[MultiPoint] = ["http://ggt-des.ibge.gov.br/api/operations-list/spatial-operation-interface-list"]
    dic[LineStringField] = ["http://ggt-des.ibge.gov.br/api/operations-list/spatial-operation-interface-list"]
    dic[LineString] = ["http://ggt-des.ibge.gov.br/api/operations-list/spatial-operation-interface-list"]
    dic[MultiLineStringField] = ["http://ggt-des.ibge.gov.br/api/operations-list/spatial-operation-interface-list"]
    dic[MultiLineString] = ["http://ggt-des.ibge.gov.br/api/operations-list/spatial-operation-interface-list"]
    dic[PolygonField] = ["http://ggt-des.ibge.gov.br/api/operations-list/spatial-operation-interface-list"]
    dic[Polygon] = ["http://ggt-des.ibge.gov.br/api/operations-list/spatial-operation-interface-list"]
    dic[MultiPolygonField] = ["http://ggt-des.ibge.gov.br/api/operations-list/spatial-operation-interface-list"]
    dic[MultiPolygon] = ["http://ggt-des.ibge.gov.br/api/operations-list/spatial-operation-interface-list"]

    return dic

def mediaTypeDict():
    dicti = {}
    geometric_media_types = [CONTENT_TYPE_GEOJSON, CONTENT_TYPE_OCTET_STREAM, CONTENT_TYPE_IMAGE_PNG]
    dicti[GeometryField] = geometric_media_types
    dicti[GEOSGeometry] = geometric_media_types
    dicti[GEOSGeometry] = geometric_media_types
    dicti[FeatureCollection] = geometric_media_types
    dicti['Feature'] = geometric_media_types
    dicti[FeatureModel] = geometric_media_types
    return dicti

def vocabulary(a_key):
    return vocabularyDict()[a_key] if a_key in vocabularyDict() else None

def operation_vocabulary(a_key):
    return OperationVocabularyDict()[a_key] if a_key in OperationVocabularyDict() else None

def media_type_for_resource_type(resource_type):
    return mediaTypeDict()[resource_type] if resource_type in mediaTypeDict() else None


class SupportedProperty():
    def __init__(self, field):
        self.property_name = field.name

        if field.primary_key:
            self.required = False
        else:
            if field.default == NOT_PROVIDED:
                self.required = not field.null # if is null, is not required
            else:
                self.required = False # if has default value, is not required

        self.readable = True
        self.writeable = True
        self.is_unique = field.unique
        self.is_identifier = field.primary_key
        self.is_external = isinstance(field, ForeignKey)
        self.field = field

    def get_supported_operations(self):
        voc = operation_vocabulary(self.field.name) if operation_vocabulary(self.field.name) is not None else operation_vocabulary( type(self.field) )

        if voc is None:
            voc  = []

        oper_res_voc_dict_list = [{"hydra:Link": voc}]
        return oper_res_voc_dict_list

    def context(self):
        return {
            "@type": "hydra:SupportedProperty",
            "hydra:property": self.property_name,
            "hydra:writeable": self.writeable,
            "hydra:readable": self.readable,
            "hydra:required": self.required,
            "isUnique": self.is_unique,
            "isIdentifier": self.is_identifier,
            "isExternal": self.is_external,
            "hydra:supportedOperations": self.get_supported_operations()
        }

class SupportedOperation():
    def __init__(self, operation='', title='', method='', expects=[] , returns='', type='', link='', description=''):
        self.method = method
        self.operation = operation
        self.title = title
        self.expects = expects
        self.returns = returns
        self.type = type
        self.link = link # the link to the explanation of what this operation is
        self.description = description

    def context(self):
        return {
                "hydra:method": self.method,
                "hydra:operation": self.operation,
                "hydra:expects": self.expects,
                "hydra:returns": self.returns,
                "hydra:statusCode": '',
                "@id": self.link,
                #'@type': self.type,
                "hydra:description": self.description
        }

class SupportedOperator():
    def __init__(self, operator='', expects='', returns='', link=''):
        self.operator = operator
        self.expects = expects
        self.returns = returns
        self.link = link

    def context(self):
        return {
            "operator": self.operator,
            "expects": self.expects,
            "returns": self.returns,
            "@id": self.link
        }

def initialize_dict():
    dict = {}
    oc = BaseOperationController()
    dict[GeometryField] = oc.geometry_operations_dict()
    dict['Feature'] = oc.geometry_operations_dict()
    dict[FeatureModel] = oc.geometry_operations_dict()
    dict['Geobuf'] = oc.geometry_operations_dict()
    dict[GEOSGeometry] = oc.geometry_operations_dict()
    dict['Image'] = oc.geometry_operations_dict()
    dict[Point] = oc.point_operations_dict()
    dict[PointField] = oc.point_operations_dict()
    dict[Polygon] = oc.polygon_operations_dict()
    dict[LineString] = oc.line_operations_dict()
    dict[MultiPoint] = oc.point_operations_dict()
    dict[MultiPolygon] = oc.polygon_operations_dict()
    dict[MultiLineString] = oc.line_operations_dict()
    dict[str] = oc.string_operations_dict()
    dict['Text'] = oc.string_operations_dict()
    dict[CharField] = oc.string_operations_dict()
    dict['Thing'] = oc.generic_object_operations_dict()
    dict[object] = oc.generic_object_operations_dict()

    ro = RasterOperationController()
    dict['Raster'] = ro.dict_all_operation_dict()
    dict['Tiff'] = ro.dict_all_operation_dict()
    dict[GDALRaster] = ro.dict_all_operation_dict()

    soc = SpatialCollectionOperationController()
    dict[GeometryCollection] = soc.feature_collection_operations_dict()
    dict['FeatureCollection'] = soc.feature_collection_operations_dict()
    dict[FeatureCollection] = soc.feature_collection_operations_dict()
    dict['GeobufCollection'] = soc.feature_collection_operations_dict()

    coc = CollectionResourceOperationController()
    dict['Collection'] = coc.collection_operations_dict()

    epoc = EntryPointResourceOperationController()
    dict['EntryPoint'] = epoc.collection_operations_dict()
    return dict

class ContextResource:

    def __init__(self):
        self.basic_path = None
        self.complement_path = None
        self.host = None
        self.dict_context = None
        self.resource = None

    def get_dict_context(self):
        '''use this method instead of reference self.dict_context directly'''
        return deepcopy(self.dict_context)

    #def attribute_name_list(self):
    #    return ( field.attname for field in self.model_class._meta.fields[:])

    #def attribute_type_list(self):
    #    return ( type(field) for field in self.model_class._meta.fields[:])

    def host_with_path(self):
        return self.host + self.basic_path + "/" + self.complement_path

    def operation_names(self):
        return [method for method in dir(self) if callable(getattr(self, method)) and self.is_not_private(method)]

    def resource_id_and_type_by_operation_dict(self, operation_return_type):
        '''
        Used as resource identification and typing
        '''
        dic = {
            self.resource.operation_controller.projection_operation_name: {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
        }
        return dic

    def resource_description_type_by_content_type_dict(self):
        return {
            CONTENT_TYPE_OCTET_STREAM:  "https://schema.org/Thing",
            CONTENT_TYPE_IMAGE_PNG:     "https://schema.org/ImageObject"
        }

    # todo: currently there is no way to specificaly determine @id for a resource that is a result of an operation, therefore we define it generically based on operation return type
    def resource_description_id_by_return_type_dict(self):
        return {
            object: "https://schema.org/Thing",
            float:  "https://schema.org/Float",
            int:    "https://schema.org/Integer",
            bool:   "https://schema.org/Boolean",
            str:    "https://schema.org/Text"
        }

    def get_resource_description_id(self, return_type):
        if return_type in self.resource_description_id_by_return_type_dict():
            return { "@id": self.resource_description_id_by_return_type_dict()[return_type]}
        return {"@id": "https://schema.org/Thing"}

    def get_resource_description_type(self, content_type):
        if content_type in self.resource_description_type_by_content_type_dict():
            return { "@type": self.resource_description_type_by_content_type_dict()[content_type]}
        return {"@type": "https://schema.org/Thing"}

    def attributes_term_definition_context_dict(self, attrs_list):
        dic_field = {}
        fields = self.resource.fields_to_web_for_attribute_names(attrs_list)
        for field_model in fields:
            dic_field[field_model.name] = self.attribute_contextualized_dict_for_field(field_model)
        dic_field.update(self.get_subClassOf_term_definition())
        return dic_field

    def operation_term_definition_context_dict(self):
        '''
        Used as term definition inside @context. it's important to remember that some operations
        don't have term definition because his name don'r appear in resource body
        '''
        dic = {}
        return dic

    def resource_id_and_type_by_operation_context(self, a_key, operation_return_type):
        if a_key in self.resource_id_and_type_by_operation_dict(operation_return_type):
            return self.resource_id_and_type_by_operation_dict(operation_return_type)[a_key]
        else:
            return None

    def operation_term_definition_context(self, a_key, operation_return_type=None):
        if a_key in self.operation_term_definition_context_dict():
            return self.operation_term_definition_context_dict()[a_key]
        return {"@id": vocabulary(object), "@type": vocabulary(object)}

    def attribute_contextualized_dict_for_field(self, field):
        voc = vocabulary(field.name)

        voc_type = vocabulary(type(field))

        res_voc = voc if voc is not None else voc_type

        if res_voc is None:
            res_voc  = vocabulary(object)
        return {
            '@id': res_voc,
            '@type':  ("@id" if isinstance(field, ForeignKey) else voc_type)
        }

    def attribute_contextualized_dict_for_type(self, a_type):
        res_voc = vocabulary(a_type)
        return {
            '@id': res_voc,
            '@type':  ("@id" if a_type == ForeignKey else res_voc)
        }

    def get_vocabulary_for(self, key):
        return vocabulary(key)

    def get_subClassOf_term_definition(self):
        dicti = {
            "subClassOf": {
                "@id": "rdfs:subClassOf", "@type": "@vocab"
            },
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
        }
        dicti.update(self.get_hydra_term_definition())
        return dicti

    def available_formats_term_definition(self):
        dicti = {
            "availableFormats": {
                "@id": "https://schema.org/domainIncludes",
                "@container": "@set"
            },
            "format": "https://schema.org/encodingFormat"
        }
        return dicti

    def get_hydra_term_definition(self):
        return {"hydra": vocabulary("hydra")}

    def attributes_contextualized_dict(self):
        dic_field = {}
        fields = self.resource.fields_to_web()
        for field_model in fields:
            dic_field[field_model.name] = self.attribute_contextualized_dict_for_field(field_model)
        dic_field.update(self.get_subClassOf_term_definition())
        #dic_field.update(self.available_formats_term_definition()) #todo: future hypermidia control
        return dic_field

    def selectedAttributeContextualized_dict(self, attribute_name_array):
        return {k: v for k, v in list(self.attributes_contextualized_dict().items()) if k in attribute_name_array}

    def supportedPropertyFor(self, field):
        voc = vocabulary(field.name)
        res_voc = voc if voc is not None else vocabulary(type(field))
        return { "@id": res_voc, "@type": "@id"}

    def identifier_field_or_None(self):
        fields = self.resource.fields_to_web()
        for field in fields:
             if field.primary_key is True:
                 return field
        return None

    def representationName(self):
        ide_field = self.identifier_field_or_None()
        if ide_field is not None:
            return  {"hydra:property":ide_field.name , "@type": "hydra:SupportedProperty"}
        return {}

    def supportedProperties(self, attribute_names=None):
        if self.resource is None:
            return []

        fields = self.resource.fields_to_web() if attribute_names is None else self.resource.fields_to_web_for_attribute_names(attribute_names)

        arr_dict = []
        for field in fields:
            arr_dict.append(
                SupportedProperty(field)
            )
        return [supportedAttribute.context() for supportedAttribute in arr_dict]

    def supportedOperationsFor(self, object, object_type=None):
        dict = initialize_dict()
        a_type = object_type or type(object)
        dict_operations = dict[a_type] if a_type in dict else {}

        arr = []
        for k, v_typed_called in dict_operations.items():

            exps = []
            if v_typed_called.has_parameters:
                for parameter, representation_list in v_typed_called.get_parameters_and_representations():
                    representation_voc_list = [vocabulary(representation) for representation in representation_list]
                    exps.append({
                        "parameter": vocabulary(parameter),
                        "represantations": representation_voc_list
                    })

            rets = vocabulary(v_typed_called.return_type) if v_typed_called.return_type in vocabularyDict() else "NOT FOUND"
            link_id = vocabulary(v_typed_called.name)
            arr.append(SupportedOperation(operation=k,
                                          title=v_typed_called.name,
                                          method='GET',
                                          expects=exps,
                                          returns=rets,
                                          type='',
                                          link=link_id,
                                          description=v_typed_called.get_operation_description())
                       )

        return [supportedOperation.context() for supportedOperation in arr]

    def iriTemplates(self):
        iri_templates = []
        dict = {}
        dict["@type"] = "IriTemplate"
        dict["template"] = self.host_with_path() + "{list*}"  # Ex.: http://host/unidades-federativas/nome,sigla,geom
        dict["mapping"] = [ {"@type": "iriTemplateMapping", "variable": "list*", "property": "hydra:property", "required": True}]

        iri_templates.append(dict)
        return {"iri_templates": iri_templates}

    def get_default_context_superclass(self):
        return {"subClassOf": "hydra:Resource"}

    def get_context_superclass_by_return_type(self, return_type):
        return {"subClassOf": "hydra:Resource"}

    def get_default_resource_type_identification(self):
        dicti = {}
        dicti["@id"] = self.get_default_resource_id_vocabulary()
        dicti["@type"] = self.get_default_resource_type_vocabulary()
        return dicti

    def get_default_resource_id_vocabulary(self):
        id_vocabulary = vocabulary(self.resource.default_resource_type())
        return id_vocabulary if id_vocabulary is not None else vocabulary(object)

    def get_default_resource_type_vocabulary(self):
        type_vocabulary = vocabulary(self.resource.default_resource_type())
        return type_vocabulary if type_vocabulary is not None else vocabulary(object)

    def get_resource_id_and_type_by_attributes_return_type(self, attr_list, return_type):
        dicti = {}
        dicti["@id"] = self.get_resource_id_by_attributes_return_type(attr_list, return_type)
        dicti["@type"] = vocabulary(return_type)
        dicti.update( self.get_context_superclass_by_attributes(attr_list) )
        return dicti

    def get_resource_id_by_attributes_return_type(self, attr_list, return_type):
        if len(attr_list) == 1:
            field_for_attribute = self.resource.field_for(attr_list[0])
            return vocabulary(field_for_attribute.name) if vocabulary(field_for_attribute.name) is not None else vocabulary(type(field_for_attribute))
        return vocabulary(object)

    def get_context_superclass_by_attributes(self, attr_list):
        return self.get_default_context_superclass()

    def get_operation_return_type_context_by_operation_name(self, operation_name):
        return self.get_operation_return_type_term_definition(operation_name)

    def get_resource_id_and_type_by_operation_return_type(self, operation_name, operation_return_type):
        dicti = self.resource_id_and_type_by_operation_context(operation_name, operation_return_type)
        dicti.update(self.get_default_context_superclass())
        return dicti

    def get_operation_return_type_term_definition(self, operation_name, operation_return_type=None):
        return {operation_name: self.operation_term_definition_context(operation_name)}

    def set_context_to_attributes(self, attributes_name):
        self.dict_context = {}
        self.dict_context["@context"] = self.selectedAttributeContextualized_dict(attributes_name)
        #self.dict_context["@context"]["hydra"] = "http://www.w3.org/ns/hydra/core#"
        self.dict_context["@context"].update(self.get_subClassOf_term_definition())

    def set_context_to_operation(self, object, operation_name):
        self.dict_context = {}
        dict = {}

        dict [operation_name] = { "@id": vocabulary(operation_name),"@type": "@id" }
        self.dict_context["@context"] = dict

    def get_context_to_operation(self, operation_name):
        dict = {}
        dict[operation_name] = { "@id": vocabulary(operation_name),"@type": "@id" }
        return {"@context": dict}

    def available_formats_for(self, resource_type):
        media_type_arr = media_type_for_resource_type(resource_type)
        dicti = {
            "availableFormats": []
        }
        for media_type in media_type_arr:
            dicti['availableFormats'].append({ "format": media_type })
        return dicti

    def initalize_context(self, resource_type):
        self.dict_context = {}
        self.dict_context["@context"] = self.attributes_contextualized_dict()
        self.dict_context["hydra:supportedProperties"] = self.supportedProperties()
        self.dict_context["hydra:supportedOperations"] = self.supportedOperationsFor(self.resource.object_model, resource_type)
        self.dict_context["hydra:representationName"] = self.representationName()
        self.dict_context["hydra:iriTemplate"] = self.iriTemplates()
        self.dict_context.update(self.get_default_context_superclass())
        self.dict_context.update(self.get_default_resource_type_identification())
        #self.dict_context.update(self.available_formats_for(resource_type)) #todo: future hypermidia control

        return deepcopy(self.dict_context)

    def context(self, resource_type=None):
        if self.dict_context is None:
            resource_type = resource_type if resource_type is not None else self.resource.default_resource_type()
            self.initalize_context(resource_type)
        return deepcopy(self.dict_context)

class FeatureResourceContext(ContextResource):

    def context_for_image(self):
        self.dict_context = {}
        self.dict_context["@context"] = self.get_subClassOf_term_definition()
        self.dict_context["hydra:supportedProperties"] = self.supportedProperties()
        self.dict_context["hydra:supportedOperations"] = self.supportedOperationsFor(self.resource.object_model, IMAGE_RESOURCE_TYPE)
        self.dict_context["hydra:representationName"] = self.representationName()
        self.dict_context["hydra:iriTemplate"] = self.iriTemplates()
        self.dict_context.update(self.get_default_context_superclass())
        self.dict_context.update(self.get_default_resource_type_identification())
        #self.dict_context.update( self.available_formats_for(FEATURE_RESOURCE_TYPE) )  # todo: future hypermidia control
        return deepcopy(self.dict_context)

    def resource_id_and_type_by_operation_dict(self, operation_return_type):
        dicti = super(FeatureResourceContext, self).resource_id_and_type_by_operation_dict(operation_return_type)
        dicti.update({
            self.resource.operation_controller.area_operation_name:             {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.buffer_operation_name:           {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.boundary_operation_name:         {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.centroid_operation_name:         {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.contains_operation_name:         {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.convex_hull_operation_name:      {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.coord_seq_operation_name:        {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.coords_operation_name:           {"@id": vocabulary(self.resource.operation_controller.coords_operation_name), "@type": vocabulary(object)},
            self.resource.operation_controller.count_operation_name:            {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.crosses_operation_name:          {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.crs_operation_name:              {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.difference_operation_name:       {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.dims_operation_name:             {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.disjoint_operation_name:         {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.distance_operation_name:         {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.empty_operation_name:            {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.envelope_operation_name:         {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.equals_exact_operation_name:     {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.equals_operation_name:           {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.ewkb_operation_name:             {"@id": vocabulary(GEOSGeometry), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.ewkt_operation_name:             {"@id": vocabulary(GEOSGeometry), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.extent_operation_name:           {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.geojson_operation_name:          {"@id": vocabulary(GEOSGeometry), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.geom_type_operation_name:        {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.geom_typeid_operation_name:      {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.has_cs_operation_name:           {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.hasz_operation_name:             {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.hex_operation_name:              {"@id": vocabulary(GEOSGeometry), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.hexewkb_operation_name:          {"@id": vocabulary(GEOSGeometry), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.intersection_operation_name:     {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.intersects_operation_name:       {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.json_operation_name:             {"@id": vocabulary(GEOSGeometry), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.kml_operation_name:              {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.length_operation_name:           {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.num_coords_operation_name:       {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.num_geom_operation_name:         {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.num_points_operation_name:       {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.ogr_operation_name:              {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.overlaps_operation_name:         {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.point_on_surface_operation_name: {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.relate_operation_name:           {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.relate_pattern_operation_name:   {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.ring_operation_name:             {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.simple_operation_name:           {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.simplify_operation_name:         {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.srid_operation_name:             {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.srs_operation_name:              {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.sym_difference_operation_name:   {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.touches_operation_name:          {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.transform_operation_name:        {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.union_operation_name:            {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.valid_operation_name:            {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.valid_reason_operation_name:     {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.within_operation_name:           {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.wkb_operation_name:              {"@id": vocabulary(GEOSGeometry), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.wkt_operation_name:              {"@id": vocabulary(GEOSGeometry), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.x_operation_name:                {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.y_operation_name:                {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.z_operation_name:                {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
        })
        return dicti

    def operation_term_definition_context_dict(self):
        dic = super(FeatureResourceContext, self).operation_term_definition_context_dict()
        dic.update({
            self.resource.operation_controller.area_operation_name:             {"@id": vocabulary(float), "@type": vocabulary(float)},
            self.resource.operation_controller.contains_operation_name:         {"@id": vocabulary(bool), "@type": vocabulary(bool)},
            self.resource.operation_controller.coords_operation_name:           {"@id": vocabulary(self.resource.operation_controller.coords_operation_name), "@type": vocabulary(self.resource.operation_controller.coords_operation_name)},
            self.resource.operation_controller.ewkt_operation_name:             {"@id": vocabulary(self.resource.operation_controller.ewkt_operation_name), "@type": vocabulary(str)},
            self.resource.operation_controller.geojson_operation_name:          {"@id": vocabulary(self.resource.operation_controller.geojson_operation_name), "@type": vocabulary(str)},
            self.resource.operation_controller.json_operation_name:             {"@id": vocabulary(self.resource.operation_controller.json_operation_name), "@type": vocabulary(str)},
            self.resource.operation_controller.ogr_operation_name:              {"@id": vocabulary(self.resource.operation_controller.ogr_operation_name), "@type": vocabulary(str)},
            self.resource.operation_controller.relate_pattern_operation_name:   {"@id": vocabulary(bool), "@type": vocabulary(bool)},
            self.resource.operation_controller.relate_operation_name:           {"@id": vocabulary(str), "@type": vocabulary(str)},
            self.resource.operation_controller.wkt_operation_name:              {"@id": vocabulary(self.resource.operation_controller.wkt_operation_name), "@type": vocabulary(str)},

        })
        return dic

    def get_resource_id_and_type_by_operation_return_type(self, operation_name, operation_return_type):
        if not issubclass(operation_return_type, GEOSGeometry):
            return super(FeatureResourceContext, self).get_resource_id_and_type_by_operation_return_type(operation_name, operation_return_type)
        dicti = {}
        dicti["@id"] = vocabulary(operation_return_type)
        dicti["@type"] = vocabulary(operation_return_type)
        dicti.update(self.get_default_context_superclass())
        return dicti

    def get_resource_id_and_type_by_attributes_return_type(self, attr_list, return_type):
        id_and_type_voc = super(FeatureResourceContext, self).get_resource_id_and_type_by_attributes_return_type(attr_list, return_type)
        if self.resource.geometry_field_name() not in attr_list:
            return id_and_type_voc
        id_and_type_voc["@type"] = vocabulary(return_type)
        return id_and_type_voc

    def get_resource_id_by_attributes_return_type(self, attr_list, return_type):
        if self.resource.geometry_field_name() not in attr_list:
            return super(FeatureResourceContext, self).get_resource_id_by_attributes_return_type(attr_list, return_type)
        return vocabulary(return_type)

    def attributes_contextualized_dict(self):
        dict_field = super(FeatureResourceContext, self).attributes_contextualized_dict()
        dict_field.pop(self.resource.geometry_field_name())
        return dict_field

    def get_supported_operations_for(self, operation_return_type):
        operations_dicts_list = self.resource.operation_controller.supported_operations_for(operation_return_type)
        if len(operations_dicts_list) == 0:
            return { HYPER_RESOURCE_SUPPORTED_OPERATIONS_LABEL: [] }

        supported_operations_arr = []
        for operation_name, type_called in operations_dicts_list.items():
            exps = []
            if type_called.has_parameters():
                for parameter, representation_list in type_called.get_parameters_and_representations():
                    representation_voc_list = [vocabulary(representation) for representation in representation_list]
                    exps.append( {"parameter": vocabulary(parameter), "represantations": representation_voc_list} )

            rets = vocabulary(type_called.return_type) if type_called.return_type in vocabularyDict() else "NOT FOUND"
            link_id = vocabulary(type_called.name)
            supported_operations_arr.append(SupportedOperation(operation=operation_name,
                                          title=type_called.name,
                                          method='GET',
                                          expects=exps,
                                          returns=rets,
                                          type='',
                                          link=link_id,
                                          description=type_called.get_operation_description())
                       )

        return {
            HYPER_RESOURCE_SUPPORTED_OPERATIONS_LABEL: [supportedOperation.context() for supportedOperation in supported_operations_arr]
        }

    def term_definition_operation_return_type(self, operation_return_type):
        return {
                self.resource.operation_controller.last_operation_name: {
                    "@id": "https://schema.org/value",
                    "@type": vocabulary(operation_return_type),
                }
            }

    def resource_description_id_by_return_type_dict(self):
        ''' Defines @id by response return type '''
        d = super(FeatureResourceContext, self).resource_description_id_by_return_type_dict()
        d.update({
            GEOSGeometry:   "https://purl.org/geojson/vocab#geometry"
        })
        return d

    def resource_description_type_by_content_type_dict(self):
        ''' Defines @type by response content-type '''
        d = super(FeatureResourceContext, self).resource_description_type_by_content_type_dict()
        d.update({
            CONTENT_TYPE_GEOJSON:   "https://purl.org/geojson/vocab#geometry", # todo: maybe 'https://schema.org/GeospatialGeometry' could add more semantics
        })
        return d

    def get_resource_description_type(self, content_type):
        if content_type == CONTENT_TYPE_GEOJSON:
            last_operation_retype = self.resource.operation_controller.operations_dict()[self.resource.operation_controller.last_operation_name].return_type
            if last_operation_retype == GEOSGeometry: # too generic
                return super(FeatureResourceContext, self).get_resource_description_type(content_type)
            return {"@type": vocabulary(last_operation_retype)}
        return super(FeatureResourceContext, self).get_resource_description_type(content_type)

    def context_for_operation(self, operation_return_type, response_content_type):
        term_definition_dict = {}
        term_definition_dict.update(self.get_hydra_term_definition())
        term_definition_dict.update(self.get_subClassOf_term_definition())

        if not issubclass(operation_return_type, GEOSGeometry) and operation_return_type != bytes:
            term_definition_dict.update(self.term_definition_operation_return_type(operation_return_type))
        context_dict = {"@context": term_definition_dict}

        context_dict.update(self.get_supported_operations_for(operation_return_type))
        context_dict.update(self.get_context_superclass_by_return_type(operation_return_type))

        #context_dict.update(self.get_resource_description_id(operation_return_type))
        context_dict.update( {"@id": self.resource_id_and_type_by_operation_dict(operation_return_type)[self.resource.operation_controller.last_operation_name]["@id"] } )
        context_dict.update(self.get_resource_description_type(response_content_type))
        return context_dict

class AbstractCollectionResourceContext(ContextResource):

    def resource_id_and_type_by_operation_dict(self, operation_return_type):
        dicti = super(AbstractCollectionResourceContext, self).resource_id_and_type_by_operation_dict(operation_return_type)
        dicti.update({
            self.resource.operation_controller.count_resource_collection_operation_name:    {"@id": "hydra:totalItems", "@type": "https://schema.org/Thing"},
            # For operations with subcollection return, @type is to much generic, therefore this @type must be based on operation return type defined in resource class (views)
            self.resource.operation_controller.distinct_collection_operation_name:          {"@id": self.get_default_resource_id_vocabulary(), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.filter_collection_operation_name:            {"@id": self.get_default_resource_id_vocabulary(), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.group_by_sum_collection_operation_name:      {"@id": self.get_default_resource_id_vocabulary(), "@type": vocabulary(operation_return_type)},
        })
        return dicti

    def operation_term_definition_context_dict(self):
        dic = super(AbstractCollectionResourceContext, self).operation_term_definition_context_dict()
        dic.update({
            self.resource.operation_controller.count_resource_collection_operation_name:    {"@id": "https://schema.org/Integer", "@type": "https://schema.org/Integer"},
            self.resource.operation_controller.group_by_sum_collection_operation_name:      {"@id": vocabulary(GROUP_BY_SUM_PROPERTY_NAME), "@type": vocabulary(GROUP_BY_SUM_PROPERTY_NAME)}
        })
        return dic

    def get_default_context_superclass(self):
        return {"subClassOf": "hydra:Resource"}

    def get_default_resource_id_vocabulary(self):
        return vocabulary(object)

    '''
    def get_resource_id_and_type_by_attributes_return_type(self, attr_list, return_type):
        dicti = {}
        dicti["@id"] = vocabulary(object)
        dicti["@type"] = vocabulary(return_type)
        dicti.update(self.get_context_superclass_by_attributes(attr_list))
        return dicti
    '''

    def get_resource_id_and_type_by_operation_return_type(self, operation_name, operation_return_type):
        dicti = self.get_context_superclass_by_return_type(operation_return_type)

        operation_id_type = self.resource_id_and_type_by_operation_context(operation_name, operation_return_type)
        if operation_id_type:
            dicti.update(operation_id_type)
        else:
            dicti.update(
                {"@id": vocabulary(object), "@type": vocabulary(operation_return_type)}
            )
        return dicti

    def get_resource_id_by_attributes(self, attr_list):
        '''
        For Collection @id represents the identification of each element in collection and not the collection itself
        '''
        if len(attr_list) > 1:
            return vocabulary(object)

        field_for_attribute = self.resource.field_for(attr_list[0])
        return vocabulary(field_for_attribute.name) if vocabulary(field_for_attribute.name) is not None else vocabulary(type(field_for_attribute))

class FeatureCollectionResourceContext(AbstractCollectionResourceContext):

    def resource_id_and_type_by_operation_dict(self, operation_return_type):
        dicti = super(FeatureCollectionResourceContext, self).resource_id_and_type_by_operation_dict(operation_return_type)
        dicti.update({
            self.resource.operation_controller.extent_collection_operation_name:    {"@id": vocabulary(operation_return_type), "@type": "https://schema.org/Thing"},
            self.resource.operation_controller.make_line_collection_operation_name: {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.union_collection_operation_name:     {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
            self.resource.operation_controller.envelope_collection_operation_name:  {"@id": vocabulary(operation_return_type), "@type": vocabulary(operation_return_type)},
        })
        return dicti

    def operation_term_definition_context_dict(self):
        dic = super(FeatureCollectionResourceContext, self).operation_term_definition_context_dict()
        dic.update({
            self.resource.operation_controller.extent_collection_operation_name:    {"@id": vocabulary(list), "@type": vocabulary(list)}
        })
        return dic

    def get_default_context_superclass(self):
        return {"subClassOf": vocabulary("Collection")}

    def get_context_superclass_by_return_type(self, return_type):
        if return_type not in [GeometryCollection, FeatureCollection]:
            return super(FeatureCollectionResourceContext, self).get_context_superclass_by_return_type(return_type)
        return self.get_default_context_superclass()

    def get_default_resource_id_vocabulary(self):
        return vocabulary("Feature")

    def get_context_superclass_by_attributes(self, attr_list):
        if self.resource.geometry_field_name() not in attr_list:
            return super(FeatureCollectionResourceContext, self).get_default_context_superclass()
        return self.get_default_context_superclass()

    def get_resource_id_and_type_by_attributes_return_type(self, attr_list, return_type):
        dicti = {}
        dicti["@id"] = self.get_resource_id_by_attributes(attr_list)
        dicti["@type"] = vocabulary(return_type)
        dicti.update( self.get_context_superclass_by_attributes(attr_list) )
        return dicti

    def attributes_contextualized_dict(self):
        dict_field = super(FeatureCollectionResourceContext, self).attributes_contextualized_dict()
        dict_field.pop(self.resource.geometry_field_name())
        return dict_field

    def get_resource_id_by_attributes(self, attr_list):
        if self.resource.geometry_field_name() not in attr_list:
            return super(FeatureCollectionResourceContext, self).get_resource_id_by_attributes(attr_list)
        if len(attr_list) > 1:
            return vocabulary("Feature")

        return vocabulary( type(self.resource.field_for(attr_list[0])) )

    def get_resource_id_and_type_by_operation_return_type(self, operation_name, operation_return_type):
        #if type(operation_return_type) == str or not issubclass(operation_return_type, GEOSGeometry):
        #    return super(FeatureCollectionResourceContext, self).get_resource_id_and_type_by_operation_return_type(operation_name, operation_return_type)
        dicti = self.get_context_superclass_by_return_type(operation_return_type)
        operation_id_type = self.resource_id_and_type_by_operation_context(operation_name, operation_return_type)
        if operation_id_type:
            dicti.update(operation_id_type)
        else:
            dicti.update(
                {"@id": self.get_default_resource_id_vocabulary(), "@type": vocabulary(operation_return_type)}
            )
        return dicti

class NonSpatialResourceContext(ContextResource):
    pass

class RasterResourceContext(ContextResource):

    def get_resource_id_by_attributes_return_type(self, attr_list, return_type):
        if len(attr_list) == 1:
            return super(RasterResourceContext, self).get_resource_id_by_attributes_return_type(attr_list, return_type)
        return vocabulary(return_type)

    def resource_id_and_type_by_operation_dict(self, operation_return_type):
        dicti = super(RasterResourceContext, self).resource_id_and_type_by_operation_dict(operation_return_type)
        dicti.update({
            self.resource.operation_controller.driver_operation_name: {"@id": "https://schema.org/Text", "@type": "https://schema.org/Thing"}
        })
        return dicti

    def attributes_term_definition_context_dict(self, attrs_list):
        if self.resource.spatial_field_name() in attrs_list:
            return self.attributes_contextualized_dict()
        return super(RasterResourceContext, self).attributes_term_definition_context_dict(attrs_list)

    def operation_term_definition_context_dict(self):
        dic = super(RasterResourceContext, self).operation_term_definition_context_dict()
        dic.update({
            self.resource.operation_controller.driver_operation_name: {"@id": "https://schema.org/Text", "@type": "https://schema.org/Text"}
        })
        return dic

    def attributes_contextualized_dict(self):
        return self.get_subClassOf_term_definition()

    def get_resource_id_and_type_by_operation_return_type(self, operation_name, operation_return_type):
        if not issubclass(operation_return_type, GDALRaster):
            return super(RasterResourceContext, self).get_resource_id_and_type_by_operation_return_type(operation_name, operation_return_type)
        dicti = self.get_default_context_superclass()
        dicti["@id"] = vocabulary(operation_return_type)
        dicti["@type"] = vocabulary(operation_return_type)
        return dicti

    def get_resource_id_and_type_by_attributes_return_type(self, attr_list, return_type):
        dicti = {}
        dicti["@id"] = self.get_resource_id_by_attributes_return_type(attr_list, return_type)
        dicti["@type"] = vocabulary(return_type)
        dicti.update( self.get_context_superclass_by_attributes(attr_list) )
        return dicti

class EntryPointResourceContext(AbstractCollectionResourceContext):

    def resource_id_and_type_by_operation_dict(self, operation_return_type):
        dicti = super(AbstractCollectionResourceContext, self).resource_id_and_type_by_operation_dict(operation_return_type)
        dicti.update({
            self.resource.operation_controller.count_resource_collection_operation_name: {"@id": "hydra:totalItems", "@type": "https://schema.org/Thing"},
        })
        return dicti

    def operation_term_definition_context_dict(self):
        dic = super(AbstractCollectionResourceContext, self).operation_term_definition_context_dict()
        dic.update({
            self.resource.operation_controller.count_resource_collection_operation_name: {"@id": "https://schema.org/Integer", "@type": "https://schema.org/Integer"}
        })
        return dic

    def get_default_resource_id_vocabulary(self):
        return vocabulary('Link')

    def attributes_contextualized_dict(self):
        default_attrs_context_dict = super(EntryPointResourceContext, self).attributes_contextualized_dict()
        for field in self.resource.fields_to_web():
            default_attrs_context_dict[field.name]["@type"] = "@id"
            default_attrs_context_dict[field.name]["@id"] = "https://schema.org/Thing"
        return default_attrs_context_dict

    def addContext(self, request, response):
        return self.createLinkOfContext(request, response)

    def createLinkOfContext(self, request, response, properties=None):
        # if properties is None:
        #     url = reverse('context:detail', args=[self.contextclassname], request=request)
        # else:
        #     url = reverse('context:detail-property', args=[self.contextclassname, ",".join(properties)], request=request)

        url = request.build_absolute_uri()
        url = url if url[-1] != '/' else url[:-1]
        url = url + HYPER_RESOURCE_EXTENSION

        context_link = ' <'+url+'>; rel="' + HYPER_RESOURCE_CONTEXT + '"; type="' + HYPER_RESOURCE_CONTENT_TYPE + '"'
        if "Link" not in response:
            response['Link'] = context_link
        else:
            response['Link'] += "," + context_link

        return response

    def create_context_as_dict(self, dict_of_name_link):
        a_context = {}
        dicti = {"@context": a_context}
        for key in dict_of_name_link.keys():
            a_context[key] = {"@id": "https://schema.org/Thing", "@type": "@id" }

        return dicti

class FeatureEntryPointResourceContext(EntryPointResourceContext):

    def attributes_contextualized_dict(self):
        default_attrs_context_dict = super(FeatureEntryPointResourceContext, self).attributes_contextualized_dict()
        for field in self.resource.fields_to_web():
            default_attrs_context_dict[field.name]["@type"] = "@id"
            default_attrs_context_dict[field.name]["@id"] = "https://purl.org/geojson/vocab#FeatureCollection"
        return default_attrs_context_dict

    def create_context_as_dict(self, dict_of_name_link):
        a_context = {}
        dicti = {"@context": a_context}
        for key in dict_of_name_link.keys():
            a_context[key] = {"@id": "https://purl.org/geojson/vocab#FeatureCollection", "@type": "@id" }

        return dicti

class RasterEntryPointResourceContext(EntryPointResourceContext):
    pass

class NonSpatialEntryPointResourceContext(EntryPointResourceContext):
    pass


class AbstractResourceContext(ContextResource):
    pass

class CollectionResourceContext(ContextResource):
    pass

class SpatialCollectionResourceContext(ContextResource):
    pass

class SpatialResourceContext(ContextResource):
    pass

class StyleResourceContext(ContextResource):
    pass

class TiffResourceContext(ContextResource):
    pass

class ProxiedNonSpatialResourceContext(ContextResource):
    pass