from setuptools import setup
import os
import subprocess
setup(
    name='fbterminal',
    version='0.1.1',
    packages=['fbterminal'],
    license='MIT',
    author='Akash Kothawale',
    author_email='io@decached.com',
    url='http://decached.com/fbterminal',
    install_requires='pycurl==7.19.0',
    entry_points={'console_scripts': ['fbterminal = fbterminal.terminal:command_line_runner']},
    data_files=[('/home/' + os.getlogin() + '/', ['fbterminal/.fbterminal'])]
)

os.system('chown ' + os.getlogin() + ' ~/.fbterminal')
