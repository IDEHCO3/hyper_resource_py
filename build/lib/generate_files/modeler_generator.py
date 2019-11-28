import inspect, sys
import os
import re
import django

#from django.contrib.gis.db import models
#from hyper_resource.models import FeatureModel

ENTRY_POINT_CLASS_NAME = "EntryPoint"
TAB_1X = (4 * " ")
NON_ASCII_CHAR_REPLACER = "0"
EQUAL_CHARACTER = "="
LINE_COMMENT_INIT_CHAR = "#"

def is_spatial(model_class):
    from django.contrib.gis.db.models.fields import GeometryField
    
    for field in model_class._meta.get_fields():
      if isinstance(field, GeometryField):
         return True
    return False

def convert_camel_case_to_snake_case(camel_case_string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_case_string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def append_field_type_string(field_name):
    return "    " + field_name + " = models.CharField(max_length=200)\n"

def generate_entry_point_class(entry_point_field_names):
    snake_case_string_arr = list(map(convert_camel_case_to_snake_case, entry_point_field_names))
    fields_string_arr = list(map(append_field_type_string, snake_case_string_arr))
    class_string = "\n\nclass " + ENTRY_POINT_CLASS_NAME + "(BusinessModel):\n"
    for field_str in fields_string_arr:
        class_string = class_string + field_str
    return class_string[:-1]

def is_class_field(line):
    regex_obj = re.search(r'\w+\ *=\ *models.', line)
    return regex_obj is not None

def add_db_column_snippet_to_field_value(line, original_field_name):
    original_field_value = line[line.index(EQUAL_CHARACTER):].strip()

    if not "db_column" in line:
        field_val_comment = ""
        if LINE_COMMENT_INIT_CHAR in original_field_value:
            field_val_comment = original_field_value[original_field_value.index(LINE_COMMENT_INIT_CHAR):]
            original_field_value = original_field_value[:original_field_value.index(LINE_COMMENT_INIT_CHAR)]

        db_column = "db_column=\"" + original_field_name + "\""
        new_field_value = original_field_value.rstrip()[:-1] + ", " + db_column + ")" + field_val_comment
        return new_field_value

    return original_field_value

def change_field_to_ascii(line):
    RENAME_REASON = "# This field was renamed because his name is not in ASCII\n"

    try:
        line.encode('ascii')
        return line
    except UnicodeEncodeError:
        original_field_name = line[:line.index(EQUAL_CHARACTER)].strip()

        new_line = TAB_1X

        for c in original_field_name:
            try:
                c.encode('ascii')
                new_line = new_line + c
            except UnicodeEncodeError:
                new_line = new_line + NON_ASCII_CHAR_REPLACER

    new_line = new_line + " " + add_db_column_snippet_to_field_value(line, original_field_name)
    new_line = new_line if RENAME_REASON in new_line else new_line + RENAME_REASON
    return new_line

def generate_file(package_name, default_name='models.py'):
    classes_from = inspect.getmembers(sys.modules[package_name + '.models'], inspect.isclass)
    geo_classe_names = [ele[0] for ele in classes_from if is_spatial( ele[1])]
    old_model = default_name
    new_model = default_name+'.new'
    entry_point_field_names = []
    has_to_generate_entry_point_model = True

    with open(old_model, 'r') as sr:
        with open(new_model, 'w+') as nm:
            nm.write('from __future__ import unicode_literals\n')
            nm.write('from hyper_resource.models import FeatureModel, BusinessModel\n')
            for line in sr.readlines():
                if line == 'from __future__ import unicode_literals\n':
                    continue
                regex_obj = re.search(r'class\s*(?P<class_model>.*)\(', line)
                class_name_in_line = regex_obj if regex_obj is None else regex_obj.group(1)

                if class_name_in_line in geo_classe_names:
                   line = line.replace('models.Model', 'FeatureModel')
                elif class_name_in_line is not None:
                    line = line.replace('models.Model', 'BusinessModel')
                elif 'models.IntegerField(primary_key=True)' in line:
                    line = line.replace('models.IntegerField(primary_key=True)', 'models.AutoField(primary_key=True)')

                # this prevents app_label to be generated more than once
                if "app_label = '" in line:
                    line = "\n"

                if is_class_field(line):
                    line = change_field_to_ascii(line)

                if "max_length=-1" in line:
                    line = line.replace("max_length=-1", "max_length=255")

                if "class Meta:" in line:
                    line = line + (8 * " ") + "app_label = '" + package_name + "'\n"

                if class_name_in_line == ENTRY_POINT_CLASS_NAME:
                    has_to_generate_entry_point_model = False
                else:
                    if class_name_in_line is not None and class_name_in_line.find(" ") < 0:
                        entry_point_field_names.append(class_name_in_line)

                nm.write(line)

            if has_to_generate_entry_point_model:
                entry_point_class_str = generate_entry_point_class(entry_point_field_names)
                nm.write(entry_point_class_str)
            nm.close()
        sr.close()
    os.remove(old_model)
    os.rename(new_model, old_model)

if __name__ == "__main__":
    if (len( sys.argv))!= 3:
        print('Usage: python modeler_generator.py django_project_name django_app_name')
        exit()

    prj_name = sys.argv[1]
    app_name = sys.argv[2]
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", prj_name + ".settings")
    django.setup()
    generate_file(app_name)
    print('models.py  has been generated')