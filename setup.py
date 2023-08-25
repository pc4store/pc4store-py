from setuptools import setup, find_packages


install_requires = ["cryptography>=3.4.5", "pydantic>=1.10.0,<2.0.0", "httpx>=0.24.1"]

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="pc4store",
    version="2.0.9",
    description="Python lib for integration with pc4store payment system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(exclude=[".tests", "examples"]),
    install_requires=install_requires,
    include_package_data=True,
)
