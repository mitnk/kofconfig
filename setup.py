# via: https://github.com/pypa/sampleproject/blob/master/setup.py
from setuptools import setup

DESC = """
Home Page: https://github.com/mitnk/kofconfig

Tested on MAME OS X Version 0.135. Mac OS X 10.11.2

Install
::

    $ pip install kofconfig


Usages
-----------------

After installed, an executable ``kofconfig`` would available for use.
If not, please replace following examples with ``python -m kofconfig``.

::

    kofconfig ABCD[XYZV] ABCD[XYZV]

    A: 轻拳  B: 轻脚  C: 重拳  D: 重脚
    X: A+B  Y: C+D  Z: A+B+C V: A+B+C+D

    XYZV are optional.

    You can also using it this way:
    kofconfig -p1 ABCD[XYZV]
    kofconfig -p2 ABCD[XYZV]
    kofconfig -p1 ABCD[XYZV] -p2 ABCD[XYZV]


Valid Examples:

::

    $ kofconfig -p1 JKUI
    $ kofconfig -p1 JKUIHN
    $ kofconfig -p2 JKLO
    $ kofconfig -p2 JKLOIU
    $ kofconfig -p2 JKLOIUNH
    $ kofconfig JKLOIU JKUI  # assume connected two keyboards
    $ kofconfig -p2 JKUI -p1 JKLOIU  # assume connected two keyboards


You need to restart MAME after config.
"""

setup(
    name='kofconfig',
    version='0.1.0',

    description='KOF Keyboard Config Tool for MAME OS X',
    long_description=DESC,

    url='https://github.com/mitnk/kofconfig',
    author='mitnk',
    author_email='w@mitnk.com',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='KOF MAME keyboard',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    # packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    py_modules=["kofconfig"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    # install_requires=['peppercorn'],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'kofconfig=kofconfig:main',
        ],
    },
)
