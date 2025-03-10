from setuptools import setup, find_packages

setup(
    name='QDF',          # Replace with your package name
    version='0.0.1',
    author='Dai-Jia, Wu',
    author_email='porkface0301@gmail.com',
    description='Quantum Data Formalizer',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/RatisWu/QDF',
    packages=find_packages(),          # Automatically find package directories
    install_requires=[                 # Optional, if you have dependencies
        'netCDF4'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)