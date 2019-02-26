import sys

import requests
LESS_ELEMENTS_INIT_TAG = '<hyper:less>'
ALL_ELEMENTS_INIT_TAG = '<hyper:all>'
MANY_ELEMENTS_INIT_TAG = '<hyper:many>'
ELEMENTS_QUANTITY_CHECK_INIT_TAG = LESS_ELEMENTS_INIT_TAG
TOKEN = '<|>'
ELEMENTS_QUANTITY_CHECK_FINAL_TAG = ELEMENTS_QUANTITY_CHECK_INIT_TAG[0] + '/' + ELEMENTS_QUANTITY_CHECK_INIT_TAG[1:]

def get_error_log_from_log_file(app_name, log_file_name):
    error_logs = []

    with open(app_name + "/test_logs/" + log_file_name, 'r') as log_file:
        analize_line = False

        for line in log_file.readlines():
            if line.strip() == ELEMENTS_QUANTITY_CHECK_FINAL_TAG:
                break

            if analize_line:
                url_or_none = get_only_url(line.strip())

                if url_or_none:
                    non_200_response_or_none = get_non_200_response_or_none(url_or_none)
                    if non_200_response_or_none:
                        error_logs.append( non_200_response_or_none )
                else:
                    continue

            if line.strip() == ELEMENTS_QUANTITY_CHECK_INIT_TAG:
                analize_line = True
            else:
                continue
    return error_logs

def get_only_url(line):
    if not line.startswith('http://') and not line.startswith('https://'):
        return None

    token_idx = line.find(TOKEN)
    if token_idx == -1:
        return line
    return line[:token_idx].strip()

def get_non_200_response_or_none(url):
    response = requests.get(url)
    if response.status_code not in [200]:
        #print('INFO: non 200 url response founded (' + url + ')')
        return 'URL ERROR (' + str(response.status_code) + '): ' + url + '\n' + response.text
    return None

def generate_error_log_file(app_name, log_file_name, non_200_urls_response):
    with open(app_name + "/test_logs/" + log_file_name + '.error', 'w+') as error_log_file:
        for line in non_200_urls_response:
            error_log_file.write(line)
        error_log_file.write('\nNumber of non 200 responses: ' + str(len(non_200_urls_response)) + "\n")

        if ELEMENTS_QUANTITY_CHECK_INIT_TAG == LESS_ELEMENTS_INIT_TAG:
            error_log_file.write("WARNING: Not all entry point links were tested. Only links with LESS elements were checked")

def main(argv):

    size_of_arguments = len(argv)
    if size_of_arguments < 3:
        print('Usage: python app_name log_file_name')
        print('"log_file_name" must be a log file with ".tlog" extension that\'s located inside test_logs folder of each application')
        exit()
    else:
        print('-------------------------------------------------------------------------------------------------------')
        print('Generating file: ' + argv[1] + '/test_logs/' + argv[2] + '.error')
        print('-------------------------------------------------------------------------------------------------------')

    app_name = argv[1]
    log_file_name = argv[2]

    error_logs_list = get_error_log_from_log_file(app_name, log_file_name)
    generate_error_log_file(app_name, log_file_name, error_logs_list)

    print('All files have been generated')

if __name__ == "__main__":
    main(sys.argv)

