"""
???When you need to control the view access, for each method (get(), options(), head(), post(), put(), delete(), etc),
When you need to control the view access, you need to call the method "request_forward(request)" in dispath method
This method verifies if the request needs token and if the token provide corresponds to an user that has the privileges
needed to complete the request (if is a POST request, the user must have write privilages, for example)

"""
import json
from collections import OrderedDict

from django.db.models import ForeignKey
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from hyper_resource.contexts import EntryPointResourceContext
from hyper_resource.resources.AbstractResource import CONTENT_TYPE_JSON
from hyper_resource.resources.EntryPointResource import NonSpatialEntryPointResource
from user_management.models import *
from user_management.serializers import *
from user_management.contexts import *

from hyper_resource.resources.CollectionResource import CollectionResource
from hyper_resource.resources.NonSpatialResource import NonSpatialResource

class APIRoot(NonSpatialEntryPointResource):

    def get_root_response(self, request, format=None, *args, **kwargs):
        root_links = {
          #'api-resource-list': reverse('user_management:APIResource_list' , request=request, format=format),
          'hyper-user-list': reverse('user_management:HyperUser_list' , request=request, format=format),
          'hyper-user-group-list': reverse('user_management:HyperUserGroup_list' , request=request, format=format),
          #'hyper-user-group-api-resource-list': reverse('user_management:HyperUserGroupAPIResource_list' , request=request, format=format),
          'hyper-user-register': reverse('user_management:HyperUserRegister', request=request, format=format),
          'hyper-user-login': reverse('user_management:HyperUserLogin', request=request, format=format),
        }

        ordered_dict_of_link = OrderedDict(sorted(root_links.items(), key=lambda t: t[0]))
        return ordered_dict_of_link

    '''
    def __init__(self):
        super(APIRoot, self).__init__()
        self.base_context = BaseContext('api-root')

    def options(self, request, *args, **kwargs):
        context = self.base_context.getContextData(request)
        root_links = get_root_response(request)
        context.update(root_links)
        response = Response(context, status=status.HTTP_200_OK, content_type="application/ld+json")
        response = self.base_context.addContext(request, response)
        return response

    def get(self, request, format=None, *args, **kwargs):
        root_links = get_root_response(request)
        response = Response(root_links)
        return self.base_context.addContext(request, response)
    '''

'''
class APIResourceList(CollectionResource):
    queryset = APIResource.objects.all()
    serializer_class = APIResourceSerializer
    contextclassname = 'api-resource-list'
    def initialize_context(self):
        self.context_resource = APIResourceListContext()
        self.context_resource.resource = self

class APIResourceDetail(NonSpatialResource):
    serializer_class = APIResourceSerializer
    contextclassname = 'api-resource-list'
    def initialize_context(self):
        self.context_resource = APIResourceDetailContext()
        self.context_resource.resource = self
'''


class HyperUserList(CollectionResource):
    queryset = HyperUser.objects.all()
    serializer_class = HyperUserSerializer
    contextclassname = 'hyper-user-list'

    def token_is_need(self):
        return True

    '''
    def dispatch(self, request, *args, **kwargs):
        if not self.request_forward(request):
            return HttpResponse(
                json.dumps({'token is not ok or inexistent': 'not enough permission for this operation'}),
                status=status.HTTP_401_UNAUTHORIZED,
                content_type=CONTENT_TYPE_JSON
            )
        return super(HyperUserList, self).dispatch(request, *args, **kwargs)
    '''

    def initialize_context(self):
        self.context_resource = HyperUserListContext()
        self.context_resource.resource = self

class HyperUserDetail(NonSpatialResource):
    serializer_class = HyperUserSerializer
    contextclassname = 'hyper-user-list'

    def initialize_context(self):
        self.context_resource = HyperUserDetailContext()
        self.context_resource.resource = self


