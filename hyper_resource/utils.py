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

if ENABLE_COMPLEX_REQUESTS:
    print ('***************************************************************************************************************************')
    print("** WARNING: Complex requests is enabled                                                                                  **")
    print("** Certify that your API isn't using the follow caracter(s) for specific purposes:                                       **")
    print("** '!' (exclamation point)                                                                                               **")
    print ('***************************************************************************************************************************')