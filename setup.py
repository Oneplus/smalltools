from distutils.core import setup

setup(
        name='corpusproc',
        version='0.1-dev',
        packages=['corpusproc',
            'corpusproc.utils',
            'corpusproc.core',
            'corpusproc.conv',
            'corpusproc.detect',
            'corpusproc.io',],
        license='',
        long_description=open('README.md').read(),
)
