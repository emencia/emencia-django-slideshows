from setuptools import setup, find_packages

setup(
    name='emencia-django-slideshows',
    version=__import__('slideshows').__version__,
    description=__import__('slideshows').__doc__,
    long_description=open('README.rst').read(),
    author='David Thenon',
    author_email='dthenon@emencia.com',
    url='http://pypi.python.org/pypi/emencia-django-slideshows',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'Django>=1.6',
        'django-filebrowser-no-grappelli>=3.5.6',
        'djangocms_text_ckeditor',
    ],
    include_package_data=True,
    zip_safe=False
)