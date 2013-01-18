from setuptools import setup

setup(
    name='fbterminal',
    version='0.1',
    packages=['fbterminal'],
    license='MIT',
    author='Akash Kothawale',
    author_email='io@decached.com',
    url='http://decached.com/fbterminal',
    install_requires='pycurl==7.19.0',
    entry_points={
        'console_scripts': ['fbterminal = fbterminal.terminal:command_line_runner',
        ]
    },
    package_data={'fbterminal': ['.fbterminal']}
)
