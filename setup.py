from setuptools import setup, find_packages

__version__ = "0.1.2"
install_requires = ['multipledispatch']
tests_require = ['pytest', 'pytest-cov']
setup_requires = ['pytest-runner', 'multipledispatch']

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="py_hcl",
    version=__version__,
    author="scutdig",
    author_email="zhongzc_arch@outlook.com",
    description=("A Hardware Construct Language"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/scutdig/pyhcl",
    install_requires=install_requires,
    tests_require=tests_require,
    setup_requires=setup_requires,
    packages=find_packages(),
    python_requires='>=3.6',
)
