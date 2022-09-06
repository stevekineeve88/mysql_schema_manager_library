import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mysql_schema_manager",
    version="0.0.1",
    author="Stephen Ayre",
    author_email="stevemamajama@gmail.com",
    description="Schema manager for MySQL script files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stevekineeve88/mysql_schema_manager_library.git",
    packages=setuptools.find_packages(),
    install_requires=[
        "git+https://github.com/stevekineeve88/mysql_data_manager_library@VERSION-0.0.1"
    ],
    python_requires='>=3.7'
)
