from distutils.core import setup
#from setuptools import setup

setup(
    name='hyper_resource_py',
    version='1.0.0',
    packages=['hyper_resource', 'image_generator', 'user_management',
              'hyper_resource_py', 'expression_interface', 'generate_files',
              'hyper_resource.resources'],
    package_dir={'hyper_resource.resources': 'hyper_resource/resources'},
#    install_requires=['geobuf', 'bcrypt==3.1.3', 'certifi>=2017.7.27.1', 'cffi>=1.10.0', 'chardet==3.0.4',
#                      'Django>=1.11.1', 'django-cors-headers==2.1.0', 'django-filter==1.0.4',
#                      'django-simple-captcha==0.5.5' ,'djangorestframework>=3.6.3', 'djangorestframework-gis>=0.11.2',
#                      'djangorestframework-jwt==1.10.0', 'html5lib==0.999999999', 'idna==2.5', 'Markdown==2.6.8',
#                      'Pillow==3.1.0', 'pycparser==2.18', 'PyJWT==1.5.0', 'python-mimeparse==1.6.0',
#                      'pytz==2017.2', 'requests==2.18.3', 'six==1.10.0', 'webencodings==0.5.1'],
    url='https://github.com/IDEHCO3/hyper_resource_py',
    license='GNU GENERAL PUBLIC LICENSE',
    author='Rogerio Borba',
    author_email='rogerio.borba17@gmail.com',
    description='Tool to work with apis of level three.',
    scripts=['generate_files/generatemodels.py', 'generate_files/generatefiles.py']
)
