import re

SECRET_KEY = '!ijb)p^wxprqdccf7*kxzu6l^&sf%_+w@!$6e#yl^^47i3j0f6asdfg' # SECRET_KEY from user_management.models

HTTP_IF_NONE_MATCH = 'HTTP_IF_NONE_MATCH'
HTTP_IF_MATCH = 'HTTP_IF_MATCH'
HTTP_IF_UNMODIFIED_SINCE = 'HTTP_IF_UNMODIFIED_SINCE'
HTTP_IF_MODIFIED_SINCE = 'HTTP_IF_MODIFIED_SINCE'
HTTP_ACCEPT = 'HTTP_ACCEPT'
CONTENT_TYPE = 'CONTENT_TYPE'
ETAG = 'Etag'
CONTENT_TYPE_GEOJSON = "application/geo+json"
CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_LD_JSON = "application/ld+json"
CONTENT_TYPE_OCTET_STREAM = "application/octet-stream"
CONTENT_TYPE_IMAGE_PNG = "image/png"
CONTENT_TYPE_IMAGE_TIFF = "image/tiff"

HYPER_RESOURCE_CONTEXT = 'http://www.w3.org/ns/json-hr#context'
HYPER_RESOURCE_CONTENT_TYPE = 'application/hr+json'
HYPER_RESOURCE_EXTENSION = '.jsonhr'

SUPPORTED_CONTENT_TYPES = (CONTENT_TYPE_GEOJSON, CONTENT_TYPE_JSON,CONTENT_TYPE_LD_JSON, CONTENT_TYPE_OCTET_STREAM, CONTENT_TYPE_IMAGE_PNG, CONTENT_TYPE_IMAGE_TIFF, HYPER_RESOURCE_CONTENT_TYPE)

IMAGE_RESOURCE_TYPE = "Image"

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
LIST_METHODS = ['GET', 'HEAD', 'OPTIONS', 'POST']
ELEMENT_METHODS = ['GET', 'HEAD', 'OPTIONS', 'PUT', 'DELETE']

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'content-location',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'link',
)

CORS_EXPOSE_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'content-location',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'x-access-token',
    'access-control-allow-origin',
    'link',
]

ENABLE_COMPLEX_REQUESTS = True
PARAM_SEPARATOR = "&"
LIST_ELEMENTS_SEPARATOR = ","

HYPER_RESOURCE_SUPPORTED_OPERATIONS_LABEL = 'hydra:supportedOperations'

if ENABLE_COMPLEX_REQUESTS:
    print ('***************************************************************************************************************************')
    print("** WARNING: Complex requests is enabled                                                                                  **")
    print("** Certify that your API isn't using the follow caracter(s) for specific purposes:                                       **")
    print("** '!' (exclamation point)                                                                                               **")
    print ('***************************************************************************************************************************')

def remove_last_slash(url_as_str):
    url = url_as_str.strip()

    if url_as_str is None or url_as_str == "":
        return url_as_str

    url = url[:-1] if url[-1] == '*' else url
    return url[:-1] if url.endswith('/') else url

def path_has_url(attributes_functions_str_url):
    return attributes_functions_str_url.find('http:') > -1 \
           or attributes_functions_str_url.find('https:') > -1 \
           or attributes_functions_str_url.find('www.') > -1

def get_url_arr_from_arr_of_tuples(arr_of_tuples):
    url_as_arr = []
    for url_tuple in arr_of_tuples:
        url_arr = list(url_tuple)
        url = [remove_last_slash(url) for url in url_arr if url != ''][0]
        url_as_arr.append(url)
    return url_as_arr

class OperationNotRecognized(Exception):
    pass

def operation_with_url_splitted_by_slash(operation_str):
    att_functions_str_url = operation_str
    exp = r'(?=https{0,1}:.+?\*)(https{0,1}:.+?\*)|(https{0,1}:.+?\/?$)'
    url_as_arr_of_tuples = re.findall(exp, att_functions_str_url, re.IGNORECASE)

    url_as_arr = get_url_arr_from_arr_of_tuples(url_as_arr_of_tuples)

    token = '_*+_TOKEN__$URL-#_Num:'
    for index, url_str in enumerate(url_as_arr):
        att_functions_str_url = att_functions_str_url.replace(url_str, token + str(index), 1)# + '/*', 1)
    att_functions_str_url_as_array = att_functions_str_url.split('/')
    for idx, url_str in enumerate(url_as_arr):
        att_functions_str_url_as_array[att_functions_str_url_as_array.index(token + str(idx))] = url_str if url_str[-1] not in ['*', '/'] else url_str[:-1]

    return att_functions_str_url_as_array if att_functions_str_url_as_array[-1] != '*' else att_functions_str_url_as_array[:-1]