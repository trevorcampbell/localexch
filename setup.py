from setuptools import setup, find_packages

setup(
    name = 'localexch',
    version='0.1',
    description="Estimation and testing for locally exchangeable data",
    author='Trevor Campbell',
    author_email='trevor@stat.ubc.ca',
    url='https://github.com/trevorcampbell/localexch/',
    packages=find_packages(),
    install_requires=['numpy', 'scipy'],
    keywords = ['exchangeability', 'testing', 'estimation', 'local'],
    platforms='ALL'
)
