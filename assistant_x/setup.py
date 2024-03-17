from setuptools import setup, find_namespace_packages

setup(
    name='assistant_x',
    version='1',
    description='Address book assistant X.',
    url='https://github.com/nikolay-rudenko/area_51_assistant_x',
    author='Area 51 Team',
    author_email='',
    license='MIT',
    packages=find_namespace_packages(),
    install_requires=['colorama'],
    entry_points={
        'console_scripts': [
            'assistant_x = assistant_x.main:main'
        ]
    }
)