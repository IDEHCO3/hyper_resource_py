import requests
import xmltodict
dic_capability = {}
dic_capability['ana'] = 'http://wms.snirh.gov.br/arcgis/services/SNIRH/2016/MapServer/WMSServer?service=wms&version=1.3.0&request=GetCapabilities'
dic_capability['anatel'] = 'http://sistemas.anatel.gov.br/geoserver/ANATEL/ows?service=wms&version=1.3.0&request=GetCapabilities'
dic_capability['bndes'] = 'https://geoservicos.inde.gov.br/geoserver/BNDES/ows?service=wms&version=1.3.0&request=GetCapabilities'
dic_capability['cmr.funai'] =  'http://cmr.funai.gov.br/geoserver/ows?service=wms&version=1.3.0&request=GetCapabilities'
dic_capability['dsg'] = 'http://www.geoportal.eb.mil.br/mapcache3857?service=wms&version=1.3.0&request=GetCapabilities'
dic_capability['cnpa.embrapa']= 'http://geoinfo.cnpa.embrapa.br/geoserver/ows?service=wms&version=1.3.0&request=GetCapabilities'
dic_capability['cnpf.embrapa']='http://geoinfo.cnpf.embrapa.br/geoserver/ows?service=wms&version=1.3.0&request=GetCapabilities'
dic_capability['cnpm.embrapa'] = 'http://geoinfo.cnpm.embrapa.br/geoserver/ows?service=wms&version=1.3.0&request=GetCapabilities'
dic_capability['cnps.embrapa'] = 'http://geoinfo.cnps.embrapa.br/geoserver/ows?service=wms&version=1.3.0&request=GetCapabilities'
dic_capability['ibge'] = 'https://geoservicos.ibge.gov.br/geoserver/ows?service=wms&version=1.3.0&request=GetCapabilities'
dic_capability['siscom.ibama'] = 'http://siscom.ibama.gov.br/geoserver/ows?service=wms&version=1.3.0&request=GetCapabilities'
dic_capability['aisweb.decea'] = 'http://www.aisweb.decea.gov.br/geoserver/ICA/wms?service=wms&version=1.3.0&request=GetCapabilities'
dic_capability['iphan'] = 'http://portal.iphan.gov.br/geoserver/ows?service=wms&version=1.3.0&request=GetCapabilities'
dic_capability['inpe'] = 'http://terrabrasilis.dpi.inpe.br/geoserver/ows?service=wms&version=1.3.0&request=GetCapabilities'
dic_capability['mpog.economia'] = 'https://geoservicos.inde.gov.br/geoserver/MPOG/ows?service=wms&version=1.3.0&request=GetCapabilities'
dic_capability['mdic.economia'] = 'https://geoservicos.inde.gov.br/geoserver/MDIC/ows?service=wms&version=1.3.0&request=GetCapabilities'
dic_capability['ods'] = 'https://geoservicos.ibge.gov.br/geoserver/ODS/ows?service=wms&version=1.3.0&request=GetCapabilities'
dic_capability['snpm.mfdh'] = 'https://geoservicos.inde.gov.br/geoserver/SPM/ows?service=wms&version=1.3.0&request=GetCapabilities'
dic_capability['sfb'] = 'https://sistemas.florestal.gov.br/geoserver/ows?service=wms&version=1.3.0&request=GetCapabilities'
dic_capability['celepar.pr'] = 'http://geoserver.pr.gov.br/geoserver/ows?service=wms&version=1.3.0&request=GetCapabilities'
dic_capability['datageo.ambiente.sp'] = 'http://datageo.ambiente.sp.gov.br/geoserver/ows?service=wms&version=1.3.0&request=GetCapabilities'
#dic_capability['ide.emplasa.sp'] = 'https://ide.emplasa.sp.gov.br/geoserver/ows?service=wms&version=1.3.0&request=GetCapabilities'
dic_capability['geobases.es'] = 'http://geoserver.geobases.es.gov.br/geoserver/ows?service=wms&version=1.3.0&request=GetCapabilities'
dic_capability['inea.rj'] = 'https://geoservicos.inde.gov.br/geoserver/INEA/ows?service=wms&version=1.3.0&request=GetCapabilities'
dic_capability['seplande.al'] = 'http://geo.seplande.al.gov.br/teogc/terraogcwms.cgi?service=wms&version=1.3.0&request=GetCapabilities'
dic_capability['bhmapogcbase.pbh'] =  'http://bhmapogcbase.pbh.gov.br/bhmapogcbase/ide_bhgeo/ows?service=wms&version=1.3.0&request=GetCapabilities'
dic_capability['ufabc'] =  'https://geoservicos.inde.gov.br/geoserver/UFABC/ows?service=wms&version=1.3.0&request=GetCapabilities'

def wms_get_capabilities(url):
    res = requests.get(url, verify=False)
    xpars = xmltodict.parse(res.text)
    return xpars['WMS_Capabilities']['Capability']['Layer']['Layer']

def all_layers_from_get_capabilities():
    layers_capabilities = []
    for key, value in dic_capability.items():
        res = requests.get(value, verify=False)
        xpars = xmltodict.parse(res.text)
        layers_capabilities + xpars['WMS_Capabilities']['Capability']['Layer']['Layer']
    return layers_capabilities

def len_all_layers_from_get_capabilities():
    return len(all_layers_from_get_capabilities())