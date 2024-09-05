from setuptools import setup, find_packages

setup(
        name='termify',
        version='1.0.0',
        description='A terminal-based Spotify controller',
        author='Evan Laube',
        author_email='laubeevan@gmail.com',
        packages=find_packages(),
        install_requires=[
            'requests',
            'python-dotenv'
            ],
        entry_points={
            'console_scripts': [
                'termify=termify.termify:main',
                ],
            },


        )
