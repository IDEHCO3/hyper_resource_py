'''
Generate a test class in <app_name>/tests.py to test the application entry point
'''

import sys, os

# METHODS TO GANARATE THE ENTRY POINT TEST FILE
def imports_str_as_array():
    arr = []
    arr.append("from django.test import SimpleTestCase\n")
    arr.append("from django.test.runner import DiscoverRunner\n")
    arr.append("import json\n")
    arr.append("import requests\n")
    arr.append("import datetime\n")
    arr.append("import os\n\n")
    return arr

def no_db_test_runner_class_str_as_array():
    arr = []
    arr.append("class NoDbTestRunner(DiscoverRunner):\n")
    arr.append((4 * " ") + "def setup_databases(self, **kwargs):\n")
    arr.append((8 * " ") + "pass\n\n")
    arr.append((4 * " ") + "def teardown_databases(self, old_config, **kwargs):\n")
    arr.append((8 * " ") + "pass\n\n")
    return arr

def class_assignature_str_as_array(app_name):
    arr = []
    arr.append("# python manage.py test " + app_name + ".tests.EntryPointLinksTest --testrunner=" + app_name + ".tests.NoDbTestRunner\n")
    arr.append("class EntryPointLinksTest(SimpleTestCase):\n")
    arr.append((4 * " ") + "'''This class tests the application entry point and generates a log file containning the number of elements for each link of the entry point'''\n")
    return arr

def setup_method_str_as_array(app_name, entry_point_url):
    arr = []
    arr.append((4 * " ") + "def setUp(self):\n")
    arr.append((8 * " ") + "super(EntryPointLinksTest, self).setUp()\n")
        #self.entry_point_url =  "http://" + HOST + "api/ibge/cartografia/bases-cartograficas/1000k/2014/" # <ENTRYPOINT_TEST_URL>
    arr.append((8 * " ") + "self.entry_point_url =  '" + entry_point_url + "'\n")
        #self.app_name = "cartografia_bases_cartograficas_1000k_2014" # <APP_NAME>
    arr.append((8 * " ") + "self.app_name = '" + app_name + "'\n")
    arr.append((8 * " ") + "self.max_elements_per_link = 500\n")
    arr.append((8 * " ") + "self.count_resource_operation_name = 'count-resource'\n")
    arr.append((8 * " ") + "self.all_entrypoint_liks = {\n")
    arr.append((12 * " ") + "'too_many_elements_links': [],\n")
    arr.append((12 * " ") + "'less_elements_links': [],\n")
    arr.append((12 * " ") + "'non_200_status_code_links': []\n")
    arr.append((8 * " ") + "}\n\n")
    return arr

def get_dict_from_response_method_str_as_array():
    arr = []
    arr.append((4 * " ") + "def aux_get_dict_from_response(self, response):\n")
    arr.append((8 * " ") + "return dict( json.loads(response.text) )\n\n")
    return arr

def get_entrypoint_links_method_str_as_array():
    arr = []
    arr.append((4 * " ") + "def aux_get_entrypoint_links(self, response):\n")
    arr.append((8 * " ") + "response_dict = self.aux_get_dict_from_response(response)\n")
    arr.append((8 * " ") + "return response_dict.values()\n\n")
    return arr

def load_entry_point_links_dict_method_str_as_array():
    arr = []
    arr.append((4 * " ") + "def aux_load_entrypoint_links_dict(self, entrypoint_response):\n")
    arr.append((8 * " ") + "entryPoint_liks = self.aux_get_entrypoint_links(entrypoint_response)\n\n")

    arr.append((8 * " ") + "for link in entryPoint_liks:\n")
    arr.append((12 * " ") + "count_resource_link = link\n")
    arr.append((12 * " ") + "if count_resource_link[-1] != '/':\n")
    arr.append((16 * " ") + "count_resource_link = count_resource_link + '/'\n\n")

    arr.append((16 * " ") + "count_resource_link = count_resource_link + self.count_resource_operation_name\n\n")

    arr.append((12 * " ") + "response_for_link = requests.get(count_resource_link)\n")
    arr.append((12 * " ") + "if response_for_link.status_code != 200:\n")
    arr.append((16 * " ") + "continue\n")

    arr.append((12 * " ") + "number_of_elements = self.aux_get_dict_from_response(response_for_link)[self.count_resource_operation_name]\n")
    arr.append((12 * " ") + "if number_of_elements > self.max_elements_per_link:\n")
    arr.append((16 * " ") + "self.all_entrypoint_liks['too_many_elements_links'].append( (link, number_of_elements) )\n\n")

    arr.append((12 * " ") + "if number_of_elements <= self.max_elements_per_link:\n")
    arr.append((16 * " ") + "self.all_entrypoint_liks['less_elements_links'].append( (link, number_of_elements) )\n\n")
    return arr

def print_entrypoint_links_overview_str_as_array():
    arr = []
    arr.append((4 * " ") + "def aux_print_entrypoint_links_overview(self):\n")
    arr.append((8 * " ") + "print('\\n\\n---------Links with too many elements---------')\n")
    arr.append((8 * " ") + "for link, number_of_elements in self.all_entrypoint_liks['too_many_elements_links']:\n")
    arr.append((12 * " ") + "print(link + '\\nhas ' + str(number_of_elements) + ' elements')\n")
    arr.append((8 * " ") + "print('\\nNUMBER OF LINKS: ' + str(len(self.all_entrypoint_liks['too_many_elements_links'])))\n")
    arr.append((8 * " ") + "print('----------------------------------------------')\n")

    arr.append((8 * " ") + "print('-----------Links with fell elements-----------')\n")
    arr.append((8 * " ") + "for link, number_of_elements in self.all_entrypoint_liks['less_elements_links']:\n")
    arr.append((12 * " ") + "print(link + '\\nhas ' + str(number_of_elements) + ' elements')\n")
    arr.append((8 * " ") + "print('\\nNUMBER OF LINKS: ' + str(len(self.all_entrypoint_liks['less_elements_links'])))\n")
    arr.append((8 * " ") + "print('----------------------------------------------')\n\n")
    return arr

