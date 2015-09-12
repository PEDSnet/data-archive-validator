import sys
from setuptools import setup, find_packages
from davd import __version__

if sys.version_info < (2, 7) or sys.version_info > (3, 0):
    raise EnvironmentError('Python 2.7.x is required')

with open('README.md', 'r') as f:
    long_description = f.read()

install_requires = []
with open('requirements.txt', 'r') as f:
    for line in f:
        install_requires.append(line.rstrip())

kwargs = {
    'name': 'davd',
    'version': __version__,
    'author': 'The Children\'s Hospital of Philadelphia',
    'author_email': 'cbmisupport@email.chop.edu',
    'url': 'https://github.com/chop-dbhi/data-models-sqlalchemy',
    'description': 'PEDSnet Data Archive Metadata Validator ',
    'long_description': long_description,
    'license': 'Other/Proprietary',
    'packages': find_packages(),
    'install_requires': install_requires,
    'download_url': '',
    'keywords': ['PEDSnet', 'Metadata', 'Archive', 'Validate'],
    'entry_points': {
        'console_scripts': [
            'davd = davd.main:main'
        ]
    }
}

setup(**kwargs)
