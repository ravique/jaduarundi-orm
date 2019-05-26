import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jaguarundi-orm",
    version="dev",
    author="Andrei Etmanov",
    author_email="andres@space-coding.ru",
    description="Simple SQLite ORM for Python 3.6+",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ravique/jaduarundi-orm.git",
    py_modules={'db_handler', 'models', '__init__', 'config'},
    packages=setuptools.find_packages(),
    scripts=['jaguarundi/models.py'],
    license="MIT",
)
