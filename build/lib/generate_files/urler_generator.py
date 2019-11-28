import inspect, sys
import os
import re
import django
from django.db.models import CharField, AutoField, SmallIntegerField, IntegerField, FloatField

ENTRY_POINT_CLASS_NAME = "EntryPoint"
TAB_1X = (' ' * 4)
DJANGO_FIELD_TYPE_FOR_PRIMITIVE_TYPES = {
    CharField: str,
    AutoField: int,
    SmallIntegerField: int,
    IntegerField: int
}

def convert_camel_case_to_hifen(camel_case_string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', camel_case_string)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()

def detect_primary_key_field(fields_of_model_class):
    return next((field for field in fields_of_model_class if field.primary_key), [None])

def is_integer_type(field_type):
    return DJANGO_FIELD_TYPE_FOR_PRIMITIVE_TYPES[field_type] == int

def get_unique_fields_dict(model_class):
    unique_fields_dict = dict()

    for field in model_class._meta.fields:
        if field.unique and not field.primary_key:
            if type(field) not in unique_fields_dict:
                unique_fields_dict.update({type(field): field.name})

    return unique_fields_dict

def unique_fields_urls_snippets(model_class_name, context_name, unique_fields_dict):
    snippet_arr = []

    for field_type, field_name in unique_fields_dict.items():
        if is_integer_type(field_type):
            snippet_arr.append(
                TAB_1X + 'url(r' + "'^" + context_name + '/<int:' + field_name + '>/?$' + "'" + ', views.' +
                model_class_name + 'Detail.as_view(), name=' + "'" + model_class_name + '_detail_unique' + "'" + '),\n')
            snippet_arr.append(
                TAB_1X + 'url(r' + "'^" + context_name + '/(<int:' + field_name + '>/(?P<attributes_functions>.*)/?$' + "'" + ', views.' +
                model_class_name + 'Detail.as_view(), name=' + "'" + model_class_name + '_detail_unique_af' + "'" + '),\n')
        else:
            snippet_arr.append(TAB_1X + 'url(r' + "'^" + context_name + '/(?P<' + field_name + '>[A-Za-z0-9]+)/?$' + "'" + ', views.' +
                       model_class_name + 'Detail.as_view(), name=' + "'" + model_class_name + '_detail_unique' + "'" + '),\n')
            snippet_arr.append(TAB_1X + 'url(r' + "'^" + context_name + '/(?P<' + field_name + '>[A-Za-z0-9]+)/(?P<attributes_functions>.*)/?$' + "'" + ', views.' +
                       model_class_name + 'Detail.as_view(), name=' + "'" + model_class_name + '_detail_unique_af' + "'" + '),\n')
    return snippet_arr

def generate_snippets_to_url(model_class_name, model_class):

    context_name = convert_camel_case_to_hifen(model_class_name) + '-list'
    primary_key_name = 'pk'
    unique_fields_dict = get_unique_fields_dict(model_class)
    arr = []

    # generating urls for primary key requests
    arr.append(TAB_1X + 'url(r' + "'^" + context_name + '/(?P<' + primary_key_name +
               '>[0-9]+)/(?P<attributes_functions>.*)/?$' + "'" + ', views.' +
               model_class_name + 'Detail.as_view(), name=' + "'" + model_class_name + '_detail_af' + "'" + '),\n')
    arr.append(TAB_1X + 'url(r' +"'^"+  context_name +'/(?P<'+ primary_key_name +'>[0-9]+)/?$' +"'"+ ', views.' +
               model_class_name + 'Detail.as_view(), name=' + "'" + model_class_name +'_detail' +"'" + '),\n')

    if unique_fields_dict:
        arr.extend( unique_fields_urls_snippets(model_class_name, context_name, unique_fields_dict) )


    arr.append(TAB_1X + 'url(r' + "'^" + context_name + '/(?P<attributes_functions>.*)/?$' +
               "'" + ', views.' + model_class_name + 'List.as_view(), name=' + "'" + model_class_name + '_list_af' +
               "'" + '),\n')
    arr.append(TAB_1X + 'url(r' + "'^" + context_name + '/?$' + "'" + ', views.' +
               model_class_name + 'List.as_view(), name=' + "'" + model_class_name + '_list' + "'" + '),\n')

    return arr

def imports_str_as_array(a_name):
    arr = []
    arr.append("from django.conf.urls import include, url\n")
    arr.append("from rest_framework.urlpatterns import format_suffix_patterns\n")
    arr.append("from " + a_name + " import views \n\n")
    return arr

def generate_file(package_name, default_name='urls.py'):
    classes_from = [(name, method) for name, method in  inspect.getmembers(sys.modules[package_name + '.models'],inspect.isclass)  if (name != 'BusinessModel' and name != 'FeatureModel' and isinstance(method, django.db.models.base.ModelBase)) ]
    with open(default_name, 'w+') as sr:
        for import_str in imports_str_as_array(package_name):
            sr.write(import_str)
        sr.write('\napp_name="' + package_name + '"\n\n')
        sr.write( 'urlpatterns = format_suffix_patterns((\n')
        sr.write(TAB_1X + 'url(r' +"'"+'^$'+"'"+', views.APIRoot.as_view(), name='+"'"+'api_root'+"'"+'),\n\n')
        sr.write(TAB_1X + 'url(r"^(?P<attributes_functions>count-resource.*$|projection.*$|filter.*$|collect.*$|offset-limit.*$)/?$", views.APIRoot.as_view(), name="api_root_af"), # HARCODED\n\n')
        for model_class_arr in classes_from:

            if model_class_arr[0] == ENTRY_POINT_CLASS_NAME:
                continue

            for str in generate_snippets_to_url(model_class_arr[0], model_class_arr[1]):
                sr.write(str)
            sr.write('\n')
        sr.write('\n))\n')
        sr.close()

if __name__ == "__main__":
    if (len( sys.argv))!= 3:
        print('Usage: python viewer_generator.py django_project_name django_app_name')
        exit()

    prj_name = sys.argv[1]
    app_name = sys.argv[2]
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", prj_name + ".settings")
    django.setup()
    generate_file(app_name)
    print('urls.py  has been generated')