# hyper_resource_py
Tool to work with apis of level three.

Dependencies
Certify yourself that GDAL is installed and environment variable properly configured. Type gdalinfo --version in your command pronpt, if you seen GDAL version you are ready to proceed

Windows
Microsoft Visual C++ 14.0

#Generate code by Reverse engineering

IMPORTANT:
Before any procedure, certify yourself that your python installations has the requirements specified in requirements.txt.
If the these dependencies ins't installed you can download the hyper_resource_py project and run the follow commands on the terminal, inside the hyper_resource_py folder:
$ pip install -r requirements.txt

And to install Hyper Resource
$ python setup.py install

If the some of the previous commands require privileges try to run the follow command
$ pip install --user

Installing hyper_resource_py

0. Open console

1. Start a Django project

	$ django-admin startproject [project_name]

2. Got to project folder through console

	$ cd path/to/your/project/[project_name]

3. Create a app inside the project folder

	$ django-admin startapp [app_name]
	
4. Type the command below and follow the instructions on console

	$ generatemodels [project_name] [app_name]

6. Generate the necessary files using the command below

	$ python generatefiles [project_name] [app_name]

7. Start your application through console

	python manage.py runserver

8. Access your project using the browser

	http://localhost:8000
