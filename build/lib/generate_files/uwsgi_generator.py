import os, sys, django

def generate_file(prj_name):
    with open("uwsgi.ini", "w") as uwsgi_file:
        uwsgi_file.write("[uwsgi]\n")
        uwsgi_file.write("http-socket =:2000\n")
        uwsgi_file.write("chdir = /code\n")
        uwsgi_file.write("module = " + prj_name + ".wsgi\n")
        uwsgi_file.write("master = 1\n")
        uwsgi_file.write("processes = 2\n")
        uwsgi_file.write("threads = 2\n")
    uwsgi_file.close()

if __name__ == "__main__":
    if (len( sys.argv))!= 2:
        print('Usage: python uwsgi_generator.py django_project_name')
        exit()

    prj_name = sys.argv[1]
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", prj_name + ".settings")
    django.setup()
    generate_file(prj_name)
    print('models.py  has been generated')