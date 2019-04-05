from distutils.core import setup

setup(
    name='hyper_resource_py',
    version='1.0.0',
    packages=['bcim', 'build.lib.bcim', 'build.lib.controle', 'build.lib.controle.migrations', 'build.lib.hyper_test',
              'build.lib.hyper_test.migrations', 'build.lib.raster_base', 'build.lib.raster_base.migrations',
              'build.lib.hyper_resource', 'build.lib.hyper_resource.resources', 'build.lib.controle_adesao',
              'build.lib.controle_adesao.migrations', 'build.lib.image_generator', 'build.lib.user_management',
              'build.lib.hyper_resource_py', 'build.lib.expression_interface',
              'build.lib.expression_interface.migrations', 'controle', 'controle.migrations', 'hyper_test',
              'hyper_test.migrations', 'raster_base', 'raster_base.migrations', 'hyper_resource',
              'hyper_resource.resources', 'controle_adesao', 'controle_adesao.migrations', 'generate_files',
              'image_generator', 'user_management', 'hyper_resource_py', 'expression_interface',
              'expression_interface.migrations'],
    url='https://github.com/IDEHCO3/hyper_resource_py',
    license='GNU GENERAL PUBLIC LICENSE',
    author='Rogerio Borba',
    author_email='rogerio.borba17@gmail.com',
    description='Tool to work with apis of level three.',
    scripts=['generate_files/generator_models_settings_files.py', 'generate_files/generator_files.py']
)
