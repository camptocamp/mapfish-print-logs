import os
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))
INSTALL_REQUIRES = open(os.path.join(HERE, 'requirements.txt')).read().splitlines()

setup(
    name='mapfish_print_logs',
    version='0.0',
    description='Micro service to expose logs from mapfish_print',
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='',
    author_email='info@camptocamp.com',
    url='',
    keywords='web pyramid mapfish',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=INSTALL_REQUIRES,
    tests_require=INSTALL_REQUIRES,
    test_suite="mapfish_print_logs",
    entry_points="""\
    [paste.app_factory]
    main = mapfish_print_logs:main
    """
)
