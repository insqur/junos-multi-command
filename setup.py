from distutils.core import setup

setup(
    name='junos-multi-command',
    version='0.3',
    author='Lance Le Roux',
    author_email='wirescrossed@gmail.com',
    packages=['junos-multi-command'],
    scripts=['junos-multi-command/junos-multi-command.py'],
    url='http://pypi.python.org/pypi/junos-multi-command/',
    license='LICENSE.txt',
    description='Run commands against multiple Juniper Junos OS devices',
    long_description=open('README.txt').read(),
    install_requires=[
        "PyYaml >= 3.10",
        "ncclient >= 0.1a",
    ],
)
