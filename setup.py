import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

exec(open('ptt/version.py').read())

setuptools.setup(
    name='ssis-ptt',
    version=__version__,
    author='Evo Pricing Limited',
    author_email='info@evopricing.com',
    long_description_content_type='text/markdown',
    description='SSIS Packages Testing Tool',
    long_description=long_description,
    license="MIT",
    url='https://gitlab.evouser.com/etl/data-quality-assurance-tool',
    project_urls={
            'Bug Tracker': 'https://gitlab.evouser.com/etl/ssis-packages-test-tool/-/issues',
            'Website': 'https://gitlab.evouser.com/etl/ssis-packages-test-tool'
    },
    packages=setuptools.find_packages(),
    keywords='ssis-ptt',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
    install_requires=[
        'fire',
        'pyyaml',
        'aioodbc',
        'python-dotenv',
        'numpy',
        'pandas',
        'pyodbc',
        'Jinja2'
    ],
    scripts=['bin/ptt']
)