def generate_test_log_file_str_as_array():
    arr = []
    arr.append((4 * " ") + "def aux_generate_test_log_file(self):\n")
    arr.append((8 * " ") + "now = datetime.datetime.now()\n")
    arr.append((8 * " ") + "test_log_file_name = str(now.year) + str(now.month) + str(now.day) + '_' + str(now.hour) + str(now.minute) + str(now.second)\n\n")

    #arr.append((8 * " ") + "os.mkdir(self.app_name + '/test_logs/')\n")
    arr.append((8 * " ") + "with open(self.app_name + '/test_logs/' + test_log_file_name + '.tlog', 'w+') as test_log_file:\n")
    arr.append((12 * " ") + "test_log_file.write('Test log for: ' + self.entry_point_url + '\\n\\n')\n")

    arr.append((12 * " ") + "test_log_file.write('---------Links with too many elements---------\\n')\n")
    arr.append((12 * " ") + "test_log_file.write('<hyper:many>\\n')\n\n")

    arr.append((12 * " ") + "for link, number_of_elements in self.all_entrypoint_liks['too_many_elements_links']:\n")
    arr.append((16 * " ") + "test_log_file.write(link + ' <|> has ' + str(number_of_elements) + ' elements\\n')\n")

    arr.append((12 * " ") + "test_log_file.write('\\nNUMBER OF LINKS: ' + str(len(self.all_entrypoint_liks['too_many_elements_links'])) + '\\n')\n")
    arr.append((12 * " ") + "test_log_file.write('</hyper:many>\\n\\n')\n\n")

    arr.append((12 * " ") + "test_log_file.write('-----------Links with fell elements-----------\\n')\n")
    arr.append((12 * " ") + "test_log_file.write('<hyper:less>\\n')\n\n")

    arr.append((12 * " ") + "for link, number_of_elements in self.all_entrypoint_liks['less_elements_links']:\n")
    arr.append((16 * " ") + "test_log_file.write(link + ' <|> has ' + str(number_of_elements) + ' elements\\n')\n\n")

    arr.append((12 * " ") + "test_log_file.write('\\nNUMBER OF LINKS: ' + str(len(self.all_entrypoint_liks['less_elements_links'])) + '\\n')\n")
    arr.append((12 * " ") + "test_log_file.write('</hyper:less>\\n')\n\n")
    return arr

def main_test_method_str_as_array(app_name):
    arr = []
    arr.append((4 * " ") + "def test_" + app_name + "(self):\n")
    arr.append((8 * " ") + "response = requests.get(self.entry_point_url)\n")
    arr.append((8 * " ") + "self.assertEquals(response.status_code, 200)\n")
    arr.append((8 * " ") + "self.aux_load_entrypoint_links_dict(response)\n")
    arr.append((8 * " ") + "self.aux_print_entrypoint_links_overview()\n")
    arr.append((8 * " ") + "self.aux_generate_test_log_file()\n")
    arr.append((8 * " ") + "print('Test log file created in: " + app_name + "/test_logs/ check this file for more test details')\n\n")
    return arr

def main(argv):

    size_of_arguments = len(argv)
    if size_of_arguments < 3:
        print('Usage: python generator_entry_point.py app_name entry_point_url')
        exit()
    else:
        print('-------------------------------------------------------------------------------------------------------')
        print('Modifying file: ' + argv[1] + '/tests.py')
        print('-------------------------------------------------------------------------------------------------------')

    app_name = argv[1]
    entry_point_url = argv[2]

    # GENERATING TEST FILE
    test_file_data_rows = []
    test_file_data_rows.extend(imports_str_as_array())
    test_file_data_rows.extend(no_db_test_runner_class_str_as_array())
    test_file_data_rows.extend(class_assignature_str_as_array(app_name))
    test_file_data_rows.extend(setup_method_str_as_array(app_name, entry_point_url))
    test_file_data_rows.extend(get_dict_from_response_method_str_as_array())
    test_file_data_rows.extend(get_entrypoint_links_method_str_as_array())
    test_file_data_rows.extend(load_entry_point_links_dict_method_str_as_array())
    test_file_data_rows.extend(print_entrypoint_links_overview_str_as_array())
    test_file_data_rows.extend(generate_test_log_file_str_as_array())
    test_file_data_rows.extend(main_test_method_str_as_array(app_name))

    try:
        os.rename(app_name + "/tests.py", app_name + "/tests_old.py")
    except FileNotFoundError:
        pass

    with open(app_name + "/tests.py", "w+") as test_file:
        for row in test_file_data_rows:
            test_file.write(row)

    # GENERATING FILE TO READ ERROR LOG TEST FILE
    try:
        os.mkdir(app_name + '/test_logs/')
    except FileExistsError:
        pass

    print('All files have been generated')

if __name__ == "__main__":
    main(sys.argv)