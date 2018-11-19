from setuptools import setup,find_packages

import pathlib
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.txt").read_text()

setup(name='Aggregator',
     version='4.0',
     author='navaneetha kannan',
     author_email='Naveneethan55@gmail.com',
     url='http://github/enakann/Aggregator',
     classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
       ],
     include_package_data=True,
     install_requires=[ "yaml"],
     packages=find_packages(),
     #packages=['Aggregator', 'Aggregator.utils','Aggregator.tests'],

      scripts=['./run.sh'],
     entry_points={
        "console_scripts": [
            "aggregator=Aggregator.__main__:main",
        ]
    },

)
