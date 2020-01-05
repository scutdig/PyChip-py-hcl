from setuptools import setup, find_packages

__version__ = "0.1.0"
install_requires = []
tests_require = ['pytest', 'pytest-cov']
setup_requires = ['pytest-runner', 'multipledispatch']

setup(
    name="py_hcl",
    version=__version__,
    author="scutdig",
    author_email="zhongzc_arch@outlook.com",
    description=("A Hardware Construct Language"),
    license="MIT",
    url="https://github.com/scutdig/pyhcl",
    install_requires=install_requires,
    tests_require=tests_require,
    setup_requires=setup_requires,
    packages=find_packages(),
)
