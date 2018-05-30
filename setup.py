#!/usr/bin/env python3

from setuptools import setup

setup(
	name = 'yt2gif',
	version = '0.0',
	description = 'Turns a youtube video into a gif',
	author = 'Adam Nunez',
	author_email = 'adam.a.nunez@gmail.com',
	license = 'GPLv3',
	url = 'https://github.com/aanunez/yt2gif',
	packages = ['yt2gif'],
    entry_points={
        'console_scripts': [
            'yt2gif = yt2gif.__main__:main'
        ]
    },
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='youtube gif'
)
