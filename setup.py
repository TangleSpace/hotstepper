from os import path

import setuptools

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='hotstepper',
    version='1.0.10',
    description='Numpy based step function library.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tanglespace/hotstepper',
    author='Jackson Storm',
    author_email='c6lculus8ntr0py@gmail.com',
    license='MIT',
    project_urls={
        'Documentation': 'https://hotstepper.readthedocs.io/',
        'Source': 'https://github.com/tanglespace/hotstepper',
        'Tracker': 'https://github.com/tanglespace/hotstepper/issues',
    },
    packages=setuptools.find_packages(),
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        'numpy',
        'matplotlib',
        'numpy-indexed==0.3.5',
        'pandas',
        'pytz>=2020.1',
        'seaborn',
        'scipy',
        'statsmodels',
        'numba>=0.51.2',
    ],
    python_requires='>=3.6',
    keywords=[
        'HotStepper',
        'Step Functions',
        'Linear Algebra',
        'Event Data',
        'Data Analysis',
        'Analysis',
        'Data Modelling',
        'Time Series',
        'Kernel Methods',
    ],
)
