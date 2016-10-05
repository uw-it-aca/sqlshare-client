import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='sqlshare_client',
    version='0.1',
    packages=['sqlshare_client'],
    include_package_data=True,
    install_requires = [
        'setuptools',
        'sanction',
        'tabulate',
    ],
    license='Apache License, Version 2.0',  # example license
    scripts = [ 'sqlshare_client/scripts/sqlshare_show_dataset',
                'sqlshare_client/scripts/sqlshare_all_datasets',
                'sqlshare_client/scripts/sqlshare_my_datasets',
                'sqlshare_client/scripts/sqlshare_shared_datasets',
                'sqlshare_client/scripts/sqlshare_whoami',
                'sqlshare_client/scripts/sqlshare_run_query',
                'sqlshare_client/scripts/sqlshare_list_queries',
                'sqlshare_client/scripts/sqlshare_permissions',
                'sqlshare_client/scripts/sqlshare_create_from_sql'],
    description='A library for accessing SQLShare REST Services',
    long_description=README,
    url='http://docs.sqlshare.apiary.io/',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
)