class HyperUserGroupList(CollectionResource):
    '''
    Rules:
    Create admingroup (group with all privileges - create, delete, update and read):
        1. By CLI hyper_config.py createadmingroup
        2. A POST request with a admin user token in Authorization header
    '''
    queryset = HyperUserGroup.objects.all()
    serializer_class = HyperUserGroupSerializer
    contextclassname = 'hyper-user-group-list'

    def initialize_context(self):
        self.context_resource = HyperUserGroupListContext()
        self.context_resource.resource = self

class HyperUserGroupDetail(NonSpatialResource):
    serializer_class = HyperUserGroupSerializer
    contextclassname = 'hyper-user-group-list'

    def initialize_context(self):
        self.context_resource = HyperUserGroupDetailContext()
        self.context_resource.resource = self

'''
class HyperUserGroupAPIResourceList(CollectionResource):
    queryset = HyperUserGroupAPIResource.objects.all()
    serializer_class = HyperUserGroupAPIResourceSerializer
    contextclassname = 'hyper-user-group-api-resource-list'
    def initialize_context(self):
        self.context_resource = HyperUserGroupAPIResourceListContext()
        self.context_resource.resource = self

class HyperUserGroupAPIResourceDetail(NonSpatialResource):
    serializer_class = HyperUserGroupAPIResourceSerializer
    contextclassname = 'hyper-user-group-api-resource-list'
    def initialize_context(self):
        self.context_resource = HyperUserGroupAPIResourceDetailContext()
        self.context_resource.resource = self
'''


class HyperUserRegister(CollectionResource):
    '''
    RULES:
    Create a superuser (user inside the group with create, update, delete and read privileges):
        1. By CLI hyper_config.py createsuperuser
        2. A POST request with a admin user token in Authorization header
    Create a default user (user inside group with only read privileges):
        1. created by normal POST request
    '''

    queryset = HyperUser.objects.all()
    serializer_class = HyperUserSerializer
    contextclassname = 'hyper-user-register'

    def __init__(self):
        super(HyperUserRegister, self).__init__()
        self.http_allowed_methods = ['get', 'head', 'options']

    def initialize_context(self):
        self.context_resource = HyperUserRegisterContext()
        self.context_resource.resource = self

    def get(self, request, *args, **kwargs):
        if format == 'jsonld':
            return super(HyperUserRegister, self).get(request, *args, **kwargs)

        if request.build_absolute_uri().endswith('.jsonld'):
            kwargs = self.remove_suffix_from_kwargs(**kwargs)
            self.kwargs = kwargs
            return self.options(request, *args, **kwargs)

        resp = Response(status=status.HTTP_204_NO_CONTENT)
        self.add_base_headers(request, resp)
        return resp

    # todo: hardcoded
    def user_group_is_admin(self, data):
        return data['group'] == 1

    def authorization_is_admin(self, request):
        http_auth = request.META.get('HTTP_AUTHORIZATION') or ''
        if http_auth.startswith('Bearer'):

            a_token = request.META['HTTP_AUTHORIZATION'][7:].strip()
            payload = jwt.decode(a_token, SECRET_KEY, algorithm=self.jwt_algorithm())

            hyper_user_group = HyperUser.objects.get(pk=payload["id"]).group
            # if user group has full privilages (CRUD)
            if hyper_user_group.read and hyper_user_group.create and hyper_user_group.update and hyper_user_group.delete:
                return True

        return False

    def convert_url_to_int(self, url):
        try:
            return int(self.remove_last_slash(url).split("/")[-1])
        except ValueError:
            raise

    def get_fields_name_and_type_dict(self):
        dict = {}
        for field in list(HyperUser().fields()):
            dict[field.name] = type(field)
        return dict

    def convert_foreign_keys_to_int(self, data):
        data_foreign_keys_converted = {}
        hyper_user_field_types_dict = self.get_fields_name_and_type_dict()

        HyperUser().fields()

        for field_name, value in data.items():
            if hyper_user_field_types_dict[field_name] == ForeignKey:
                data_foreign_keys_converted[field_name] = value if type(value) == int else self.convert_url_to_int(value)
            else:
                data_foreign_keys_converted[field_name] = value
        return data_foreign_keys_converted

    def get_related_object(self, foreign_key_model_field, related_object_pk):
        if type(related_object_pk) != int:
            related_object_pk = int(self.remove_last_slash(related_object_pk).split("/")[-1])
        related_field = [field for field in foreign_key_model_field._related_fields[0] if type(field) != ForeignKey][0]
        return related_field.model.objects.get(pk=related_object_pk)

    def append_related_objects(self, data):
        model_fields = HyperUser().fields()
        data_with_related_object = {}

        for field_name, value in data.items():
            for model_field in model_fields:
                if field_name == model_field.name:
                    if type(model_field) == ForeignKey:
                        data_with_related_object[field_name] = self.get_related_object(model_field, value)
                    else:
                        data_with_related_object[field_name] = value

        return data_with_related_object

    def post(self, request, *args, **kwargs):
        #data = self.append_related_objects(request.data)
        data_with_foreign_key = self.convert_foreign_keys_to_int(request.data)
        #data_with_related_object = self.append_related_objects(request.data)
        serializer = self.serializer_class(data=data_with_foreign_key, context={'request': request})

        if serializer.is_valid(): # the validation is done with integers in foreign keys
            if self.user_group_is_admin(data_with_foreign_key):
                try:
                    if not self.authorization_is_admin(request):
                        error_message = {"Not enough privilages": "Your account does't have all the permissions: READ, WRITE, UPDATE and DELETE"}
                        return Response(data=error_message, status=status.HTTP_401_UNAUTHORIZED)

                except jwt.InvalidTokenError:
                    error_message = {"Token error": "This is not a valid token"}
                    return Response(data=error_message, status=status.HTTP_401_UNAUTHORIZED)

            obj =  serializer.save()
            self.object_model = obj

            response = self.basic_post(request)
            response['x-access-token'] = self.object_model.getToken()
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    '''
    def post(self, request, *args, **kwargs):
        resp = super(HyperUserRegister, self).post(request, *args, **kwargs)
        if resp.status_code == 200:
            resp['x-access-token'] = self.object_model.getToken()
        return resp
    '''

    def head(self, request, *args, **kwargs):
        resp = Response(data={}, status=status.HTTP_200_OK, content_type=self.default_content_type())
        self.add_base_headers(request, resp)
        return resp

