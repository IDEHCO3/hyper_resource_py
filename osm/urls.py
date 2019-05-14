from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from osm import views 


app_name="osm"

urlpatterns = format_suffix_patterns((
    url(r'^$', views.APIRoot.as_view(), name='api_root'),

    url(r"^(?P<attributes_functions>count-resource.*$|projection.*$|filter.*$|collect.*$|offset-limit.*$)/?$", views.APIRoot.as_view(), name="api_root_af"), # HARCODED

    url(r'^aldeia-indigena-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.AldeiaIndigenaDetail.as_view(), name='AldeiaIndigena_detail_af'),
    url(r'^aldeia-indigena-list/(?P<pk>[0-9]+)/?$', views.AldeiaIndigenaDetail.as_view(), name='AldeiaIndigena_detail'),
    url(r'^aldeia-indigena-list/(?P<attributes_functions>.*)/?$', views.AldeiaIndigenaList.as_view(), name='AldeiaIndigena_list_af'),
    url(r'^aldeia-indigena-list/?$', views.AldeiaIndigenaList.as_view(), name='AldeiaIndigena_list'),

    url(r'^buildings-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.BuildingsDetail.as_view(), name='Buildings_detail_af'),
    url(r'^buildings-list/(?P<pk>[0-9]+)/?$', views.BuildingsDetail.as_view(), name='Buildings_detail'),
    url(r'^buildings-list/(?P<attributes_functions>.*)/?$', views.BuildingsList.as_view(), name='Buildings_list_af'),
    url(r'^buildings-list/?$', views.BuildingsList.as_view(), name='Buildings_list'),

    url(r'^comando-insert-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.ComandoInsertDetail.as_view(), name='ComandoInsert_detail_af'),
    url(r'^comando-insert-list/(?P<pk>[0-9]+)/?$', views.ComandoInsertDetail.as_view(), name='ComandoInsert_detail'),
    url(r'^comando-insert-list/(?P<attributes_functions>.*)/?$', views.ComandoInsertList.as_view(), name='ComandoInsert_list_af'),
    url(r'^comando-insert-list/?$', views.ComandoInsertList.as_view(), name='ComandoInsert_list'),

    url(r'^eixos-al-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.EixosAlDetail.as_view(), name='EixosAl_detail_af'),
    url(r'^eixos-al-list/(?P<pk>[0-9]+)/?$', views.EixosAlDetail.as_view(), name='EixosAl_detail'),
    url(r'^eixos-al-list/(?P<attributes_functions>.*)/?$', views.EixosAlList.as_view(), name='EixosAl_list_af'),
    url(r'^eixos-al-list/?$', views.EixosAlList.as_view(), name='EixosAl_list'),

    url(r'^eixos-cete2018-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.EixosCete2018Detail.as_view(), name='EixosCete2018_detail_af'),
    url(r'^eixos-cete2018-list/(?P<pk>[0-9]+)/?$', views.EixosCete2018Detail.as_view(), name='EixosCete2018_detail'),
    url(r'^eixos-cete2018-list/(?P<attributes_functions>.*)/?$', views.EixosCete2018List.as_view(), name='EixosCete2018_list_af'),
    url(r'^eixos-cete2018-list/?$', views.EixosCete2018List.as_view(), name='EixosCete2018_list'),

    url(r'^eixos-rj-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.EixosRjDetail.as_view(), name='EixosRj_detail_af'),
    url(r'^eixos-rj-list/(?P<pk>[0-9]+)/?$', views.EixosRjDetail.as_view(), name='EixosRj_detail'),
    url(r'^eixos-rj-list/(?P<attributes_functions>.*)/?$', views.EixosRjList.as_view(), name='EixosRj_list_af'),
    url(r'^eixos-rj-list/?$', views.EixosRjList.as_view(), name='EixosRj_list'),

    url(r'^landuse-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.LanduseDetail.as_view(), name='Landuse_detail_af'),
    url(r'^landuse-list/(?P<pk>[0-9]+)/?$', views.LanduseDetail.as_view(), name='Landuse_detail'),
    url(r'^landuse-list/(?P<attributes_functions>.*)/?$', views.LanduseList.as_view(), name='Landuse_list_af'),
    url(r'^landuse-list/?$', views.LanduseList.as_view(), name='Landuse_list'),

    url(r'^municipios2018-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.Municipios2018Detail.as_view(), name='Municipios2018_detail_af'),
    url(r'^municipios2018-list/(?P<pk>[0-9]+)/?$', views.Municipios2018Detail.as_view(), name='Municipios2018_detail'),
    url(r'^municipios2018-list/(?P<attributes_functions>.*)/?$', views.Municipios2018List.as_view(), name='Municipios2018_list_af'),
    url(r'^municipios2018-list/?$', views.Municipios2018List.as_view(), name='Municipios2018_list'),

    url(r'^municipios-al-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.MunicipiosAlDetail.as_view(), name='MunicipiosAl_detail_af'),
    url(r'^municipios-al-list/(?P<pk>[0-9]+)/?$', views.MunicipiosAlDetail.as_view(), name='MunicipiosAl_detail'),
    url(r'^municipios-al-list/(?P<attributes_functions>.*)/?$', views.MunicipiosAlList.as_view(), name='MunicipiosAl_list_af'),
    url(r'^municipios-al-list/?$', views.MunicipiosAlList.as_view(), name='MunicipiosAl_list'),

    url(r'^municipios-rj-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.MunicipiosRjDetail.as_view(), name='MunicipiosRj_detail_af'),
    url(r'^municipios-rj-list/(?P<pk>[0-9]+)/?$', views.MunicipiosRjDetail.as_view(), name='MunicipiosRj_detail'),
    url(r'^municipios-rj-list/(?P<attributes_functions>.*)/?$', views.MunicipiosRjList.as_view(), name='MunicipiosRj_list_af'),
    url(r'^municipios-rj-list/?$', views.MunicipiosRjList.as_view(), name='MunicipiosRj_list'),

    url(r'^natural-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.NaturalDetail.as_view(), name='Natural_detail_af'),
    url(r'^natural-list/(?P<pk>[0-9]+)/?$', views.NaturalDetail.as_view(), name='Natural_detail'),
    url(r'^natural-list/(?P<attributes_functions>.*)/?$', views.NaturalList.as_view(), name='Natural_list_af'),
    url(r'^natural-list/?$', views.NaturalList.as_view(), name='Natural_list'),

    url(r'^natural-a-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.NaturalADetail.as_view(), name='NaturalA_detail_af'),
    url(r'^natural-a-list/(?P<pk>[0-9]+)/?$', views.NaturalADetail.as_view(), name='NaturalA_detail'),
    url(r'^natural-a-list/(?P<attributes_functions>.*)/?$', views.NaturalAList.as_view(), name='NaturalA_list_af'),
    url(r'^natural-a-list/?$', views.NaturalAList.as_view(), name='NaturalA_list'),

    url(r'^places-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.PlacesDetail.as_view(), name='Places_detail_af'),
    url(r'^places-list/(?P<pk>[0-9]+)/?$', views.PlacesDetail.as_view(), name='Places_detail'),
    url(r'^places-list/(?P<attributes_functions>.*)/?$', views.PlacesList.as_view(), name='Places_list_af'),
    url(r'^places-list/?$', views.PlacesList.as_view(), name='Places_list'),

    url(r'^places-a-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.PlacesADetail.as_view(), name='PlacesA_detail_af'),
    url(r'^places-a-list/(?P<pk>[0-9]+)/?$', views.PlacesADetail.as_view(), name='PlacesA_detail'),
    url(r'^places-a-list/(?P<attributes_functions>.*)/?$', views.PlacesAList.as_view(), name='PlacesA_list_af'),
    url(r'^places-a-list/?$', views.PlacesAList.as_view(), name='PlacesA_list'),

    url(r'^pofw-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.PofwDetail.as_view(), name='Pofw_detail_af'),
    url(r'^pofw-list/(?P<pk>[0-9]+)/?$', views.PofwDetail.as_view(), name='Pofw_detail'),
    url(r'^pofw-list/(?P<attributes_functions>.*)/?$', views.PofwList.as_view(), name='Pofw_list_af'),
    url(r'^pofw-list/?$', views.PofwList.as_view(), name='Pofw_list'),

    url(r'^pofw-a-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.PofwADetail.as_view(), name='PofwA_detail_af'),
    url(r'^pofw-a-list/(?P<pk>[0-9]+)/?$', views.PofwADetail.as_view(), name='PofwA_detail'),
    url(r'^pofw-a-list/(?P<attributes_functions>.*)/?$', views.PofwAList.as_view(), name='PofwA_list_af'),
    url(r'^pofw-a-list/?$', views.PofwAList.as_view(), name='PofwA_list'),

    url(r'^pois-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.PoisDetail.as_view(), name='Pois_detail_af'),
    url(r'^pois-list/(?P<pk>[0-9]+)/?$', views.PoisDetail.as_view(), name='Pois_detail'),
    url(r'^pois-list/(?P<attributes_functions>.*)/?$', views.PoisList.as_view(), name='Pois_list_af'),
    url(r'^pois-list/?$', views.PoisList.as_view(), name='Pois_list'),

    url(r'^pois-a-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.PoisADetail.as_view(), name='PoisA_detail_af'),
    url(r'^pois-a-list/(?P<pk>[0-9]+)/?$', views.PoisADetail.as_view(), name='PoisA_detail'),
    url(r'^pois-a-list/(?P<attributes_functions>.*)/?$', views.PoisAList.as_view(), name='PoisA_list_af'),
    url(r'^pois-a-list/?$', views.PoisAList.as_view(), name='PoisA_list'),

    url(r'^railways-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.RailwaysDetail.as_view(), name='Railways_detail_af'),
    url(r'^railways-list/(?P<pk>[0-9]+)/?$', views.RailwaysDetail.as_view(), name='Railways_detail'),
    url(r'^railways-list/(?P<attributes_functions>.*)/?$', views.RailwaysList.as_view(), name='Railways_list_af'),
    url(r'^railways-list/?$', views.RailwaysList.as_view(), name='Railways_list'),

    url(r'^roads-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.RoadsDetail.as_view(), name='Roads_detail_af'),
    url(r'^roads-list/(?P<pk>[0-9]+)/?$', views.RoadsDetail.as_view(), name='Roads_detail'),
    url(r'^roads-list/(?P<attributes_functions>.*)/?$', views.RoadsList.as_view(), name='Roads_list_af'),
    url(r'^roads-list/?$', views.RoadsList.as_view(), name='Roads_list'),

    url(r'^t-lm-estados-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.TLmEstadosDetail.as_view(), name='TLmEstados_detail_af'),
    url(r'^t-lm-estados-list/(?P<pk>[0-9]+)/?$', views.TLmEstadosDetail.as_view(), name='TLmEstados_detail'),
    url(r'^t-lm-estados-list/(?P<attributes_functions>.*)/?$', views.TLmEstadosList.as_view(), name='TLmEstados_list_af'),
    url(r'^t-lm-estados-list/?$', views.TLmEstadosList.as_view(), name='TLmEstados_list'),

    url(r'^t-lm-municipios-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.TLmMunicipiosDetail.as_view(), name='TLmMunicipios_detail_af'),
    url(r'^t-lm-municipios-list/(?P<pk>[0-9]+)/?$', views.TLmMunicipiosDetail.as_view(), name='TLmMunicipios_detail'),
    url(r'^t-lm-municipios-list/(?P<attributes_functions>.*)/?$', views.TLmMunicipiosList.as_view(), name='TLmMunicipios_list_af'),
    url(r'^t-lm-municipios-list/?$', views.TLmMunicipiosList.as_view(), name='TLmMunicipios_list'),

    url(r'^t-lm-vias-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.TLmViasDetail.as_view(), name='TLmVias_detail_af'),
    url(r'^t-lm-vias-list/(?P<pk>[0-9]+)/?$', views.TLmViasDetail.as_view(), name='TLmVias_detail'),
    url(r'^t-lm-vias-list/(?P<attributes_functions>.*)/?$', views.TLmViasList.as_view(), name='TLmVias_list_af'),
    url(r'^t-lm-vias-list/?$', views.TLmViasList.as_view(), name='TLmVias_list'),

    url(r'^t-st-eixo-logr2018-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.TStEixoLogr2018Detail.as_view(), name='TStEixoLogr2018_detail_af'),
    url(r'^t-st-eixo-logr2018-list/(?P<pk>[0-9]+)/?$', views.TStEixoLogr2018Detail.as_view(), name='TStEixoLogr2018_detail'),
    url(r'^t-st-eixo-logr2018-list/(?P<attributes_functions>.*)/?$', views.TStEixoLogr2018List.as_view(), name='TStEixoLogr2018_list_af'),
    url(r'^t-st-eixo-logr2018-list/?$', views.TStEixoLogr2018List.as_view(), name='TStEixoLogr2018_list'),

    url(r'^t-st-eixos-logradouro-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.TStEixosLogradouroDetail.as_view(), name='TStEixosLogradouro_detail_af'),
    url(r'^t-st-eixos-logradouro-list/(?P<pk>[0-9]+)/?$', views.TStEixosLogradouroDetail.as_view(), name='TStEixosLogradouro_detail'),
    url(r'^t-st-eixos-logradouro-list/(?P<attributes_functions>.*)/?$', views.TStEixosLogradouroList.as_view(), name='TStEixosLogradouro_list_af'),
    url(r'^t-st-eixos-logradouro-list/?$', views.TStEixosLogradouroList.as_view(), name='TStEixosLogradouro_list'),

    url(r'^t-st-vias2018-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.TStVias2018Detail.as_view(), name='TStVias2018_detail_af'),
    url(r'^t-st-vias2018-list/(?P<pk>[0-9]+)/?$', views.TStVias2018Detail.as_view(), name='TStVias2018_detail'),
    url(r'^t-st-vias2018-list/(?P<attributes_functions>.*)/?$', views.TStVias2018List.as_view(), name='TStVias2018_list_af'),
    url(r'^t-st-vias2018-list/?$', views.TStVias2018List.as_view(), name='TStVias2018_list'),

    url(r'^traffic-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.TrafficDetail.as_view(), name='Traffic_detail_af'),
    url(r'^traffic-list/(?P<pk>[0-9]+)/?$', views.TrafficDetail.as_view(), name='Traffic_detail'),
    url(r'^traffic-list/(?P<attributes_functions>.*)/?$', views.TrafficList.as_view(), name='Traffic_list_af'),
    url(r'^traffic-list/?$', views.TrafficList.as_view(), name='Traffic_list'),

    url(r'^traffic-a-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.TrafficADetail.as_view(), name='TrafficA_detail_af'),
    url(r'^traffic-a-list/(?P<pk>[0-9]+)/?$', views.TrafficADetail.as_view(), name='TrafficA_detail'),
    url(r'^traffic-a-list/(?P<attributes_functions>.*)/?$', views.TrafficAList.as_view(), name='TrafficA_list_af'),
    url(r'^traffic-a-list/?$', views.TrafficAList.as_view(), name='TrafficA_list'),

    url(r'^transport-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.TransportDetail.as_view(), name='Transport_detail_af'),
    url(r'^transport-list/(?P<pk>[0-9]+)/?$', views.TransportDetail.as_view(), name='Transport_detail'),
    url(r'^transport-list/(?P<attributes_functions>.*)/?$', views.TransportList.as_view(), name='Transport_list_af'),
    url(r'^transport-list/?$', views.TransportList.as_view(), name='Transport_list'),

    url(r'^transport-a-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.TransportADetail.as_view(), name='TransportA_detail_af'),
    url(r'^transport-a-list/(?P<pk>[0-9]+)/?$', views.TransportADetail.as_view(), name='TransportA_detail'),
    url(r'^transport-a-list/(?P<attributes_functions>.*)/?$', views.TransportAList.as_view(), name='TransportA_list_af'),
    url(r'^transport-a-list/?$', views.TransportAList.as_view(), name='TransportA_list'),

    url(r'^trecho-ferroviario-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.TrechoFerroviarioDetail.as_view(), name='TrechoFerroviario_detail_af'),
    url(r'^trecho-ferroviario-list/(?P<pk>[0-9]+)/?$', views.TrechoFerroviarioDetail.as_view(), name='TrechoFerroviario_detail'),
    url(r'^trecho-ferroviario-list/(?P<attributes_functions>.*)/?$', views.TrechoFerroviarioList.as_view(), name='TrechoFerroviario_list_af'),
    url(r'^trecho-ferroviario-list/?$', views.TrechoFerroviarioList.as_view(), name='TrechoFerroviario_list'),

    url(r'^unidade-federacao-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.UnidadeFederacaoDetail.as_view(), name='UnidadeFederacao_detail_af'),
    url(r'^unidade-federacao-list/(?P<pk>[0-9]+)/?$', views.UnidadeFederacaoDetail.as_view(), name='UnidadeFederacao_detail'),
    url(r'^unidade-federacao-list/(?P<attributes_functions>.*)/?$', views.UnidadeFederacaoList.as_view(), name='UnidadeFederacao_list_af'),
    url(r'^unidade-federacao-list/?$', views.UnidadeFederacaoList.as_view(), name='UnidadeFederacao_list'),

    url(r'^water-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.WaterDetail.as_view(), name='Water_detail_af'),
    url(r'^water-list/(?P<pk>[0-9]+)/?$', views.WaterDetail.as_view(), name='Water_detail'),
    url(r'^water-list/(?P<attributes_functions>.*)/?$', views.WaterList.as_view(), name='Water_list_af'),
    url(r'^water-list/?$', views.WaterList.as_view(), name='Water_list'),

    url(r'^waterways-list/(?P<pk>[0-9]+)/(?P<attributes_functions>.*)/?$', views.WaterwaysDetail.as_view(), name='Waterways_detail_af'),
    url(r'^waterways-list/(?P<pk>[0-9]+)/?$', views.WaterwaysDetail.as_view(), name='Waterways_detail'),
    url(r'^waterways-list/(?P<attributes_functions>.*)/?$', views.WaterwaysList.as_view(), name='Waterways_list_af'),
    url(r'^waterways-list/?$', views.WaterwaysList.as_view(), name='Waterways_list'),


))
