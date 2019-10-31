from setuptools import setup , config,find_packages

setup(
    name='Filepath',
    version='1.0',
    find_packages=['random, os, shutil, re, datetime'],
    packages=['random, os, shutil, re, datetime'],
    package_dir={'': 'MagicPath'},
    url='https://github.com/omeh2003/Filepath',
    license='',
    author='omeh2',
    author_email='omeh2003@gmail.com',
    description='Объектная работа с файловой системой'
    # entry_points={
    #     'console_scripts': [
    #         'magicf = cmd.cmd:entry_point'
    #     ]
    # }

)
