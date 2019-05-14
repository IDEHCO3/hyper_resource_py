from osm.models import *
from hyper_resource.serializers import *
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from rest_framework.serializers import HyperlinkedRelatedField

class AldeiaIndigenaSerializer(GeoBusinessSerializer):
    class Meta:
        model = AldeiaIndigena
        fields = ['gid','id_objeto','nome','nomeabrev','geometriaa','codigofuna','terraindig','etnia','id_produto','id_element','cd_insumo_field','nr_insumo_field','nr_insumo0','tx_insumo_field','geom']
        geo_field = 'geom'
        identifier = 'gid'
        identifiers = ['pk', 'gid']

class BuildingsSerializer(GeoBusinessSerializer):
    class Meta:
        model = Buildings
        fields = ['gid','osm_id','code','fclass','name','type','geom']
        geo_field = 'geom'
        identifier = 'gid'
        identifiers = ['pk', 'gid']

class ComandoInsertSerializer(BusinessSerializer):
    class Meta:
        model = ComandoInsert
        fields = ['id','field_column_field']
        identifier = 'id'
        identifiers = ['pk', 'id']

class EixosAlSerializer(GeoBusinessSerializer):
    class Meta:
        model = EixosAl
        fields = ['id','geom','cd_layer','cd_setor','nm_txtmemo','cd_seq_log','tp_insumo_field']
        geo_field = 'geom'
        identifier = 'id'
        identifiers = ['pk', 'id']

class EixosCete2018Serializer(GeoBusinessSerializer):
    class Meta:
        model = EixosCete2018
        fields = ['gid','fid','cd_layer','cd_setor','nm_txtmemo','cd_seq_log','id','tp_insumo_field','geom']
        geo_field = 'geom'
        identifier = 'gid'
        identifiers = ['pk', 'gid']

class EixosRjSerializer(GeoBusinessSerializer):
    class Meta:
        model = EixosRj
        fields = ['gid','id','cd_setor','nm_txtmemo','chk_linha','id1','geom']
        geo_field = 'geom'
        identifier = 'gid'
        identifiers = ['pk', 'gid']

class EntryPointSerializer(BusinessSerializer):
    class Meta:
        model = EntryPoint
        fields = ['eixos_cete2018','municipios2018','aldeia_indigena','buildings','comando_insert','eixos_al','eixos_rj','landuse','municipios_al','municipios_rj','natural','natural_a','places','places_a','pofw','pofw_a','pois','pois_a','railways','roads','t_lm_estados','t_lm_municipios','t_lm_vias','t_st_eixo_logr2018','t_st_eixos_logradouro','t_st_vias2018','traffic','traffic_a','transport','transport_a','trecho_ferroviario','unidade_federacao','water','waterways']
        identifier = None
        identifiers = []

class LanduseSerializer(GeoBusinessSerializer):
    class Meta:
        model = Landuse
        fields = ['gid','osm_id','code','fclass','name','geom']
        geo_field = 'geom'
        identifier = 'gid'
        identifiers = ['pk', 'gid']

class Municipios2018Serializer(GeoBusinessSerializer):
    class Meta:
        model = Municipios2018
        fields = ['id','geom','fid','id_0','vl_area_tot','cd_geocodigo','vl_latitudesede','vl_longitudesede','nm_municipio','vl_perimetro','cd_sede','cd_ano','tp_insumo_img']
        geo_field = 'geom'
        identifier = 'id'
        identifiers = ['pk', 'id']

class MunicipiosAlSerializer(GeoBusinessSerializer):
    class Meta:
        model = MunicipiosAl
        fields = ['id','geom','vl_area_to','cd_geocodi','vl_latitud','vl_longitu','nm_municip','vl_perimet','cd_sede','cd_ano','tp_insumo_field']
        geo_field = 'geom'
        identifier = 'id'
        identifiers = ['pk', 'id']

