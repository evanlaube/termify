from setuptools import setup, find_packages

def getVersion():
    version_file = 'termify/__version__.py'
    with open(version_file) as f:
        globals_dict = {}
        exec(f.read(), globals_dict)
        return globals_dict['__version__']

setup(
        name='termify-py',
        version=getVersion(),
        description='A terminal-based Spotify controller',
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        url='https://github.com/evanlaube/termify',
        author='Evan Laube',
        author_email='laubeevan@gmail.com',
        license='GPL-3.0',
        packages=find_packages(),
        install_requires=[
            'requests',
            'procyon-py',
            'python-dotenv'
            ],
        extras_require={
            'windows': ['windows-curses']
        },
        entry_points={
            'console_scripts': [
                'termify=termify.__main__:main',
                ],
            },


        )
