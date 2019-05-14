from __future__ import unicode_literals

from django.db import connections
from hyper_resource.models import FeatureModel, BusinessModel
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.contrib.gis.db import models


class EixosCete2018(FeatureModel):
    gid = models.AutoField(primary_key=True)
    fid = models.CharField(max_length=80, blank=True, null=True)
    cd_layer = models.CharField(max_length=64, blank=True, null=True)
    cd_setor = models.CharField(max_length=32, blank=True, null=True)
    nm_txtmemo = models.CharField(max_length=200, blank=True, null=True)
    cd_seq_log = models.CharField(max_length=50, blank=True, null=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    tp_insumo_field = models.CharField(db_column='tp_insumo_', max_length=200, blank=True, null=True)  # Field renamed because it ended with '_'.
    geom = models.MultiLineStringField(dim=4, blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = '_eixos_cete_2018'


class Municipios2018(FeatureModel):
    geom = models.MultiPolygonField(blank=True, null=True)
    fid = models.CharField(max_length=200, blank=True, null=True)
    id_0 = models.DecimalField(db_column='ID', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase. Field renamed because of name conflict.
    vl_area_tot = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cd_geocodigo = models.CharField(max_length=7, blank=True, null=True)
    vl_latitudesede = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    vl_longitudesede = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nm_municipio = models.CharField(max_length=64, blank=True, null=True)
    vl_perimetro = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cd_sede = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cd_ano = models.CharField(max_length=50, blank=True, null=True)
    tp_insumo_img = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = '_municipios_2018'


class AldeiaIndigena(FeatureModel):
    gid = models.AutoField(primary_key=True)
    id_objeto = models.IntegerField(blank=True, null=True)
    nome = models.CharField(max_length=254, blank=True, null=True)
    nomeabrev = models.CharField(max_length=254, blank=True, null=True)
    geometriaa = models.CharField(max_length=254, blank=True, null=True)
    codigofuna = models.CharField(max_length=254, blank=True, null=True)
    terraindig = models.CharField(max_length=254, blank=True, null=True)
    etnia = models.CharField(max_length=254, blank=True, null=True)
    id_produto = models.IntegerField(blank=True, null=True)
    id_element = models.IntegerField(blank=True, null=True)
    cd_insumo_field = models.IntegerField(db_column='cd_insumo_', blank=True, null=True)  # Field renamed because it ended with '_'.
    nr_insumo_field = models.IntegerField(db_column='nr_insumo_', blank=True, null=True)  # Field renamed because it ended with '_'.
    nr_insumo0 = models.IntegerField(blank=True, null=True)
    tx_insumo_field = models.CharField(db_column='tx_insumo_', max_length=254, blank=True, null=True)  # Field renamed because it ended with '_'.
    geom = models.PointField(blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 'aldeia_indigena'


class Buildings(FeatureModel):
    gid = models.AutoField(primary_key=True)
    osm_id = models.CharField(max_length=10, blank=True, null=True)
    code = models.SmallIntegerField(blank=True, null=True)
    fclass = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    geom = models.MultiPolygonField(blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 'buildings'


class ComandoInsert(BusinessModel):
    field_column_field = models.TextField(db_column='?column?', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 'comando_insert'


class EixosAl(FeatureModel):
    id = models.BigAutoField(primary_key=True)
    geom = models.MultiLineStringField(blank=True, null=True)
    cd_layer = models.CharField(max_length=32, blank=True, null=True)
    cd_setor = models.CharField(max_length=16, blank=True, null=True)
    nm_txtmemo = models.CharField(max_length=100, blank=True, null=True)
    cd_seq_log = models.CharField(max_length=25, blank=True, null=True)
    tp_insumo_field = models.CharField(db_column='tp_insumo_', max_length=100, blank=True, null=True)  # Field renamed because it ended with '_'.

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 'eixos_al'


class EixosRj(FeatureModel):
    gid = models.AutoField(primary_key=True)
    id = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cd_setor = models.CharField(max_length=16, blank=True, null=True)
    nm_txtmemo = models.CharField(max_length=100, blank=True, null=True)
    chk_linha = models.CharField(max_length=255, blank=True, null=True)
    id1 = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    geom = models.MultiLineStringField(blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 'eixos_rj'


class Landuse(FeatureModel):
    gid = models.AutoField(primary_key=True)
    osm_id = models.CharField(max_length=10, blank=True, null=True)
    code = models.SmallIntegerField(blank=True, null=True)
    fclass = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    geom = models.MultiPolygonField(blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 'landuse'


class MunicipiosAl(FeatureModel):
    id = models.BigAutoField(primary_key=True)
    geom = models.MultiPolygonField(blank=True, null=True)
    vl_area_to = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cd_geocodi = models.CharField(max_length=7, blank=True, null=True)
    vl_latitud = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    vl_longitu = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nm_municip = models.CharField(max_length=64, blank=True, null=True)
    vl_perimet = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cd_sede = models.BigIntegerField(blank=True, null=True)
    cd_ano = models.CharField(max_length=50, blank=True, null=True)
    tp_insumo_field = models.CharField(db_column='tp_insumo_', max_length=100, blank=True, null=True)  # Field renamed because it ended with '_'.

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 'municipios_al'


class MunicipiosRj(FeatureModel):
    id = models.BigAutoField(primary_key=True)
    geom = models.MultiPolygonField(blank=True, null=True)
    vl_area_to = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cd_geocodigo = models.CharField(max_length=7, blank=True, null=True)
    vl_latitud = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    vl_longitu = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nm_municipio = models.CharField(max_length=64, blank=True, null=True)
    vl_perimet = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cd_sede = models.BigIntegerField(blank=True, null=True)
    cd_ano = models.CharField(max_length=50, blank=True, null=True)
    tp_insumo_field = models.CharField(db_column='tp_insumo_', max_length=100, blank=True, null=True)  # Field renamed because it ended with '_'.

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 'municipios_rj'


class Natural(FeatureModel):
    gid = models.AutoField(primary_key=True)
    osm_id = models.CharField(max_length=10, blank=True, null=True)
    code = models.SmallIntegerField(blank=True, null=True)
    fclass = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    geom = models.PointField(blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 'natural'


class NaturalA(FeatureModel):
    gid = models.AutoField(primary_key=True)
    osm_id = models.CharField(max_length=10, blank=True, null=True)
    code = models.SmallIntegerField(blank=True, null=True)
    fclass = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    geom = models.MultiPolygonField(blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 'natural_a'


class Places(FeatureModel):
    gid = models.AutoField(primary_key=True)
    osm_id = models.CharField(max_length=10, blank=True, null=True)
    code = models.SmallIntegerField(blank=True, null=True)
    fclass = models.CharField(max_length=20, blank=True, null=True)
    population = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    geom = models.PointField(blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 'places'


class PlacesA(FeatureModel):
    gid = models.AutoField(primary_key=True)
    osm_id = models.CharField(max_length=10, blank=True, null=True)
    code = models.SmallIntegerField(blank=True, null=True)
    fclass = models.CharField(max_length=20, blank=True, null=True)
    population = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    geom = models.MultiPolygonField(blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 'places_a'


class Pofw(FeatureModel):
    gid = models.AutoField(primary_key=True)
    osm_id = models.CharField(max_length=10, blank=True, null=True)
    code = models.SmallIntegerField(blank=True, null=True)
    fclass = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    geom = models.PointField(blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 'pofw'


class PofwA(FeatureModel):
    gid = models.AutoField(primary_key=True)
    osm_id = models.CharField(max_length=10, blank=True, null=True)
    code = models.SmallIntegerField(blank=True, null=True)
    fclass = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    geom = models.MultiPolygonField(blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 'pofw_a'


class Pois(FeatureModel):
    gid = models.AutoField(primary_key=True)
    osm_id = models.CharField(max_length=10, blank=True, null=True)
    code = models.SmallIntegerField(blank=True, null=True)
    fclass = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    geom = models.PointField(blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 'pois'


class PoisA(FeatureModel):
    gid = models.AutoField(primary_key=True)
    osm_id = models.CharField(max_length=10, blank=True, null=True)
    code = models.SmallIntegerField(blank=True, null=True)
    fclass = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    geom = models.MultiPolygonField(blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 'pois_a'


class Railways(FeatureModel):
    gid = models.AutoField(primary_key=True)
    osm_id = models.CharField(max_length=10, blank=True, null=True)
    code = models.SmallIntegerField(blank=True, null=True)
    fclass = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    geom = models.MultiLineStringField(blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 'railways'


class Roads(FeatureModel):
    gid = models.AutoField(primary_key=True)
    osm_id = models.CharField(max_length=10, blank=True, null=True)
    code = models.SmallIntegerField(blank=True, null=True)
    fclass = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    ref = models.CharField(max_length=20, blank=True, null=True)
    oneway = models.CharField(max_length=1, blank=True, null=True)
    maxspeed = models.SmallIntegerField(blank=True, null=True)
    layer = models.FloatField(blank=True, null=True)
    bridge = models.CharField(max_length=1, blank=True, null=True)
    tunnel = models.CharField(max_length=1, blank=True, null=True)
    geom = models.MultiLineStringField(blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 'roads'


class TLmEstados(FeatureModel):
    id = models.AutoField(primary_key=True)
    cd_geocodigo = models.CharField(max_length=2)
    nm_estado = models.CharField(max_length=50)
    nm_regiao = models.CharField(max_length=20)
    gm_area = models.GeometryField(blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 't_lm_estados'


class TLmMunicipios(FeatureModel):
    id = models.AutoField(primary_key=True)
    cd_geocodigo = models.CharField(max_length=255)
    nm_municipio = models.CharField(max_length=60)
    gm_area = models.GeometryField(blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 't_lm_municipios'


class TLmVias(FeatureModel):
    id = models.AutoField(primary_key=True)
    cd_geo = models.CharField(max_length=25, blank=True, null=True)
    cd_setor = models.CharField(max_length=15, blank=True, null=True)
    cd_quadra = models.CharField(max_length=15, blank=True, null=True)
    cd_face = models.CharField(max_length=15, blank=True, null=True)
    nm_localidade = models.CharField(max_length=60, blank=True, null=True)
    nm_tipo_logr = models.CharField(max_length=30, blank=True, null=True)
    nm_titulo_logr = models.CharField(max_length=50, blank=True, null=True)
    nm_nome_logr = models.CharField(max_length=60, blank=True, null=True)
    nm_txtmemo = models.CharField(max_length=250, blank=True, null=True)
    cd_cep = models.CharField(max_length=8, blank=True, null=True)
    cd_layer = models.CharField(max_length=15, blank=True, null=True)
    cd_seq_logr = models.CharField(max_length=25, blank=True, null=True)
    cd_seq_qface = models.CharField(max_length=25, blank=True, null=True)
    gm_linha = models.GeometryField(blank=True, null=True)
    tp_insumo_img = models.CharField(max_length=100, blank=True, null=True)
    sit_pre_coleta = models.IntegerField(blank=True, null=True)
    origem = models.IntegerField(blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 't_lm_vias'


class TStEixoLogr2018(FeatureModel):
    gid = models.AutoField(primary_key=True)
    cd_setor = models.CharField(max_length=16, blank=True, null=True)
    nm_txtmemo = models.CharField(max_length=100, blank=True, null=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    geom = models.MultiLineStringField(blank=True, null=True)
    cd_layer = models.CharField(max_length=32, blank=True, null=True)
    cd_seq_log = models.CharField(max_length=25, blank=True, null=True)
    tp_insumo_img = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 't_st_eixo_logr2018'


class TStEixosLogradouro(FeatureModel):
    id = models.AutoField(primary_key=True)
    cd_layer = models.CharField(max_length=32, blank=True, null=True)
    cd_setor = models.CharField(max_length=16, blank=True, null=True)
    nm_txtmemo = models.CharField(max_length=100, blank=True, null=True)
    cd_seq_logr = models.CharField(max_length=25, blank=True, null=True)
    tp_insumo_img = models.CharField(max_length=100, blank=True, null=True)
    gm_linha = models.GeometryField(blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 't_st_eixos_logradouro'


class TStVias2018(FeatureModel):
    gid = models.AutoField(primary_key=True)
    cd_layer = models.CharField(max_length=15, blank=True, null=True)
    cd_setor = models.CharField(max_length=15, blank=True, null=True)
    cd_quadra = models.CharField(max_length=15, blank=True, null=True)
    cd_face = models.CharField(max_length=15, blank=True, null=True)
    cd_geo = models.CharField(max_length=45, blank=True, null=True)
    cd_seq_log = models.CharField(max_length=25, blank=True, null=True)
    id = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    cd_cep = models.CharField(max_length=8, blank=True, null=True)
    nm_tipo_lo = models.CharField(max_length=30, blank=True, null=True)
    nm_titulo_field = models.CharField(db_column='nm_titulo_', max_length=50, blank=True, null=True)  # Field renamed because it ended with '_'.
    nm_nome_lo = models.CharField(max_length=255, blank=True, null=True)
    geom = models.MultiLineStringField(blank=True, null=True)
    cd_seq_qfa = models.CharField(max_length=25, blank=True, null=True)
    nm_txtmemo = models.CharField(max_length=255, blank=True, null=True)
    nm_localid = models.CharField(max_length=255, blank=True, null=True)
    origem = models.IntegerField(blank=True, null=True)
    sit_pre_co = models.IntegerField(blank=True, null=True)
    tp_insumo_img = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 't_st_vias2018'


class Traffic(FeatureModel):
    gid = models.AutoField(primary_key=True)
    osm_id = models.CharField(max_length=10, blank=True, null=True)
    code = models.SmallIntegerField(blank=True, null=True)
    fclass = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    geom = models.PointField(blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 'traffic'


class TrafficA(FeatureModel):
    gid = models.AutoField(primary_key=True)
    osm_id = models.CharField(max_length=10, blank=True, null=True)
    code = models.SmallIntegerField(blank=True, null=True)
    fclass = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    geom = models.MultiPolygonField(blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 'traffic_a'


class Transport(FeatureModel):
    gid = models.AutoField(primary_key=True)
    osm_id = models.CharField(max_length=10, blank=True, null=True)
    code = models.SmallIntegerField(blank=True, null=True)
    fclass = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    geom = models.PointField(blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 'transport'


class TransportA(FeatureModel):
    gid = models.AutoField(primary_key=True)
    osm_id = models.CharField(max_length=10, blank=True, null=True)
    code = models.SmallIntegerField(blank=True, null=True)
    fclass = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    geom = models.MultiPolygonField(blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 'transport_a'


class TrechoFerroviario(FeatureModel):
    gid = models.AutoField(primary_key=True)
    id_objeto = models.IntegerField(blank=True, null=True)
    nome = models.CharField(max_length=254, blank=True, null=True)
    nomeabrev = models.CharField(max_length=254, blank=True, null=True)
    geometriaa = models.CharField(max_length=254, blank=True, null=True)
    codtrechof = models.CharField(max_length=254, blank=True, null=True)
    posicaorel = models.CharField(max_length=254, blank=True, null=True)
    tipotrecho = models.CharField(max_length=254, blank=True, null=True)
    bitola = models.CharField(max_length=254, blank=True, null=True)
    eletrifica = models.CharField(max_length=254, blank=True, null=True)
    nrlinhas = models.CharField(max_length=254, blank=True, null=True)
    emarruamen = models.CharField(max_length=254, blank=True, null=True)
    jurisdicao = models.CharField(max_length=254, blank=True, null=True)
    administra = models.CharField(max_length=254, blank=True, null=True)
    concession = models.CharField(max_length=254, blank=True, null=True)
    operaciona = models.CharField(max_length=254, blank=True, null=True)
    cargasupor = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    situacaofi = models.CharField(max_length=254, blank=True, null=True)
    id_produto = models.IntegerField(blank=True, null=True)
    id_element = models.IntegerField(blank=True, null=True)
    cd_insumo_field = models.IntegerField(db_column='cd_insumo_', blank=True, null=True)  # Field renamed because it ended with '_'.
    nr_insumo_field = models.IntegerField(db_column='nr_insumo_', blank=True, null=True)  # Field renamed because it ended with '_'.
    nr_insumo0 = models.IntegerField(blank=True, null=True)
    tx_insumo_field = models.CharField(db_column='tx_insumo_', max_length=254, blank=True, null=True)  # Field renamed because it ended with '_'.
    geom = models.MultiLineStringField(blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 'trecho_ferroviario'


    '''
    def get_model_objects_geobuf(self, view_resource):
        import base64
        with connections["osm"].cursor() as cursor:
            #cursor.execute("SELECT encode(ST_AsGeobuf(q, %s), 'base64') FROM " + view_resource.table_name() + " as q",
            #               [view_resource.geometry_field_name()])

            cursor.execute( "SELECT ST_AsGeobuf(q, %s) FROM " + view_resource.table_name() + " as q", [view_resource.geometry_field_name()] )
            #cursor.execute( "SELECT encode(ST_AsGeobuf(q, %s), %s) FROM " + view_resource.table_name() + " as q", [view_resource.geometry_field_name(), "base64"] )
            rows = cursor.fetchall()
            return rows[0][0]
    '''



class UnidadeFederacao(FeatureModel):
    gid = models.AutoField(primary_key=True)
    id_objeto = models.IntegerField(blank=True, null=True)
    nome = models.CharField(max_length=254, blank=True, null=True)
    nomeabrev = models.CharField(max_length=254, blank=True, null=True)
    geometriaa = models.CharField(max_length=254, blank=True, null=True)
    sigla = models.CharField(max_length=254, blank=True, null=True)
    geocodigo = models.CharField(max_length=254, blank=True, null=True)
    id_produto = models.IntegerField(blank=True, null=True)
    id_element = models.IntegerField(blank=True, null=True)
    cd_insumo_field = models.IntegerField(db_column='cd_insumo_', blank=True, null=True)  # Field renamed because it ended with '_'.
    nr_insumo_field = models.IntegerField(db_column='nr_insumo_', blank=True, null=True)  # Field renamed because it ended with '_'.
    nr_insumo0 = models.IntegerField(blank=True, null=True)
    tx_insumo_field = models.CharField(db_column='tx_insumo_', max_length=254, blank=True, null=True)  # Field renamed because it ended with '_'.
    geom = models.MultiPolygonField(blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 'unidade_federacao'

    '''
    def get_model_objects_geobuf(self, view_resource):
        import base64
        with connection.cursor() as cursor:
            #cursor.execute("SELECT encode(ST_AsGeobuf(q, %s), 'base64') FROM " + view_resource.table_name() + " as q",
            #               [view_resource.geometry_field_name()])

            #cursor.execute( "SELECT ST_AsGeobuf(q, %s) FROM " + view_resource.table_name() + " as q", [view_resource.geometry_field_name()] )
            cursor.execute( "SELECT ST_AsGeobuf(q, %s) FROM (select geom from " + view_resource.table_name() + ") as q", [view_resource.geometry_field_name()] )
            #cursor.execute( "SELECT encode(ST_AsGeobuf(q, %s), %s) FROM " + view_resource.table_name() + " as q", [view_resource.geometry_field_name(), "base64"] )
            rows = cursor.fetchall()
            return rows[0][0]
    '''


class Water(FeatureModel):
    gid = models.AutoField(primary_key=True)
    osm_id = models.CharField(max_length=10, blank=True, null=True)
    code = models.SmallIntegerField(blank=True, null=True)
    fclass = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    geom = models.MultiPolygonField(blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 'water'


class Waterways(FeatureModel):
    gid = models.AutoField(primary_key=True)
    osm_id = models.CharField(max_length=10, blank=True, null=True)
    code = models.SmallIntegerField(blank=True, null=True)
    fclass = models.CharField(max_length=20, blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    geom = models.MultiLineStringField(blank=True, null=True)

    class Meta:
        app_label = 'osm'
        managed = False
        db_table = 'waterways'


class EntryPoint(BusinessModel):
    eixos_cete2018 = models.CharField(max_length=200)
    municipios2018 = models.CharField(max_length=200)
    aldeia_indigena = models.CharField(max_length=200)
    buildings = models.CharField(max_length=200)
    comando_insert = models.CharField(max_length=200)
    eixos_al = models.CharField(max_length=200)
    eixos_rj = models.CharField(max_length=200)
    landuse = models.CharField(max_length=200)
    municipios_al = models.CharField(max_length=200)
    municipios_rj = models.CharField(max_length=200)
    natural = models.CharField(max_length=200)
    natural_a = models.CharField(max_length=200)
    places = models.CharField(max_length=200)
    places_a = models.CharField(max_length=200)
    pofw = models.CharField(max_length=200)
    pofw_a = models.CharField(max_length=200)
    pois = models.CharField(max_length=200)
    pois_a = models.CharField(max_length=200)
    railways = models.CharField(max_length=200)
    roads = models.CharField(max_length=200)
    t_lm_estados = models.CharField(max_length=200)
    t_lm_municipios = models.CharField(max_length=200)
    t_lm_vias = models.CharField(max_length=200)
    t_st_eixo_logr2018 = models.CharField(max_length=200)
    t_st_eixos_logradouro = models.CharField(max_length=200)
    t_st_vias2018 = models.CharField(max_length=200)
    traffic = models.CharField(max_length=200)
    traffic_a = models.CharField(max_length=200)
    transport = models.CharField(max_length=200)
    transport_a = models.CharField(max_length=200)
    trecho_ferroviario = models.CharField(max_length=200)
    unidade_federacao = models.CharField(max_length=200)
    water = models.CharField(max_length=200)
    waterways = models.CharField(max_length=200)