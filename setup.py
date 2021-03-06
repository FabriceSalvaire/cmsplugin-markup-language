from setuptools import setup, find_packages
from cmsplugin_markup_language import __version__

REQUIREMENTS = [
    'django-cms>=3.0.12',
    'django-filer>=0.9.9',
    'django>=1.7',
]

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
]

setup(
    name='cmsplugin-markup-language',
    version=__version__,
    description='Markup Language Plugin for Django CMS (ReStructured Text, RST)',
    author='Fabrice Salvaire',
    author_email='fabrice.salvaire@orange.fr',
    url='https://github.com/FabriceSalvaire/cmsplugin-markup-language',
    packages=find_packages(),
    license='LICENSE.txt',
    platforms=['OS Independent'],
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    include_package_data=True,
    zip_safe=False,
    long_description=open('README.rst').read(),
)
