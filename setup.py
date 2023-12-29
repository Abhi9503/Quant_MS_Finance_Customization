from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in quantbit_finance_customization/__init__.py
from quantbit_finance_customization import __version__ as version

setup(
	name="quantbit_finance_customization",
	version=version,
	description="This application used to add customization in erpnext",
	author="Quanbit Tech",
	author_email="abhishek.shinde@erpdata.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
