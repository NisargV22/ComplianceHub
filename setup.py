from setuptools import setup, find_packages

setup(
    name="compliancehub",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "SQLAlchemy",
        "pandas",
        "Jinja2",
        "WeasyPrint",
    ],
    entry_points={
        "console_scripts": [
            "compliancehub=compliancehub.cli:cli",
        ],
    },
)
