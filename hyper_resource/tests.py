import django
import rest_framework
#from rest_framework import generics
#from rest_framework.response import Response
#from rest_framework.views import APIView
#from rest_framework import permissions
#from rest_framework import permissions

from django.contrib.gis.geos import Point
from django.test import TestCase
# Create your tests here.
from django.contrib.gis.db import models

from hyper_resource.models import FeatureModel, FactoryComplexQuery
from hyper_resource.contexts import *
from hyper_resource.views import AbstractResource, FeatureCollectionResource, AbstractCollectionResource
from django.contrib.gis.geos import GEOSGeometry
from django.test import SimpleTestCase

import json
import requests
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


from django.test.runner import DiscoverRunner
#import os
#os.environ['DJANGO_SETTINGS_MODULE'] = 'bc_edgv.settings'
#django.setup()
#python manage.py test bcim.test_utils  --testrunner=bcim.test_utils.NoDbTestRunner
#python manage.py test hyper_resource.tests --testrunner=hyper_resource.tests.NoDbTestRunner
from django.contrib.gis.db.models import Q
class NoDbTestRunner(DiscoverRunner):
   """ A test runner to test without database creation/deletion """

   def setup_databases(self, **kwargs):
     pass

   def teardown_databases(self, old_config, **kwargs):
     pass

