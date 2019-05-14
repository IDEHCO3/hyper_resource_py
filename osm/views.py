from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from hyper_resource.views import *
from hyper_resource.contexts import *
from osm.models import *
from osm.serializers import *
from osm.contexts import *

from hyper_resource.resources.EntryPointResource import *
from hyper_resource.resources.AbstractCollectionResource import AbstractCollectionResource
from hyper_resource.resources.AbstractResource import *
from hyper_resource.resources.CollectionResource import CollectionResource
from hyper_resource.resources.FeatureCollectionResource import FeatureCollectionResource
from hyper_resource.resources.FeatureResource import FeatureResource
from hyper_resource.resources.NonSpatialResource import NonSpatialResource
from hyper_resource.resources.RasterCollectionResource import RasterCollectionResource
from hyper_resource.resources.RasterResource import RasterResource
from hyper_resource.resources.SpatialCollectionResource import SpatialCollectionResource
from hyper_resource.resources.SpatialResource import SpatialResource
from hyper_resource.resources.StyleResource import StyleResource
from hyper_resource.resources.TiffCollectionResource import TiffCollectionResource
from hyper_resource.resources.TiffResource import TiffResource
import geobuf

class APIRoot(FeatureEntryPointResource):

    serializer_class = EntryPointSerializer

    def get_root_response(self, request, format=None, *args, **kwargs):
        root_links = {

          'aldeia-indigena-list': reverse('osm:AldeiaIndigena_list' , request=request, format=format),
          'buildings-list': reverse('osm:Buildings_list' , request=request, format=format),
          'comando-insert-list': reverse('osm:ComandoInsert_list' , request=request, format=format),
          'eixos-al-list': reverse('osm:EixosAl_list' , request=request, format=format),
          'eixos-cete2018-list': reverse('osm:EixosCete2018_list' , request=request, format=format),
          'eixos-rj-list': reverse('osm:EixosRj_list' , request=request, format=format),
          'landuse-list': reverse('osm:Landuse_list' , request=request, format=format),
          'municipios2018-list': reverse('osm:Municipios2018_list' , request=request, format=format),
          'municipios-al-list': reverse('osm:MunicipiosAl_list' , request=request, format=format),
          'municipios-rj-list': reverse('osm:MunicipiosRj_list' , request=request, format=format),
          'natural-list': reverse('osm:Natural_list' , request=request, format=format),
          'natural-a-list': reverse('osm:NaturalA_list' , request=request, format=format),
          'places-list': reverse('osm:Places_list' , request=request, format=format),
          'places-a-list': reverse('osm:PlacesA_list' , request=request, format=format),
          'pofw-list': reverse('osm:Pofw_list' , request=request, format=format),
          'pofw-a-list': reverse('osm:PofwA_list' , request=request, format=format),
          'pois-list': reverse('osm:Pois_list' , request=request, format=format),
          'pois-a-list': reverse('osm:PoisA_list' , request=request, format=format),
          'railways-list': reverse('osm:Railways_list' , request=request, format=format),
          'roads-list': reverse('osm:Roads_list' , request=request, format=format),
          't-lm-estados-list': reverse('osm:TLmEstados_list' , request=request, format=format),
          't-lm-municipios-list': reverse('osm:TLmMunicipios_list' , request=request, format=format),
          't-lm-vias-list': reverse('osm:TLmVias_list' , request=request, format=format),
          't-st-eixo-logr2018-list': reverse('osm:TStEixoLogr2018_list' , request=request, format=format),
          't-st-eixos-logradouro-list': reverse('osm:TStEixosLogradouro_list' , request=request, format=format),
          't-st-vias2018-list': reverse('osm:TStVias2018_list' , request=request, format=format),
          'traffic-list': reverse('osm:Traffic_list' , request=request, format=format),
          'traffic-a-list': reverse('osm:TrafficA_list' , request=request, format=format),
          'transport-list': reverse('osm:Transport_list' , request=request, format=format),
          'transport-a-list': reverse('osm:TransportA_list' , request=request, format=format),
          'trecho-ferroviario-list': reverse('osm:TrechoFerroviario_list' , request=request, format=format),
          'unidade-federacao-list': reverse('osm:UnidadeFederacao_list' , request=request, format=format),
          'water-list': reverse('osm:Water_list' , request=request, format=format),
          'waterways-list': reverse('osm:Waterways_list' , request=request, format=format),
        }

        ordered_dict_of_link = OrderedDict(sorted(root_links.items(), key=lambda t: t[0]))
        return ordered_dict_of_link

