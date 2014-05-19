
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Sensor project for the summer internship',
    'author': 'Pingpan',
    'download_url': 'pingpan2013@github.com',
    'author_email': 'pingpan@umich.edu',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['sensor_project'],
    'scripts': [],
    'name': 'Sensor_Project'
}

setup(**config)
