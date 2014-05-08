from distutils.core import setup

setup(
        name='smalltools',
        version='0.0.2-dev',
        packages=['smalltools',
            'smalltools.utils',
            'smalltools.core',
            'smalltools.detect',
            'smalltools.io',],
        license='',
        long_description=open('README.md').read(),
)