class AldeiaIndigenaList(FeatureCollectionResource):
    queryset = AldeiaIndigena.objects.all()
    serializer_class = AldeiaIndigenaSerializer
    contextclassname = 'aldeia-indigena-list'
    def initialize_context(self):
        self.context_resource = AldeiaIndigenaListContext()
        self.context_resource.resource = self

    '''
    def basic_get(self, request, *args, **kwargs):
        self.object_model = self.model_class()()
        self.set_basic_context_resource(request)
        attributes_functions_str = self.kwargs.get('attributes_functions')

        if self.is_simple_path(attributes_functions_str):
            return self.required_object_for_simple_path(request)
    '''


class AldeiaIndigenaDetail(FeatureResource):
    serializer_class = AldeiaIndigenaSerializer
    contextclassname = 'aldeia-indigena-list'
    def initialize_context(self):
        self.context_resource = AldeiaIndigenaDetailContext()
        self.context_resource.resource = self

class BuildingsList(FeatureCollectionResource):
    queryset = Buildings.objects.all()
    serializer_class = BuildingsSerializer
    contextclassname = 'buildings-list'
    def initialize_context(self):
        self.context_resource = BuildingsListContext()
        self.context_resource.resource = self

class BuildingsDetail(FeatureResource):
    serializer_class = BuildingsSerializer
    contextclassname = 'buildings-list'
    def initialize_context(self):
        self.context_resource = BuildingsDetailContext()
        self.context_resource.resource = self

class ComandoInsertList(CollectionResource):
    queryset = ComandoInsert.objects.all()
    serializer_class = ComandoInsertSerializer
    contextclassname = 'comando-insert-list'
    def initialize_context(self):
        self.context_resource = ComandoInsertListContext()
        self.context_resource.resource = self

class ComandoInsertDetail(NonSpatialResource):
    serializer_class = ComandoInsertSerializer
    contextclassname = 'comando-insert-list'
    def initialize_context(self):
        self.context_resource = ComandoInsertDetailContext()
        self.context_resource.resource = self

class EixosAlList(FeatureCollectionResource):
    queryset = EixosAl.objects.all()
    serializer_class = EixosAlSerializer
    contextclassname = 'eixos-al-list'
    def initialize_context(self):
        self.context_resource = EixosAlListContext()
        self.context_resource.resource = self

class EixosAlDetail(FeatureResource):
    serializer_class = EixosAlSerializer
    contextclassname = 'eixos-al-list'
    def initialize_context(self):
        self.context_resource = EixosAlDetailContext()
        self.context_resource.resource = self

class EixosCete2018List(FeatureCollectionResource):
    queryset = EixosCete2018.objects.all()
    serializer_class = EixosCete2018Serializer
    contextclassname = 'eixos-cete2018-list'
    def initialize_context(self):
        self.context_resource = EixosCete2018ListContext()
        self.context_resource.resource = self

class EixosCete2018Detail(FeatureResource):
    serializer_class = EixosCete2018Serializer
    contextclassname = 'eixos-cete2018-list'
    def initialize_context(self):
        self.context_resource = EixosCete2018DetailContext()
        self.context_resource.resource = self

class EixosRjList(FeatureCollectionResource):
    queryset = EixosRj.objects.all()
    serializer_class = EixosRjSerializer
    contextclassname = 'eixos-rj-list'
    def initialize_context(self):
        self.context_resource = EixosRjListContext()
        self.context_resource.resource = self

class EixosRjDetail(FeatureResource):
    serializer_class = EixosRjSerializer
    contextclassname = 'eixos-rj-list'
    def initialize_context(self):
        self.context_resource = EixosRjDetailContext()
        self.context_resource.resource = self

