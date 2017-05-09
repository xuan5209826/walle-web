"""
walle-web
=======

walle-web web deployment.


And Easy to Setup
-----------------

.. code:: bash
    $ pip install -e .


    $ python run.py
     * Running on http://localhost:5000/


Resources
---------

* `website <https://walle-web.io>`_
* `source <https://github.com/meolu/walle-web>`_
* `issues <https://github.com/meolu/walle-web/issues>`_
"""
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name='walle-web',
    version='2.0.dev0',
    url='http://github.com/meolu/walle-web/',
    license='BSD',
    author='Peter Justin',
    author_email='wushuiyong@walle-web.io',
    description='walle-web.io',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=REQUIREMENTS,
    test_suite='',
    tests_require=[
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers, Users',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