class MunicipiosRjSerializer(GeoBusinessSerializer):
    class Meta:
        model = MunicipiosRj
        fields = ['id','geom','vl_area_to','cd_geocodigo','vl_latitud','vl_longitu','nm_municipio','vl_perimet','cd_sede','cd_ano','tp_insumo_field']
        geo_field = 'geom'
        identifier = 'id'
        identifiers = ['pk', 'id']

class NaturalSerializer(GeoBusinessSerializer):
    class Meta:
        model = Natural
        fields = ['gid','osm_id','code','fclass','name','geom']
        geo_field = 'geom'
        identifier = 'gid'
        identifiers = ['pk', 'gid']

class NaturalASerializer(GeoBusinessSerializer):
    class Meta:
        model = NaturalA
        fields = ['gid','osm_id','code','fclass','name','geom']
        geo_field = 'geom'
        identifier = 'gid'
        identifiers = ['pk', 'gid']

class PlacesSerializer(GeoBusinessSerializer):
    class Meta:
        model = Places
        fields = ['gid','osm_id','code','fclass','population','name','geom']
        geo_field = 'geom'
        identifier = 'gid'
        identifiers = ['pk', 'gid']

class PlacesASerializer(GeoBusinessSerializer):
    class Meta:
        model = PlacesA
        fields = ['gid','osm_id','code','fclass','population','name','geom']
        geo_field = 'geom'
        identifier = 'gid'
        identifiers = ['pk', 'gid']

class PofwSerializer(GeoBusinessSerializer):
    class Meta:
        model = Pofw
        fields = ['gid','osm_id','code','fclass','name','geom']
        geo_field = 'geom'
        identifier = 'gid'
        identifiers = ['pk', 'gid']

class PofwASerializer(GeoBusinessSerializer):
    class Meta:
        model = PofwA
        fields = ['gid','osm_id','code','fclass','name','geom']
        geo_field = 'geom'
        identifier = 'gid'
        identifiers = ['pk', 'gid']

class PoisSerializer(GeoBusinessSerializer):
    class Meta:
        model = Pois
        fields = ['gid','osm_id','code','fclass','name','geom']
        geo_field = 'geom'
        identifier = 'gid'
        identifiers = ['pk', 'gid']

class PoisASerializer(GeoBusinessSerializer):
    class Meta:
        model = PoisA
        fields = ['gid','osm_id','code','fclass','name','geom']
        geo_field = 'geom'
        identifier = 'gid'
        identifiers = ['pk', 'gid']

class RailwaysSerializer(GeoBusinessSerializer):
    class Meta:
        model = Railways
        fields = ['gid','osm_id','code','fclass','name','geom']
        geo_field = 'geom'
        identifier = 'gid'
        identifiers = ['pk', 'gid']

class RoadsSerializer(GeoBusinessSerializer):
    class Meta:
        model = Roads
        fields = ['gid','osm_id','code','fclass','name','ref','oneway','maxspeed','layer','bridge','tunnel','geom']
        geo_field = 'geom'
        identifier = 'gid'
        identifiers = ['pk', 'gid']

class TLmEstadosSerializer(GeoBusinessSerializer):
    class Meta:
        model = TLmEstados
        fields = ['id','cd_geocodigo','nm_estado','nm_regiao','gm_area']
        geo_field = 'gm_area'
        identifier = 'id'
        identifiers = ['pk', 'id']

class TLmMunicipiosSerializer(GeoBusinessSerializer):
    class Meta:
        model = TLmMunicipios
        fields = ['id','cd_geocodigo','nm_municipio','gm_area']
        geo_field = 'gm_area'
        identifier = 'id'
        identifiers = ['pk', 'id']

class TLmViasSerializer(GeoBusinessSerializer):
    class Meta:
        model = TLmVias
        fields = ['id','cd_geo','cd_setor','cd_quadra','cd_face','nm_localidade','nm_tipo_logr','nm_titulo_logr','nm_nome_logr','nm_txtmemo','cd_cep','cd_layer','cd_seq_logr','cd_seq_qface','gm_linha','tp_insumo_img','sit_pre_coleta','origem']
        geo_field = 'gm_linha'
        identifier = 'id'
        identifiers = ['pk', 'id']