class LanduseList(FeatureCollectionResource):
    queryset = Landuse.objects.all()
    serializer_class = LanduseSerializer
    contextclassname = 'landuse-list'
    def initialize_context(self):
        self.context_resource = LanduseListContext()
        self.context_resource.resource = self

class LanduseDetail(FeatureResource):
    serializer_class = LanduseSerializer
    contextclassname = 'landuse-list'
    def initialize_context(self):
        self.context_resource = LanduseDetailContext()
        self.context_resource.resource = self

class Municipios2018List(FeatureCollectionResource):
    queryset = Municipios2018.objects.all()
    serializer_class = Municipios2018Serializer
    contextclassname = 'municipios2018-list'
    def initialize_context(self):
        self.context_resource = Municipios2018ListContext()
        self.context_resource.resource = self

class Municipios2018Detail(FeatureResource):
    serializer_class = Municipios2018Serializer
    contextclassname = 'municipios2018-list'
    def initialize_context(self):
        self.context_resource = Municipios2018DetailContext()
        self.context_resource.resource = self

class MunicipiosAlList(FeatureCollectionResource):
    queryset = MunicipiosAl.objects.all()
    serializer_class = MunicipiosAlSerializer
    contextclassname = 'municipios-al-list'
    def initialize_context(self):
        self.context_resource = MunicipiosAlListContext()
        self.context_resource.resource = self

class MunicipiosAlDetail(FeatureResource):
    serializer_class = MunicipiosAlSerializer
    contextclassname = 'municipios-al-list'
    def initialize_context(self):
        self.context_resource = MunicipiosAlDetailContext()
        self.context_resource.resource = self

class MunicipiosRjList(FeatureCollectionResource):
    queryset = MunicipiosRj.objects.all()
    serializer_class = MunicipiosRjSerializer
    contextclassname = 'municipios-rj-list'
    def initialize_context(self):
        self.context_resource = MunicipiosRjListContext()
        self.context_resource.resource = self

class MunicipiosRjDetail(FeatureResource):
    serializer_class = MunicipiosRjSerializer
    contextclassname = 'municipios-rj-list'
    def initialize_context(self):
        self.context_resource = MunicipiosRjDetailContext()
        self.context_resource.resource = self

class NaturalList(FeatureCollectionResource):
    queryset = Natural.objects.all()
    serializer_class = NaturalSerializer
    contextclassname = 'natural-list'
    def initialize_context(self):
        self.context_resource = NaturalListContext()
        self.context_resource.resource = self

class NaturalDetail(FeatureResource):
    serializer_class = NaturalSerializer
    contextclassname = 'natural-list'
    def initialize_context(self):
        self.context_resource = NaturalDetailContext()
        self.context_resource.resource = self

class NaturalAList(FeatureCollectionResource):
    queryset = NaturalA.objects.all()
    serializer_class = NaturalASerializer
    contextclassname = 'natural-a-list'
    def initialize_context(self):
        self.context_resource = NaturalAListContext()
        self.context_resource.resource = self

class NaturalADetail(FeatureResource):
    serializer_class = NaturalASerializer
    contextclassname = 'natural-a-list'
    def initialize_context(self):
        self.context_resource = NaturalADetailContext()
        self.context_resource.resource = self

class PlacesList(FeatureCollectionResource):
    queryset = Places.objects.all()
    serializer_class = PlacesSerializer
    contextclassname = 'places-list'
    def initialize_context(self):
        self.context_resource = PlacesListContext()
        self.context_resource.resource = self

class PlacesDetail(FeatureResource):
    serializer_class = PlacesSerializer
    contextclassname = 'places-list'
    def initialize_context(self):
        self.context_resource = PlacesDetailContext()
        self.context_resource.resource = self

class PlacesAList(FeatureCollectionResource):
    queryset = PlacesA.objects.all()
    serializer_class = PlacesASerializer
    contextclassname = 'places-a-list'
    def initialize_context(self):
        self.context_resource = PlacesAListContext()
        self.context_resource.resource = self

