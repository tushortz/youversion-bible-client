from setuptools import setup

setup(
    name='youversion-bible-client',
    version='0.1.0',
    description='A Command line interface for interacting with the YouVersion BIble API',
    long_description='A Command line interface for interacting with the YouVersion BIble API',
    keywords=[
        "YouVersion Bible",
        "Bible",
        "Youversion",
        "Lifechurch"
    ],
    url='https://github.com/tushortz/youversion-bible-client',
    author='Taiwo Kareem',
    maintainer='Taiwo Kareem',
    maintainer_email='taiwo.kareem36@gmail.com',
    license='MIT',
    packages=[
        'youversion'
    ],
    zip_safe=False,
    requires=[
        "requests"
    ]
)