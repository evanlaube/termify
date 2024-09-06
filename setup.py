from setuptools import setup, find_packages

setup(
        name='termify-py',
        version='1.0.0',
        description='A terminal-based Spotify controller',
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        url='https://github.com/evanlaube/termify',
        author='Evan Laube',
        author_email='laubeevan@gmail.com',
        license='GPT-3.0',
        packages=find_packages(),
        install_requires=[
            'requests',
            'python-dotenv'
            ],
        entry_points={
            'console_scripts': [
                'termify=termify.__main__:main',
                ],
            },


        )