class PlacesADetail(FeatureResource):
    serializer_class = PlacesASerializer
    contextclassname = 'places-a-list'
    def initialize_context(self):
        self.context_resource = PlacesADetailContext()
        self.context_resource.resource = self

class PofwList(FeatureCollectionResource):
    queryset = Pofw.objects.all()
    serializer_class = PofwSerializer
    contextclassname = 'pofw-list'
    def initialize_context(self):
        self.context_resource = PofwListContext()
        self.context_resource.resource = self

class PofwDetail(FeatureResource):
    serializer_class = PofwSerializer
    contextclassname = 'pofw-list'
    def initialize_context(self):
        self.context_resource = PofwDetailContext()
        self.context_resource.resource = self

class PofwAList(FeatureCollectionResource):
    queryset = PofwA.objects.all()
    serializer_class = PofwASerializer
    contextclassname = 'pofw-a-list'
    def initialize_context(self):
        self.context_resource = PofwAListContext()
        self.context_resource.resource = self

class PofwADetail(FeatureResource):
    serializer_class = PofwASerializer
    contextclassname = 'pofw-a-list'
    def initialize_context(self):
        self.context_resource = PofwADetailContext()
        self.context_resource.resource = self

class PoisList(FeatureCollectionResource):
    queryset = Pois.objects.all()
    serializer_class = PoisSerializer
    contextclassname = 'pois-list'
    def initialize_context(self):
        self.context_resource = PoisListContext()
        self.context_resource.resource = self

class PoisDetail(FeatureResource):
    serializer_class = PoisSerializer
    contextclassname = 'pois-list'
    def initialize_context(self):
        self.context_resource = PoisDetailContext()
        self.context_resource.resource = self

class PoisAList(FeatureCollectionResource):
    queryset = PoisA.objects.all()
    serializer_class = PoisASerializer
    contextclassname = 'pois-a-list'
    def initialize_context(self):
        self.context_resource = PoisAListContext()
        self.context_resource.resource = self

class PoisADetail(FeatureResource):
    serializer_class = PoisASerializer
    contextclassname = 'pois-a-list'
    def initialize_context(self):
        self.context_resource = PoisADetailContext()
        self.context_resource.resource = self

class RailwaysList(FeatureCollectionResource):
    queryset = Railways.objects.all()
    serializer_class = RailwaysSerializer
    contextclassname = 'railways-list'
    def initialize_context(self):
        self.context_resource = RailwaysListContext()
        self.context_resource.resource = self

class RailwaysDetail(FeatureResource):
    serializer_class = RailwaysSerializer
    contextclassname = 'railways-list'
    def initialize_context(self):
        self.context_resource = RailwaysDetailContext()
        self.context_resource.resource = self

class RoadsList(FeatureCollectionResource):
    queryset = Roads.objects.all()
    serializer_class = RoadsSerializer
    contextclassname = 'roads-list'
    def initialize_context(self):
        self.context_resource = RoadsListContext()
        self.context_resource.resource = self

class RoadsDetail(FeatureResource):
    serializer_class = RoadsSerializer
    contextclassname = 'roads-list'
    def initialize_context(self):
        self.context_resource = RoadsDetailContext()
        self.context_resource.resource = self

class TLmEstadosList(FeatureCollectionResource):
    queryset = TLmEstados.objects.all()
    serializer_class = TLmEstadosSerializer
    contextclassname = 't-lm-estados-list'
    def initialize_context(self):
        self.context_resource = TLmEstadosListContext()
        self.context_resource.resource = self

class TLmEstadosDetail(FeatureResource):
    serializer_class = TLmEstadosSerializer
    contextclassname = 't-lm-estados-list'
    def initialize_context(self):
        self.context_resource = TLmEstadosDetailContext()
        self.context_resource.resource = self

class TLmMunicipiosList(FeatureCollectionResource):
    queryset = TLmMunicipios.objects.all()
    serializer_class = TLmMunicipiosSerializer
    contextclassname = 't-lm-municipios-list'
    def initialize_context(self):
        self.context_resource = TLmMunicipiosListContext()
        self.context_resource.resource = self

