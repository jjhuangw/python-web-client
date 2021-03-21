# -*- coding: utf-8 -*-
"""
    GDSD Feature Store SDK 
"""
from setuptools import setup, find_packages

def fix_setuptools():
    """Work around bugs in setuptools.                                                                                                                                                        

    Some versions of setuptools are broken and raise SandboxViolation for normal                                                                                                              
    operations in a virtualenv. We therefore disable the sandbox to avoid these                                                                                                               
    issues.                                                                                                                                                                                   
    """
    try:
        from setuptools.sandbox import DirectorySandbox
        def violation(operation, *args, **_):
            print("SandboxViolation: %s" % (args,))

        DirectorySandbox._violation = violation
    except ImportError:
        pass

# Fix bugs in setuptools.                                                                                                                                                                     
fix_setuptools()

classifiers = [
    'Development Status :: Alpha',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: BSD License',
    'Operating System :: MacOS',
    'Operating System :: POSIX',
    'Operating System :: Unix',
    'Operating System :: Microsoft',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.6',
    'Topic :: Internet :: Proxy Servers',
    'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
]

setup(
    name                = 'web-client',
    version             = '0.0.1',
    description         = 'restful service client',
    long_description    = open('README.md').read().strip(),
    author              = 'chien chang huang',
    author_email        = '',
    url                 = '',
    license             = 'BSD',
    packages            = find_packages(),
    install_requires    = ['setuptools',
                           'configparser',
                           'requests',
                           'selenium'],
    classifiers         = classifiers
)
