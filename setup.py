from os.path import basename, dirname, join, splitext
from glob import glob

from setuptools import setup, find_namespace_packages

base_dir = dirname(__file__)

__pkginfo__ = {}
with open(join(base_dir, '__pkginfo__.py')) as pkginfo_fp:
    exec(pkginfo_fp.read(), __pkginfo__)  # pylint: disable=exec-used

version = __pkginfo__.get('version')

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    author='Steve Cirelli',
    author_email='steve@cirelli.org',
    url='https://github.com/ccirelli2/property_scraper',

    name='property_scraper',
    version=version,
    description='Zillow scraper',

    package_dir={'': 'src'},
    packages=find_namespace_packages('src', exclude=['*.tests', '*.tests.*', 'tests.*', 'tests', 'scripts']),
    dependency_links=[],
    install_requires=[
        'astroid==2.4.1',
        'beautifulsoup4==4.9.0',
        'certifi==2020.4.5.1',
        'cffi==1.14.0',
        'chardet==3.0.4',
        'cryptography==2.9.2',
        'idna==2.9',
        'importlib-metadata==1.6.0',
        'isort==4.3.21',
        'lazy-object-proxy==1.4.3',
        'lxml==4.5.0',
        'mccabe==0.6.1',
        'mysql-connector==2.2.9',
        'numpy==1.18.4',
        'pandas==1.0.3',
        'pycparser==2.20',
        'Pygments==2.6.1',
        'PyMySQL==0.9.3',
        'python-dateutil==2.8.1',
        'pytz==2020.1',
        'pyzillow==0.5.5',
        'requests==2.23.0',
        'six==1.14.0',
        'soupsieve==2.0.1',
        'toml==0.10.1',
        'typed-ast==1.4.1',
        'urllib3==1.25.9',
        'urwid==2.1.0',
        'wrapt==1.12.1',
        'zipp==3.1.0'
    ],

    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],

    entry_points={
        'console_scripts': [
            'zillow-scraper = main.cli:main'
        ],
        'gui_scripts': []
    },

    package_data={
        'scraper': 'abbr-name.json'
    },
    include_package_data=True,

    keywords='zillow scrapper',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities'
    ],
    python_requires='>=3.7'
)
