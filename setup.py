import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="database_migration",
    version="0.0.1",

    description="In this course you will learn the value and process of moving from self-managed databases (on premises or in the cloud) into fully managed Amazon Web Services (AWS) database solutions.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="author",

    package_dir={"": "database_migration"},
    packages=setuptools.find_packages(where="database_migration"),

    install_requires=[
        "aws-cdk.core==1.70.0",
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
