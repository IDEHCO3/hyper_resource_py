from setuptools import setup

setup(
    name='hyper_resource_py',
    version='1.0.0',
    packages=['hyper_resource', 'image_generator', 'user_management',
              'hyper_resource_py', 'expression_interface', 'generate_files',
              'hyper_resource.resources'],
    package_dir={'hyper_resource.resources': 'hyper_resource/resources'},
    url='https://github.com/IDEHCO3/hyper_resource_py',
    license='GNU GENERAL PUBLIC LICENSE',
    author='Rogerio Borba',
    author_email='rogerio.borba17@gmail.com',
    description='Tool to work with apis of level three.',
    scripts=['generate_files/generatemodels.py', 'generate_files/generatefiles.py']
)
