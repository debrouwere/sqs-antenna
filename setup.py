import os
import inspect
from setuptools import setup, find_packages
import antenna

setup(
    name='sqs-antenna',
    version="0.1.1",
    description="Command-line tool that executes a command for each SQS message it receives.",
    long_description=open('README.rst').read(),
    author='Stijn Debrouwere',
    author_email='stijn@stdout.be',
    url='http://github.com/newslynx/sqs-antenna/tree/master',
    packages=find_packages(),
    zip_safe=False,
    license='ISC', 
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ], 
    entry_points = {
          'console_scripts': [
                'antenna = antenna:main', 
          ],
    },
)

