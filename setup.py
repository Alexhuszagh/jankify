from setuptools import setup

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'License :: Public Domain',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Intended Audience :: Science/Research',
    'Natural Language :: English',
    'Operating System :: Unix',
    'Operating System :: POSIX :: Linux',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Internet :: WWW/HTTP',
]

setup(
    name='jankify',
    version='0.37',
    description=DESCRIPTION,
    classifiers=CLASSIFIERS,
    author='Alex Huszagh',
    py_modules=['jankify'],
    url='https://github.com/Alexhuszagh/jankify',
    license='Public Domain',
    zip_safe=False,
    install_requires=[
        'bs4',
        'markovify',
        'requests',
        'six',
        'tweepy',
    ],
)
