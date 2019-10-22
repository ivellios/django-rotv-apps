import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-rotv-apps',
    version='2.5.0',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',  # example license
    description='Applications for a web tv service use in Polish language (i18n in future).',
    long_description=README,
    url='http://raportobiezyswiata.tv/',
    author='Janusz Kamienski',
    author_email='ivellios@raportobiezyswiata.tv',
    test_suite='runtests.runtests',
    install_requires=[
        'Pillow==6.2.0',
        'Django==1.11.23',
        'django-tagging==0.4.5',
        'django-filebrowser>=3.9.1',
        'django-grappelli>=2.10.1',
        'django-adminactions',
        'django-tinymce4-lite',
        'yturl==2.0.2',
        'factory_boy',
        'tox',
        'mock',
    ],
    depency_links = [
        'git+https://git@github.com/ivellios/django-tinymce4-lite.git#egg=django-tinymce4-lite',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