class TStEixoLogr2018Serializer(GeoBusinessSerializer):
    class Meta:
        model = TStEixoLogr2018
        fields = ['gid','cd_setor','nm_txtmemo','id','geom','cd_layer','cd_seq_log','tp_insumo_img']
        geo_field = 'geom'
        identifier = 'gid'
        identifiers = ['pk', 'gid']

class TStEixosLogradouroSerializer(GeoBusinessSerializer):
    class Meta:
        model = TStEixosLogradouro
        fields = ['id','cd_layer','cd_setor','nm_txtmemo','cd_seq_logr','tp_insumo_img','gm_linha']
        geo_field = 'gm_linha'
        identifier = 'id'
        identifiers = ['pk', 'id']

class TStVias2018Serializer(GeoBusinessSerializer):
    class Meta:
        model = TStVias2018
        fields = ['gid','cd_layer','cd_setor','cd_quadra','cd_face','cd_geo','cd_seq_log','id','cd_cep','nm_tipo_lo','nm_titulo_field','nm_nome_lo','geom','cd_seq_qfa','nm_txtmemo','nm_localid','origem','sit_pre_co','tp_insumo_img']
        geo_field = 'geom'
        identifier = 'gid'
        identifiers = ['pk', 'gid']

class TrafficSerializer(GeoBusinessSerializer):
    class Meta:
        model = Traffic
        fields = ['gid','osm_id','code','fclass','name','geom']
        geo_field = 'geom'
        identifier = 'gid'
        identifiers = ['pk', 'gid']

class TrafficASerializer(GeoBusinessSerializer):
    class Meta:
        model = TrafficA
        fields = ['gid','osm_id','code','fclass','name','geom']
        geo_field = 'geom'
        identifier = 'gid'
        identifiers = ['pk', 'gid']

class TransportSerializer(GeoBusinessSerializer):
    class Meta:
        model = Transport
        fields = ['gid','osm_id','code','fclass','name','geom']
        geo_field = 'geom'
        identifier = 'gid'
        identifiers = ['pk', 'gid']

class TransportASerializer(GeoBusinessSerializer):
    class Meta:
        model = TransportA
        fields = ['gid','osm_id','code','fclass','name','geom']
        geo_field = 'geom'
        identifier = 'gid'
        identifiers = ['pk', 'gid']

class TrechoFerroviarioSerializer(GeoBusinessSerializer):
    class Meta:
        model = TrechoFerroviario
        fields = ['gid','id_objeto','nome','nomeabrev','geometriaa','codtrechof','posicaorel','tipotrecho','bitola','eletrifica','nrlinhas','emarruamen','jurisdicao','administra','concession','operaciona','cargasupor','situacaofi','id_produto','id_element','cd_insumo_field','nr_insumo_field','nr_insumo0','tx_insumo_field','geom']
        geo_field = 'geom'
        identifier = 'gid'
        identifiers = ['pk', 'gid']

class UnidadeFederacaoSerializer(GeoBusinessSerializer):
    class Meta:
        model = UnidadeFederacao
        fields = ['gid','id_objeto','nome','nomeabrev','geometriaa','sigla','geocodigo','id_produto','id_element','cd_insumo_field','nr_insumo_field','nr_insumo0','tx_insumo_field','geom']
        geo_field = 'geom'
        identifier = 'gid'
        identifiers = ['pk', 'gid']

class WaterSerializer(GeoBusinessSerializer):
    class Meta:
        model = Water
        fields = ['gid','osm_id','code','fclass','name','geom']
        geo_field = 'geom'
        identifier = 'gid'
        identifiers = ['pk', 'gid']

class WaterwaysSerializer(GeoBusinessSerializer):
    class Meta:
        model = Waterways
        fields = ['gid','osm_id','code','fclass','width','name','geom']
        geo_field = 'geom'
        identifier = 'gid'
        identifiers = ['pk', 'gid']



serializers_dict = {}