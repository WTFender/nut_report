import setuptools

with open('requirements.txt') as f:
	requirements = f.readlines()

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
	name='NutReport',
	version='1.0.0',
	author='WTFender',
	author_email='wtfender.cs@gmail.com',
	description='Demo parser utility for Counter-Strike 2',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/WTFender/nut_report',
	packages=setuptools.find_packages(),
	install_requires=requirements,
	entry_points = {
		'console_scripts': ['nut_report=nut_report.cli:main']
	},
	classifiers=[
		'Programming Language :: Python :: 3',
		'Operating System :: OS Independent'
	]
)