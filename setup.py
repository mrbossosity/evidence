from setuptools import setup

with open("README.md", "rb") as f:
    long_descr = f.read()

setup(
    name="evidence with ease",
    version="1.0",
    packages=["evidence"],
    description="A nifty Python tool for expediting evidence printing.",
    long_description=long_descr,
    long_description_content_type="text/markdown", 
    entry_points = {
        "console-scripts":["evidence = evidence-with-ease.evidence:main"]
    },
    install_requires=[
        "requests",
        "lxml",
        "beautifulsoup4",
        "pdfkit",
        "PyPDF2"
    ],
    author="mrbossosity",
    author_email="mrbossosity@gmail.com"
)