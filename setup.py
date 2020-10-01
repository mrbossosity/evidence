from setuptools import setup

with open("README.md", "r") as f:
    long_descr = f.read()

setup(
    name="evidence with ease",
    version="1.1.2",
    packages=["evidence"],
    description="A nifty Python tool for expediting evidence printing.",
    long_description=long_descr,
    long_description_content_type="text/markdown", 
    entry_points = {
        "console_scripts":["evidence = evidence.__main__:main"]
    },
    install_requires=[
        "requests",
        "lxml",
        "beautifulsoup4",
        "pdfkit",
        "PyPDF2"
    ],
    author="mrbossosity",
    author_email="mrbossosity@gmail.com",
    url="https://github.com/mrbossosity/evidence"
)