class HyperUserLogin(CollectionResource):
    '''
    OBS: For login view, the field "group" must be required=False
    '''

    queryset = HyperUser.objects.all()
    serializer_class = HyperUserSerializer
    contextclassname = 'hyper-user-login'

    def __init__(self):
        super(HyperUserLogin, self).__init__()
        self.http_allowed_methods = ['get', 'head', 'options']

    def initialize_context(self):
        self.context_resource = HyperUserLoginContext()
        self.context_resource.resource = self

    def post(self, request, *args, **kwargs):
        res = HyperUser.getOneOrNone(request.data['user_name'], request.data['password'])

        if res is None:
            res = Response(status=status.HTTP_401_UNAUTHORIZED, content_type='application/json')
            res['WWW-Authenticate'] = 'Bearer'
            return res
        response = Response(status=status.HTTP_201_CREATED, content_type='application/json')
        response['Content-Location'] = request.path + str(res.id) + '/'
        response['x-access-token'] = res.getToken()
        return response

    def get(self, request, *args, **kwargs):
        if format == 'jsonld':
            return super(HyperUserLogin, self).get(request, *args, **kwargs)

        if request.build_absolute_uri().endswith('.jsonld'):
            kwargs = self.remove_suffix_from_kwargs(**kwargs)
            self.kwargs = kwargs
            return self.options(request, *args, **kwargs)
        resp = Response(status=status.HTTP_204_NO_CONTENT)
        self.add_base_headers(request, resp)
        return resp

    def head(self, request, *args, **kwargs):
        resp = Response(data={}, status=status.HTTP_200_OK, content_type=self.default_content_type())
        self.add_base_headers(request, resp)
        return resp