class Ponto(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    geom = models.PointField(blank=True, null=True)
class Linha(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    geom = models.LineStringField(blank=True, null=True)
class Poligono(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    geom = models.PolygonField(blank=True, null=True)
class Geometria(FeatureModel):
    id_objeto = models.IntegerField(primary_key=True)
    geom = models.GeometryField(blank=True, null=True)

## ativando virtual environment em: source ~/desenv/env/env_bc_edgv/bin/activate
## Testando
# python manage.py test hyper_resource.tests  --testrunner=hyper_resource.tests.NoDbTestRunner
##
#python manage.py test bcim.test_utils  --testrunner=bcim.test_utils.NoDbTestRunner
#python manage.py test hyper_resource.tests --testrunner=hyper_resource.tests.NoDbTestRunner
from django.test import SimpleTestCase
#from bcim.utils import APIViewHypermedia
#python manage.py test app --testrunner=app.filename.NoDbTestRunner
#python manage.py test bcim.tests  --testrunner=bcim.tests.NoDbTestRunner
#python manage.py test hyper_resource.tests --testrunner=hyper_resource.tests.NoDbTestRunner
from bcim.models import ModeloTeste

class ModelTest(models.Model):
    id_objeto = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nomeabrev = models.CharField(max_length=50, blank=True, null=True)
    geometriaaproximada = models.CharField(max_length=3, blank=True, null=True)
    operacional = models.CharField(max_length=12, blank=True, null=True)
    situacaofisica = models.TextField(blank=True, null=True)
    tipopostofisc = models.CharField(max_length=22, blank=True, null=True)
    geometry = models.GeometryField(blank=True, null=True)
    polygon = models.PolygonField(blank=True, null=True)
    lineString = models.LineStringField(blank=True, null=True)
    point = models.PointField(blank=True, null=True)
    multipolygon = models.MultiPolygonField(blank=True, null=True)

class TesteResource(AbstractResource):
    def __init__(self, a_name, params, answer):
        self.name = a_name
        self.parameters = params
        self.return_type = answer

class FeatureModelTestCase(SimpleTestCase):
    def setUp(self):
        self.ponto = Ponto()
        self.linha = Linha()
        self.poligono = Poligono()
        self.geometria = Geometria()

    def url_feature(self):
        return ''

    def test_get_geometry_type(self):
        self.assertEquals(self.ponto.get_geometry_type(), Point)

    def test_fields(self):
        self.assertEquals(self.ponto.fields()[0].name, 'id_objeto')

class AbstractResourceTestCase(SimpleTestCase):

    def setUp(self):
        self.tr = TesteResource('name', 'parameters', 'answer')
        self.ar = AbstractCollectionResource()

    def test_attributes(self):
        pass
    def test_operations(self):
        pass
    def test_remove_last_slash(self):

        self.assertEquals(self.ar.remove_last_slash('within/__tokenurl__1/collect/geom/buffer/0.2/'), 'within/__tokenurl__1/collect/geom/buffer/0.2')
        self.assertEquals(self.ar.remove_last_slash('within/__tokenurl__1/collect/geom/buffer/0.2'), 'within/__tokenurl__1/collect/geom/buffer/0.2')
        self.assertEquals(self.ar.remove_last_slash('within/__tokenurl__1/collect/geom/buffer/0.2 '), 'within/__tokenurl__1/collect/geom/buffer/0.2')

    def test_attribute_functions_str_splitted_by_slash(self):
        res = self.ar.attribute_functions_str_splitted_by_slash('within/http://172.30.10.86:8000/ibge/bcim/municipios/3159407/*collect/geom/buffer/0.2/intersects/https://172.30.10.86:8000/instituicoes/bcim/estado/rj/*')
        self.assertEquals(res[0], 'within')
        self.assertEquals(res[1], 'http://172.30.10.86:8000/ibge/bcim/municipios/3159407/')
        self.assertEquals(res[2], '*collect')
        self.assertEquals(res[3], 'geom')
        self.assertEquals(res[4], 'buffer')
        self.assertEquals(res[5], '0.2')
        self.assertEquals(res[6], 'intersects')
        self.assertEquals(res[7], 'https://172.30.10.86:8000/instituicoes/bcim/estado/rj/')

class SpatialResourceTest(SimpleTestCase):

    def test_attributeContextualized(self):
        pass

class FeatureResourceTest(SimpleTestCase):

    def test_basic_get(self):
        pass
    def test_options_url_without_parameters(self):
        pass
    def test_options_url_with_only_attributes(self):
        pass
    def test_options_url_with_only_one_attribute(self):
        pass
    def test_options_url_with_spatia_functions(self):
        pass

class FactoryComplexQueryTest(SimpleTestCase):
    def setUp(self):
        self.fcq = FactoryComplexQuery()
    def test_q_object_for_in(self):

        q = self.fcq.q_object_for_in(str,'sigla', ['ES,RJ'])
        self.assertEquals(Q(sigla__in=['ES,RJ']).__repr__(), q.__repr__())

    def test_q_object_for_eq(self):

        q = self.fcq.q_object_for_eq(str,'sigla', 'ES')
        self.assertEquals(Q(sigla='ES').__repr__(), q.__repr__())

    def test_q_object_for_neq(self):

        q = self.fcq.q_object_for_neq(str, 'sigla', 'ES')
        self.assertEquals((~Q(sigla='ES')).__repr__(), q.__repr__())

    def test_q_object_by_filter_operation(self):
        attribute_operation_str ='filter/sigla/in/rj,es,go/and/data/between/2017-02-01,2017-06-30/'
        import datetime
        start_date = datetime.date(2017, 2, 1)
        end_date = datetime.date(2017, 6, 30)
        q = Q(sigla__in=['rj','es','go']) & Q(data__range=(start_date, end_date))
        model_class = ModeloTeste
        self.fcq.q_object_serialized_by_filter_operation(attribute_operation_str, model_class)

class AbstractCollectionResourceTestCase(SimpleTestCase):
    def setUp(self):
        self.attributes_functions = ['filter/sigla/in/rj,es,go/', 'filter/sigla/uppercase/in/rj,es,go/and/data/between/2017-02-01,2017-06-30/', 'filter/sigla/in/rj,es,go/and/geom/within/{"type":"Polygon","coordinates":[[[-41.881710164667396,-21.297482165015307],[-28.840495695785098,-21.297482165015307],[-28.840495695785098,-17.886950999070834],[-41.881710164667396,-17.886950999070834],[-41.881710164667396,-21.297482165015307]]]}']
        self.acr = AbstractCollectionResource()

    def test_get_operation_name_from_path(self):
        self.assertEquals(self.acr.get_operation_name_from_path('collect/geom/buffer/0.2'), 'collect')
        self.assertEquals(self.acr.get_operation_name_from_path('filter/geom/buffer/0.2'), 'filter')
        self.assertEquals(self.acr.get_operation_name_from_path('filter/geom/containing/http://host/aldeias-indigenas/821/*collect/nome.geom/buffer/0.2'), 'filter_collect')
        self.assertEquals(self.acr.get_operation_name_from_path('collect/nome&geom/buffer/0.2/containing/http://host/aldeias-indigenas/821/*filter/nome/startswith/rio'), 'collect_filter')
        self.assertEquals(self.acr.get_operation_name_from_path('count_resource'), 'count_resource')
        self.assertEquals(self.acr.get_operation_name_from_path('group_by/nome'), 'group_by')
        self.assertEquals(self.acr.get_operation_name_from_path('group_by_count/nome'), 'group_by_count')
        self.assertEquals(self.acr.get_operation_name_from_path('distinct'), 'distinct')
        self.assertEquals(self.acr.get_operation_name_from_path('offset_limit/1&10'), 'offset_limit')
        self.assertEquals(self.acr.get_operation_name_from_path('nadahaver'), None)
    def test_attributes_functions_str_is_filter_with_spatial_operation(self):
        pass
        """
        self.assertTrue(self.acr.attributes_functions_str_is_filter_with_spatial_operation('filter/sigla/in/rj,es,go/and/geom/within/Point(1,2)'))
        self.assertFalse(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/filter'))
        self.assertFalse(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/filter/filter'))
        self.assertFalse(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/filter/ast/eq/ass/geom/within/asd'))
        self.assertFalse(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/filter/within/eq/asd'))
        self.assertTrue(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/filter/within/eq/geom/and/geom/within/asd'))
        self.assertFalse(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/filter/operacao/eq/within'))
        self.assertTrue(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/filter/eq/within/abxgeom'))
        self.assertFalse(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/filter/within/eq/abxx'))
        self.assertFalse(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/within/geom'))
        self.assertFalse(self.acr.attributes_functions_str_is_filter_with_spatial_operation('/within/filter'))
        """
    def test_attributes_functions_str_splitted_by_slash(self):
        self.acr.attribute_functions_str_splitted_by_slash('collect/geom/buffer/0.2') == ['collect','geom', 'buffer', '0.2']
        self.acr.attribute_functions_str_splitted_by_slash('collect/geom/buffer/0.2/') == ['collect','geom', 'buffer', '0.2']
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('collect/geom/buffer/0.2'), ['collect','geom', 'buffer', '0.2'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('collect/geom/buffer/0.2/transform/3005&True/area'), ['collect', 'geom', 'buffer', '0.2', 'transform', '3005&True', 'area'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('offsetLimit/1&10/collect/geom/buffer/0.2'), ['offsetLimit', '1&10', 'collect', 'geom', 'buffer', '0.2'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('within/{"type":"Polygon","coordinates":[[[-48.759514611370854,-28.3426735036349],[-48.631647133384185,-28.3426735036349],[-48.631647133384185,-28.082673631081306],[-48.759514611370854,-28.082673631081306],[-48.759514611370854,-28.3426735036349]]]}/collect/geom/buffer/0.2'), ['within', '{"type":"Polygon","coordinates":[[[-48.759514611370854,-28.3426735036349],[-48.631647133384185,-28.3426735036349],[-48.631647133384185,-28.082673631081306],[-48.759514611370854,-28.082673631081306],[-48.759514611370854,-28.3426735036349]]]}', 'collect', 'geom', 'buffer', '0.2'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('within/http://172.30.10.86:8000/instituicoes/ibge/bcim/municipios/3159407/*collect/geom/buffer/0.2/'), ['within', 'http://172.30.10.86:8000/instituicoes/ibge/bcim/municipios/3159407/', '*collect', 'geom', 'buffer', '0.2'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('within/https://172.30.10.86:8000/instituicoes/ibge/bcim/municipios/3159407/*collect/geom/buffer/0.2'), ['within', 'https://172.30.10.86:8000/instituicoes/ibge/bcim/municipios/3159407/', '*collect', 'geom', 'buffer', '0.2'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('within/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/*collect/geom/buffer/0.2/within/http://ibge/unidades-federativas/RJ/*'), ['within', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/', '*collect', 'geom', 'buffer', '0.2', 'within','http://ibge/unidades-federativas/RJ/'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('filter/geom/within/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/*'), ['filter', 'geom', 'within', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('filter/geom/within/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geom/*and/sigla/eq/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geocodigo/*'), ['filter', 'geom', 'within', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geom/', '*and', 'sigla', 'eq', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geocodigo/'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('filter/geom/within/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geom/*collect/collect/eq/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geocodigo/*'), ['filter', 'geom', 'within', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geom/', '*collect', 'collect', 'eq', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geocodigo/'])
 #       self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('filter/geom/within/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geom*/and/geocodigo/eq/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geocodigo/*/collect/collect/eq/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geocodigo*'),
#['filter', 'geom', 'within', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geom','and','geocodigo','eq','http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geom/and/geocodigo', 'collect', 'collect', 'eq', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geocodigo'])
        #self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('within/WWw.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407*/collect/geom/buffer/0.2'), ['filter', 'geom', 'within', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geom', 'and', 'sigla', 'eq', 'http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/geocodigo'])
        self.assertEquals(self.acr.attribute_functions_str_splitted_by_slash('filter/collect/within/http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/*collect/collect/transform/3005&True/area'),[
            'filter','collect','within','http://www.ibge.gov.br:8080/instituicoes/ibge/bcim/municipios/3159407/','*collect','collect','transform', '3005&True','area'] )

    def test_get_generic_operation_name(self):

        prefix = 'get_objects_from_'
        suffix = '_operation'

        operation_name = self.acr.get_generic_operation_name('filter/geom/within/http://luc00557347.ibge.gov.br/ibge/bcim/unidades-federativas/ES/geom/buffer/0.2*/and/fclass/eq/school/*collect/geom/buffer/0.2')
        self.assertEquals(operation_name, prefix + 'filter_and_collect' + suffix)

        operation_name = self.acr.get_generic_operation_name('filter/sigla/in/RJ,ES/*collect/geom/transform/3005&True/area')
        self.assertEquals(operation_name, prefix + 'filter_and_collect' + suffix)

        operation_name = self.acr.get_generic_operation_name('collect/geom/buffer/0.2/*filter/geom/within/http://luc00557347.ibge.gov.br/ibge/bcim/unidades-federativas/ES/geom/buffer/0.2/and/fclass/eq/school*/')
        self.assertEquals(operation_name, prefix + 'collect_and_filter' + suffix)

        operation_name = self.acr.get_generic_operation_name('filter/geom/within/http://luc00557347.ibge.gov.br/ibge/bcim/unidades-federativas/ES/geom/buffer/0.2')
        self.assertEquals(operation_name, prefix + 'filter' + suffix)

        operation_name = self.acr.get_generic_operation_name('collect/geom/buffer/0.2')
        self.assertEquals(operation_name, prefix + 'collect' + suffix)

        operation_name = self.acr.get_generic_operation_name('groupby/geom/')
        self.assertEquals(operation_name, prefix + 'groupby' + suffix)

        operation_name = self.acr.get_generic_operation_name('groupbycount/geom/')
        self.assertEquals(operation_name, prefix + 'groupbycount' + suffix)

        operation_name = self.acr.get_generic_operation_name('offsetlimit/1:10/')
        self.assertEquals(operation_name, prefix + 'offsetlimit' + suffix)

        operation_name = self.acr.get_generic_operation_name('distinct')
        self.assertEquals(operation_name, prefix + 'distinct' + suffix)

        operation_name = self.acr.get_generic_operation_name('countresource')
        self.assertEquals(operation_name, prefix + 'countresource' + suffix)

        operation_name = self.acr.get_generic_operation_name('annotate/')
        self.assertEquals(operation_name, prefix + 'annotate' + suffix)

class FeatureCollectionResourceTest(SimpleTestCase):
    def setUp(self):
        self.attributes_functions = ['filter/sigla/in/rj,es,go/', 'filter/sigla/uppercase/in/rj,es,go/and/data/between/2017-02-01,2017-06-30/', 'filter/sigla/in/rj,es,go/and/geom/within/{"type":"Polygon","coordinates":[[[-41.881710164667396,-21.297482165015307],[-28.840495695785098,-21.297482165015307],[-28.840495695785098,-17.886950999070834],[-41.881710164667396,-17.886950999070834],[-41.881710164667396,-21.297482165015307]]]}']
        self.fc = FeatureCollectionResource()

    def test_is_filter_operation(self):
        self.assertTrue(self.fc.path_has_filter_operation('filter/sigla/in/rj,es,go/and/geom'))
        self.assertFalse( self.fc.path_has_filter_operation('/filter'))
        self.assertTrue('filter/sigla/uppercase/in/rj,es,go/and/data/between/2017-02-01,2017-06-30/')

    def test_get_objects_serialized_by_filter_operation(self):
        pass


    def test_q_objects_from_filter_operation(self):
        return True
        result = self.fc.q_objects_from_filter_operation('filter/sigla/eq/ES')[0]
        self.assertEquals(result.__repr__(), Q(sigla='ES').__repr__())
        result = self.fc.q_objects_from_filter_operation('filter/sigla/eq/ES/')[0]
        self.assertEquals(result.__repr__(), Q(sigla='ES').__repr__())
        result = self.fc.q_objects_from_filter_operation('filter/sigla/in/ES,RJ')[0]
        self.assertEquals(result.__repr__(), Q(sigla__in=['ES,RJ']).__repr__())
        result = self.fc.q_objects_from_filter_operation('filter/sigla/in/ES,RJ/')[0]
        self.assertEquals(result, Q(sigla__in=['ES,RJ']))
        result1 = self.fc.q_objects_from_filter_operation('filter/sigla/in/ES,RJ/and/data/between/2017-02-01,2017-06-30')[0]
        result2 = self.fc.q_objects_from_filter_operation('filter/sigla/in/ES,RJ/and/data/between/2017-02-01,2017-06-30')[1]
        self.assertEquals(result1, Q(sigla__in=['ES,RJ']))
        self.assertEquals(result2, Q(data='ES,RJ'))

    def test_transform_path_with_spatial_operation_str_and_url_as_array(self):
        self.maxDiff = None
        s = 'geom/contains/http://172.30.10.86:8000/instituicoes/ibge/bcim/municipios/3159407/*or/geom/contains/http://172.30.10.86:8000/instituicoes/ibge/bcim/municipios/3159406'
        arr = ['geom', 'contains', 'http:','172.30.10.86:8000','instituicoes','ibge','bcim','municipios','3159407', '*or', 'geom', 'contains', 'http:','172.30.10.86:8000','instituicoes','ibge','bcim','municipios','3159406']
        arr1 = ['geom', 'contains', 'http://172.30.10.86:8000/instituicoes/ibge/bcim/municipios/3159407/', '*or', 'geom', 'contains', 'http://172.30.10.86:8000/instituicoes/ibge/bcim/municipios/3159406/']

        self.assertEquals(len(self.fc.transform_path_with_url_as_array(arr)), len(arr1))

class CollectionResourceTest(SimpleTestCase):
    def setUp(self):
        self.host = 'luc00557196.ibge.gov.br:8000/'
        self.base_uri = "http://" + self.host + "controle-list/"

    def test_simple_collection_request(self):
        # requests.get(uri, headers={key: value, key: value})
        res = requests.get(self.base_uri + "gasto-list/")
        self.assertEquals(res.status_code, 200)
        self.assertEquals(res.headers['content-type'], 'application/json')

    def test_collection_request_by_attributes(self):
        res = requests.get(self.base_uri + "gasto-list/id,data,valor")
        self.assertEquals(res.status_code, 200)
        self.assertEquals(res.headers['content-type'], 'application/json')

    def test_distinct_operation_for_collection_resource(self):
        res = requests.get(self.base_uri + "gasto-list/distinct/data")
        self.assertEquals(res.status_code, 200)
        self.assertEquals(res.headers['content-type'], 'application/json')

    def test_offset_limit_operation_for_collection_resource(self):
        res = requests.get(self.base_uri + "gasto-list/offsetLimit/2&3")
        self.assertEquals(res.status_code, 200)
        self.assertEquals(res.headers['content-type'], 'application/json')
    """
    def test_groupBy_operation_for_collection_resource(self):
        res = requests.get(self.base_uri + "gasto-list/groupBy/data,valor")
        self.assertEquals(res.status_code, 200)
        self.assertEquals(res.headers['content-type'], 'application/json')
    """

class RequestOptionsTest(SimpleTestCase):
    def setUp(self):
        self.host = 'luc00557196.ibge.gov.br:8000/'
        #self.host = '192.168.0.10:8000/'
        self.bcim_base_uri = "http://" + self.host + "ibge/bcim/"
        self.controle_base_uri = "http://" + self.host + "controle-list/"
        self.simple_path_options_dict_keys = ['@context', '@id', '@type', 'hydra:iriTemplate', 'hydra:representationName', 'hydra:supportedOperations', 'hydra:supportedProperties']
        self.path_with_geom_attr_dict_keys = ["@context", '@id', '@type', 'hydra:supportedOperations']
        self.spatial_operation_names = ['area', 'boundary', 'buffer', 'centroid', 'contains', 'convex_hull', 'coord_seq', 'coords', 'count', 'crosses',
                                        'crs', 'difference', 'dims', 'disjoint', 'distance', 'empty', 'envelope', 'equals', 'equals_exact', 'ewkb',
                                        'ewkt', 'extend', 'extent', 'geojson', 'geom_type', 'geom_typeid', 'get_coords', 'get_srid', 'get_x', 'get_y',
                                        'get_z', 'has_cs', 'hasz', 'hex', 'hexewkb', 'index', 'interpolate', 'intersection', 'intersects', 'json', 'kml',
                                        'length', 'normalize', 'num_coords', 'num_geom', 'num_points', 'ogr', 'overlaps', 'point_on_surface', 'relate',
                                        'relate_pattern', 'ring', 'set_coords', 'set_srid', 'set_x', 'set_y', 'set_z', 'simple', 'simplify', 'srid',
                                        'srs', 'sym_difference', 'touches', 'transform', 'union', 'valid', 'valid_reason', 'within', 'wkb', 'wkt', 'x', 'y', 'z']
        self.geometry_collection_operation_names = ['col_bbcontains', 'col_bboverlaps', 'col_contained', 'col_contains', 'col_contains_properly',
                                                    'col_covers', 'col_covers_by', 'col_crosses', 'col_disjoint', 'col_distance_gt', 'col_distance_gte',
                                                    'col_distance_lt', 'col_distance_lte', 'col_dwithin', 'col_extent', 'col_intersects', 'col_isvalid',
                                                    'col_left', 'col_make_line', 'col_overlaps', 'col_overlaps_above', 'col_overlaps_below', 'col_overlaps_left',
                                                    'col_overlaps_right', 'col_relate', 'col_right', 'col_strictly_above', 'col_strictly_below', 'col_touches',
                                                    'col_within', 'collect', 'count_resource', 'distinct', 'filter', 'group_by', 'group_by_count', 'offset_limit', 'union']
        self.collection_operation_names = ['collect', 'count_resource', 'distinct', 'filter', 'group_by', 'group_by_count', 'offset_limit']

    def aux_get_dict_from_response(self, response):
        json_response = json.loads(response.text)
        return dict(json_response)

    def aux_get_supported_operations_names(self, response):
        response_dict = self.aux_get_dict_from_response(response)
        operations_names = [operation_dict['hydra:operation'] for operation_dict in response_dict['hydra:supportedOperations']]
        operations_names.sort()
        return operations_names

    def aux_get_keys_from_response(self, response):
        response_dict = self.aux_get_dict_from_response(response)
        response_dict_keys = list(response_dict.keys())
        response_dict_keys.sort()
        return response_dict_keys

    def aux_get_keys_from_response_context(self, response):
        response_dict = self.aux_get_dict_from_response(response)
        context_keys = list(response_dict["@context"].keys())
        context_keys.sort()
        return context_keys

    # tests for feature collection
    def test_options_for_feature_collection_simple_path(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/")
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.simple_path_options_dict_keys)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.geometry_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'FeatureCollection')

    def test_options_for_feature_collection_simple_path_with_accept_header(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/", headers={'accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.simple_path_options_dict_keys)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'bytes')


    def test_options_for_feature_collection_only_attributes(self):
        attrs = ["geom", "nome"]
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/" + attrs[0] + "," + attrs[1])
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.path_with_geom_attr_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, attrs)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.geometry_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'FeatureCollection')

    def test_options_for_feature_collection_only_geometric_attribute(self):
        attrs = ["geom"]
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/" + attrs[0])
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.path_with_geom_attr_dict_keys)

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, attrs)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.geometry_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'GeometryCollection')

    def test_options_for_feature_collection_only_alphanumeric_attributes(self):
        alpha_attrs = ["nome", "nomeabrev"]
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/" + alpha_attrs[0] + "," + alpha_attrs[1])
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, ["@context", '@id', '@type'])

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_dict_keys, alpha_attrs)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Collection')


    def test_options_for_feature_collection_operation_with_geometry_collection_return(self):
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/col_within/" + self.bcim_base_uri + "unidades-federativas/ES")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, ["@context", '@id', '@type', "hydra:supportedOperations"])

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_dict_keys, ['within'])

        supp_oper_for_ret_type = self.aux_get_supported_operations_names(response)
        self.assertEquals(supp_oper_for_ret_type, self.geometry_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'FeatureCollection')

    def test_options_for_feature_collection_operation_with_geometry_collection_return_and_accept_header(self):
        response = requests.options(
            self.bcim_base_uri + "aldeias-indigenas/col_within/" + self.bcim_base_uri + "unidades-federativas/ES",
            headers={'accept': 'application/octet-stream'}
        )
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, ["@context", '@id', '@type', "hydra:supportedOperations"])

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_dict_keys, ['within'])

        supp_oper_for_ret_type = self.aux_get_supported_operations_names(response)
        self.assertEquals(supp_oper_for_ret_type, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'bytes')


    def test_options_collect_for_feature_collection_with_spatial_operation_geometry_return_type(self):
        attrs = ["geom", "nome"]
        response = requests.options(self.bcim_base_uri + "aldeias-indigenas/collect/" + attrs[1] + "&" + attrs[0] + "/buffer/0.2")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.path_with_geom_attr_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        attrs.append('buffer')
        attrs.sort()
        self.assertListEqual(context_dict_keys, attrs)

        response_operations_name = self.aux_get_supported_operations_names(response)
        self.assertListEqual(response_operations_name, self.geometry_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'FeatureCollection')

    def test_options_collect_for_feature_collection_with_spatial_operation_geometry_return_type_and_only_geometric_attribute(self):
        attrs = ["geom"]
        response = requests.options(
            self.bcim_base_uri + "aldeias-indigenas/collect/" + attrs[0] + "/buffer/0.2")
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.path_with_geom_attr_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        attrs.append('buffer')
        attrs.sort()
        self.assertListEqual(context_dict_keys, attrs)

        response_operations_name = self.aux_get_supported_operations_names(response)
        self.assertListEqual(response_operations_name, self.geometry_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'GeometryCollection')

    def test_options_collect_for_feature_collection_with_spatial_operation_geometry_return_type_and_accept_header(self):
        attrs = ["geom", "nome"]
        response = requests.options(
            self.bcim_base_uri + "aldeias-indigenas/collect/" + attrs[1] + "&" + attrs[0] + "/buffer/0.2",
            headers={'accept': 'application/octet-stream'}
        )
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.path_with_geom_attr_dict_keys)

        context_dict_keys = self.aux_get_keys_from_response_context(response)
        attrs.append('buffer')
        attrs.sort()
        self.assertListEqual(context_dict_keys, attrs)

        response_operations_name = self.aux_get_supported_operations_names(response)
        self.assertListEqual(response_operations_name, self.geometry_collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'bytes')

    # tests for collection
    def test_options_for_collection_simple_path(self):
        response = requests.options(self.controle_base_uri + 'gasto-list/')
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.simple_path_options_dict_keys)

        operation_name = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operation_name, self.collection_operation_names)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Collection')

    def test_options_for_collection_simple_path_with_accept_header(self):
        response = requests.options(self.controle_base_uri + 'gasto-list/', headers={'accept': 'application/octet-stream'})
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, self.simple_path_options_dict_keys)

        operation_name = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operation_name, [])

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'bytes')

    def test_options_for_collection_only_attributes(self):
        attrs = ['data', 'valor']
        response = requests.options(self.controle_base_uri + 'gasto-list/' + attrs[0] + ',' + attrs[1])
        self.assertEquals(response.status_code, 200)

        response_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_keys, ['@context', '@id', '@type'])

        context_keys = self.aux_get_keys_from_response_context(response)
        self.assertListEqual(context_keys, attrs)

        response_dict = self.aux_get_dict_from_response(response)
        self.assertEquals(response_dict["@type"], 'Collection')

    """
    def test_options_for_feature_resource_simple_path(self):
        response = requests.options(self.base_uri + 'unidades-federativas/ES')
        self.assertEquals(response.status_code, 200)

        response_dict_keys = self.aux_get_keys_from_response(response)
        self.assertListEqual(response_dict_keys, self.simple_path_options_dict_keys)

        operations_names = self.aux_get_supported_operations_names(response)
        self.assertListEqual(operations_names, self.spatial_operation_names)

    def test_options_for_feature_resource_only_attributes(self):
        attrs = ["geom", "nome"]
        response = requests.options(self.base_uri + 'unidades-federativas/ES/' + attrs[0] + "," + attrs[1])
        self.assertEquals(response.status_code, 200)

        json_response = json.loads(response.text)
        response_dict = dict(json_response)
        response_dict_keys = list(response_dict.keys())
        response_dict_keys.sort()
        self.assertListEqual(response_dict_keys, self.path_with_geom_attr_dict_keys)

        context_for_attrs = response_dict['@context'].keys()
        context_for_attrs.sort()
        self.assertListEqual(context_for_attrs, attrs)

        operations_names = self.aux_get_supported_operations_names(response_dict)
        self.assertListEqual(operations_names, self.spatial_operation_names)

    def test_options_for_feature_resource_only_alphanumeric_attributes(self):
        alpha_attrs = ["geocodigo", "nome"]
        response = requests.options(self.base_uri + 'unidades-federativas/ES/' + alpha_attrs[0] + "," + alpha_attrs[1])
        self.assertEquals(response.status_code, 200)

        json_response = json.loads(response.text)
        response_dict = dict(json_response)
        response_dict_keys = response_dict.keys()
        response_dict_keys = list(response_dict_keys)
        response_dict_keys.sort()
        self.assertListEqual(response_dict_keys, ["@context"])

        context_dict_keys = list(response_dict["@context"].keys())
        context_dict_keys.sort()
        self.assertListEqual(alpha_attrs, context_dict_keys)
    """
    """
class RequestHeadersTest(SimpleTestCase):
    def setUp(self):
        self.host = 'luc00557196.ibge.gov.br:8000/'
        self.bcim_base_uri = "http://" + self.host + "ibge/bcim/"
        self.geo_json_content_type = 'application/vnd.geo+json'
        self.cors_headers = {"access-control-allow-headers" : ['accept', 'accept-encoding', 'authorization', 'content-location', 'content-type', 'dnt', 'link', 'origin', 'user-agent', 'x-csrftoken', 'x-requested-with'],
                             "access-control-allow-methods": ["GET", "HEAD", "OPTIONS"],
                             "access-control-allow-origin": "*",
                             "access-control-expose-headers": ['accept', 'accept-encoding', 'access-control-allow-origin', 'authorization', 'content-location', 'content-type', 'dnt', 'link', 'origin', 'user-agent', 'x-access-token', 'x-csrftoken', 'x-requested-with'],
                             "allow" : ['DELETE', 'GET', 'HEAD', 'OPTIONS', 'PATCH', 'POST', 'PUT'],
                             }

    def aux_order_response_dict(self, response):
        for k in sorted(response.headers):
            print("Chave: " + str(k) + " Valor:" + response.headers[k] )
        #collections.OrderedDict(sorted(resp_headers.items()))

    def test_get_for_feature_collection_simple_path(self):
        #res = requests.get(self.bcim_base_uri + 'aldeias-indigenas', headers=self.headers)
        response = requests.get(self.bcim_base_uri + 'aldeias-indigenas')
        self.aux_order_response_dict(response)
        #self.assertEquals(response.headers['content-type'], self.geo_json_content_type)

        #resp_dict = sorted(response.headers)
        #self.assertDictEqual(resp_dict, self.cors_headers)

    def test_head_for_feature_collection_simple_path(self):
        response = requests.head(self.bcim_base_uri + 'aldeias-indigenas')
        self.assertEquals(response.headers['content-type'], self.geo_json_content_type)
    """