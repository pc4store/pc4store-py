from setuptools import setup, find_packages

install_requires = ['requests>=2.25.1', 'cryptography>=3.4.5', 'aiohttp>=3.6.2']

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='pc4store',
    version='1.0.0',
    description='Python lib for integration with pc4store payment system',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires,
    include_package_data=True,
)
