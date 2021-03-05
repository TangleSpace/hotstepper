import setuptools
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='hotstepper',
    version='1.0.3',    
    description='Numpy based step function library.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tanglespace/hotstepper',
    author='Jackson Storm',
    author_email='c6lculus8ntr0py@gmail.com',
    license='MIT',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
            'numpy>=1.19.5',
            'matplotlib>=3.3.3',
			'numpy-indexed==0.3.5',
			'pandas>=1.2.0',
			'pytz>=2020.1',  
            'seaborn>=0.11.1',
            'scipy>=1.5.4',
            'statsmodels>=0.12.0',
            'numba>=0.51.2',
                      ],

)