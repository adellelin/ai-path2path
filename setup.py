from setuptools import setup, find_packages
from path2path.package import version

setup(
    name='path2path',
    packages=find_packages(),
    version=version,
    install_requires=[
        'flask', 'flask-restful', 'tensorflow>=1.6', 'matplotlib', 'rdp', 'numpy', 'scipy', 'requests'],

    # data_files=data_files,

    entry_points={
        'console_scripts': [
            'crserver=path2path.crserver:main'
        ]
    },
)
