
import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

# maintained automatically in pipeline release to master branch by python-semantic-release
__version__ = '1.2.3'

setuptools.setup(
    name='arcimoto',
    version=__version__,
    author='Cord Slatton',
    author_email='cords@arcimoto.com',
    description='The package and dependencies to build the Arcimoto Global Dependencies Lambda Layer that is attached to each lambda during deployment',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/arcimotocode1/arcimoto-lambda-global-dependencies',
    license='private',
    packages=[
        'arcimoto',
        'arcimoto_aws_services',
        'arcimoto_aws_services.arcimoto_aws_services'
    ],
    install_requires=['cerberus', 'psycopg2'],
)
