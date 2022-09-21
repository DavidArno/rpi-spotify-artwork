from distutils.core import setup
import os.path
import codecs

# "borrowed" this code from https://packaging.python.org/en/latest/guides/single-sourcing-package-version/
def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError('Unable to find version string.')

setup(
    name = 'rpi_spotify_artwork',
    version = get_version('src/rpi_spotify_shared/version.py'),
    author = 'David Arno', 
    author_email = 'david@davidarno.org',
    packages = [
        'rpi_spotify_shared/message_handler', 
        'hub75_display',
        'i75_display_driver',
        'i75_display_driver/shared',
        'i75_display_driver/spotify_view',
        'i75_display_driver/test_views',
        'i75_display_driver/weather_forecast_view',
        'third_party'
    ],
    package_data = {
        'hub75_display': [ 'py.typed' ]
    }, 
    package_dir = {
        '': 'src'
    },
    long_description=open('README.md').read()
)