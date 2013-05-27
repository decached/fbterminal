from setuptools import setup
import os
setup(
    name='fbterminal',
    version='0.2',
    description='Access Facebook on Terminal',
    packages=['fbterminal'],
    license='MIT',
    author='Akash Kothawale',
    author_email='io@decached.com',
    url='http://decached.com/fbterminal',
    install_requires='requests>=1.2.3',
    entry_points={'console_scripts': ['fbterminal = fbterminal.terminal:command_line_runner']},
    data_files=[('/home/' + os.getlogin() + '/', ['fbterminal/.fbterminal'])]
)

os.system('chown ' + os.getlogin() + ' ~/.fbterminal')