class TLmMunicipiosDetail(FeatureResource):
    serializer_class = TLmMunicipiosSerializer
    contextclassname = 't-lm-municipios-list'
    def initialize_context(self):
        self.context_resource = TLmMunicipiosDetailContext()
        self.context_resource.resource = self

class TLmViasList(FeatureCollectionResource):
    queryset = TLmVias.objects.all()
    serializer_class = TLmViasSerializer
    contextclassname = 't-lm-vias-list'
    def initialize_context(self):
        self.context_resource = TLmViasListContext()
        self.context_resource.resource = self

class TLmViasDetail(FeatureResource):
    serializer_class = TLmViasSerializer
    contextclassname = 't-lm-vias-list'
    def initialize_context(self):
        self.context_resource = TLmViasDetailContext()
        self.context_resource.resource = self

class TStEixoLogr2018List(FeatureCollectionResource):
    queryset = TStEixoLogr2018.objects.all()
    serializer_class = TStEixoLogr2018Serializer
    contextclassname = 't-st-eixo-logr2018-list'
    def initialize_context(self):
        self.context_resource = TStEixoLogr2018ListContext()
        self.context_resource.resource = self

class TStEixoLogr2018Detail(FeatureResource):
    serializer_class = TStEixoLogr2018Serializer
    contextclassname = 't-st-eixo-logr2018-list'
    def initialize_context(self):
        self.context_resource = TStEixoLogr2018DetailContext()
        self.context_resource.resource = self

class TStEixosLogradouroList(FeatureCollectionResource):
    queryset = TStEixosLogradouro.objects.all()
    serializer_class = TStEixosLogradouroSerializer
    contextclassname = 't-st-eixos-logradouro-list'
    def initialize_context(self):
        self.context_resource = TStEixosLogradouroListContext()
        self.context_resource.resource = self

class TStEixosLogradouroDetail(FeatureResource):
    serializer_class = TStEixosLogradouroSerializer
    contextclassname = 't-st-eixos-logradouro-list'
    def initialize_context(self):
        self.context_resource = TStEixosLogradouroDetailContext()
        self.context_resource.resource = self

class TStVias2018List(FeatureCollectionResource):
    queryset = TStVias2018.objects.all()
    serializer_class = TStVias2018Serializer
    contextclassname = 't-st-vias2018-list'
    def initialize_context(self):
        self.context_resource = TStVias2018ListContext()
        self.context_resource.resource = self

class TStVias2018Detail(FeatureResource):
    serializer_class = TStVias2018Serializer
    contextclassname = 't-st-vias2018-list'
    def initialize_context(self):
        self.context_resource = TStVias2018DetailContext()
        self.context_resource.resource = self

class TrafficList(FeatureCollectionResource):
    queryset = Traffic.objects.all()
    serializer_class = TrafficSerializer
    contextclassname = 'traffic-list'
    def initialize_context(self):
        self.context_resource = TrafficListContext()
        self.context_resource.resource = self

class TrafficDetail(FeatureResource):
    serializer_class = TrafficSerializer
    contextclassname = 'traffic-list'
    def initialize_context(self):
        self.context_resource = TrafficDetailContext()
        self.context_resource.resource = self

class TrafficAList(FeatureCollectionResource):
    queryset = TrafficA.objects.all()
    serializer_class = TrafficASerializer
    contextclassname = 'traffic-a-list'
    def initialize_context(self):
        self.context_resource = TrafficAListContext()
        self.context_resource.resource = self

class TrafficADetail(FeatureResource):
    serializer_class = TrafficASerializer
    contextclassname = 'traffic-a-list'
    def initialize_context(self):
        self.context_resource = TrafficADetailContext()
        self.context_resource.resource = self

class TransportList(FeatureCollectionResource):
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    contextclassname = 'transport-list'
    def initialize_context(self):
        self.context_resource = TransportListContext()
        self.context_resource.resource = self

class TransportDetail(FeatureResource):
    serializer_class = TransportSerializer
    contextclassname = 'transport-list'
    def initialize_context(self):
        self.context_resource = TransportDetailContext()
        self.context_resource.resource = self

