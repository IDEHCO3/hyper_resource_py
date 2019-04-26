from django.test import SimpleTestCase
from django.test.runner import DiscoverRunner
import json
import requests
import datetime
import os

class NoDbTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass

# python manage.py test bcim.tests.EntryPointLinksTest --testrunner=bcim.tests.NoDbTestRunner
class EntryPointLinksTest(SimpleTestCase):
    '''This class tests the application entry point and generates a log file containning the number of elements for each link of the entry point'''
    def setUp(self):
        super(EntryPointLinksTest, self).setUp()
        self.entry_point_url =  'http://gabriel:8000/api/bcim/'
        self.app_name = 'bcim'
        self.max_elements_per_link = 5000
        self.count_resource_operation_name = 'count-resource'
        self.all_entrypoint_liks = {
            'too_many_elements_links': [],
            'less_elements_links': [],
            'non_200_status_code_links': []
        }

    def aux_get_dict_from_response(self, response):
        return dict( json.loads(response.text) )

    def aux_get_entrypoint_links(self, response):
        response_dict = self.aux_get_dict_from_response(response)
        return response_dict.values()

    def aux_load_entrypoint_links_dict(self, entrypoint_response):
        entryPoint_liks = self.aux_get_entrypoint_links(entrypoint_response)

        for link in entryPoint_liks:
            count_resource_link = link
            if count_resource_link[-1] != '/':
                count_resource_link = count_resource_link + '/'

                count_resource_link = count_resource_link + self.count_resource_operation_name

            response_for_link = requests.get(count_resource_link)
            if response_for_link.status_code != 200:
                continue
            number_of_elements = self.aux_get_dict_from_response(response_for_link)[self.count_resource_operation_name]
            if number_of_elements > self.max_elements_per_link:
                self.all_entrypoint_liks['too_many_elements_links'].append( (link, number_of_elements) )

            if number_of_elements <= self.max_elements_per_link:
                self.all_entrypoint_liks['less_elements_links'].append( (link, number_of_elements) )

    def aux_print_entrypoint_links_overview(self):
        print('\n\n---------Links with too many elements---------')
        for link, number_of_elements in self.all_entrypoint_liks['too_many_elements_links']:
            print(link + '\nhas ' + str(number_of_elements) + ' elements')
        print('\nNUMBER OF LINKS: ' + str(len(self.all_entrypoint_liks['too_many_elements_links'])))
        print('----------------------------------------------')
        print('-----------Links with fell elements-----------')
        for link, number_of_elements in self.all_entrypoint_liks['less_elements_links']:
            print(link + '\nhas ' + str(number_of_elements) + ' elements')
        print('\nNUMBER OF LINKS: ' + str(len(self.all_entrypoint_liks['less_elements_links'])))
        print('----------------------------------------------')

    def aux_generate_test_log_file(self):
        now = datetime.datetime.now()
        test_log_file_name = str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '_' + str(now.hour) + '-' + str(now.minute) + '-' + str(now.second)

        with open(self.app_name + '/test_logs/' + test_log_file_name + '.tlog', 'w+') as test_log_file:
            test_log_file.write('Test log for: ' + self.entry_point_url + '\n\n')
            test_log_file.write('---------Links with too many elements---------\n')
            test_log_file.write('<hyper:many>\n')

            for link, number_of_elements in self.all_entrypoint_liks['too_many_elements_links']:
                test_log_file.write(link + ' <|> has ' + str(number_of_elements) + ' elements\n')
            test_log_file.write('\nNUMBER OF LINKS: ' + str(len(self.all_entrypoint_liks['too_many_elements_links'])) + '\n')
            test_log_file.write('</hyper:many>\n\n')

            test_log_file.write('-----------Links with fell elements-----------\n')
            test_log_file.write('<hyper:less>\n')

            for link, number_of_elements in self.all_entrypoint_liks['less_elements_links']:
                test_log_file.write(link + ' <|> has ' + str(number_of_elements) + ' elements\n')

            test_log_file.write('\nNUMBER OF LINKS: ' + str(len(self.all_entrypoint_liks['less_elements_links'])) + '\n')
            test_log_file.write('</hyper:less>\n')

    def test_bcim(self):
        response = requests.get(self.entry_point_url)
        self.assertEquals(response.status_code, 200)
        self.aux_load_entrypoint_links_dict(response)
        self.aux_print_entrypoint_links_overview()
        self.aux_generate_test_log_file()
        print('Test log file created in: bcim/test_logs/ check this file for more test details')