class TransportAList(FeatureCollectionResource):
    queryset = TransportA.objects.all()
    serializer_class = TransportASerializer
    contextclassname = 'transport-a-list'
    def initialize_context(self):
        self.context_resource = TransportAListContext()
        self.context_resource.resource = self

class TransportADetail(FeatureResource):
    serializer_class = TransportASerializer
    contextclassname = 'transport-a-list'
    def initialize_context(self):
        self.context_resource = TransportADetailContext()
        self.context_resource.resource = self

class TrechoFerroviarioList(FeatureCollectionResource):
    queryset = TrechoFerroviario.objects.all()
    serializer_class = TrechoFerroviarioSerializer
    contextclassname = 'trecho-ferroviario-list'
    def initialize_context(self):
        self.context_resource = TrechoFerroviarioListContext()
        self.context_resource.resource = self

    '''
    def basic_get(self, request, *args, **kwargs):
        self.object_model = self.model_class()()
        self.set_basic_context_resource(request)
        attributes_functions_str = self.kwargs.get('attributes_functions')

        if self.is_simple_path(attributes_functions_str):
            return self.required_object_for_simple_path(request)
    '''

    '''
    def required_object_for_simple_path(self, request):
        if not self.accept_is_binary(request):
            return super(TrechoFerroviarioList, self).required_object_for_simple_path(request)
        binary_content = self.object_model.get_model_objects_geobuf(self)
        return RequiredObject(binary_content.tobytes(), CONTENT_TYPE_OCTET_STREAM, self.object_model, 200)
    '''

class TrechoFerroviarioDetail(FeatureResource):
    serializer_class = TrechoFerroviarioSerializer
    contextclassname = 'trecho-ferroviario-list'
    def initialize_context(self):
        self.context_resource = TrechoFerroviarioDetailContext()
        self.context_resource.resource = self


class UnidadeFederacaoList(FeatureCollectionResource):
    queryset = UnidadeFederacao.objects.all()
    serializer_class = UnidadeFederacaoSerializer
    contextclassname = 'unidade-federacao-list'
    def initialize_context(self):
        self.context_resource = UnidadeFederacaoListContext()
        self.context_resource.resource = self

    '''
    def basic_get(self, request, *args, **kwargs):
        self.object_model = self.model_class()()
        self.set_basic_context_resource(request)
        attributes_functions_str = self.kwargs.get('attributes_functions')

        if self.is_simple_path(attributes_functions_str):
            return self.required_object_for_simple_path(request)
    '''
    '''
    def required_object_for_simple_path(self, request):
        if not self.accept_is_binary(request):
            return super(UnidadeFederacaoList, self).required_object_for_simple_path(request)
        binary_content = self.object_model.get_model_objects_geobuf(self)
        return RequiredObject(binary_content.tobytes(), CONTENT_TYPE_OCTET_STREAM, self.object_model, 200)
    '''

class UnidadeFederacaoDetail(FeatureResource):
    serializer_class = UnidadeFederacaoSerializer
    contextclassname = 'unidade-federacao-list'
    def initialize_context(self):
        self.context_resource = UnidadeFederacaoDetailContext()
        self.context_resource.resource = self

class WaterList(FeatureCollectionResource):
    queryset = Water.objects.all()
    serializer_class = WaterSerializer
    contextclassname = 'water-list'
    def initialize_context(self):
        self.context_resource = WaterListContext()
        self.context_resource.resource = self

class WaterDetail(FeatureResource):
    serializer_class = WaterSerializer
    contextclassname = 'water-list'
    def initialize_context(self):
        self.context_resource = WaterDetailContext()
        self.context_resource.resource = self

class WaterwaysList(FeatureCollectionResource):
    queryset = Waterways.objects.all()
    serializer_class = WaterwaysSerializer
    contextclassname = 'waterways-list'
    def initialize_context(self):
        self.context_resource = WaterwaysListContext()
        self.context_resource.resource = self

class WaterwaysDetail(FeatureResource):
    serializer_class = WaterwaysSerializer
    contextclassname = 'waterways-list'
    def initialize_context(self):
        self.context_resource = WaterwaysDetailContext()
        self.context_resource.resource = self

