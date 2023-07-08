from pathlib import Path
from setuptools import setup

README = (Path(__file__).parent / "README.md").read_text()

setup(
    name='gsclinks',
    version='1.0.5',
    description='Scrape backlink data from Google Search Console',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/tranngocminhhieu/google-search-console-links',
    author='Tran Ngoc Minh Hieu',
    author_email='tnmhieu@gmail.com',
    packages=['gsclinks'],
    install_requires=[
        'beautifulsoup4',
        'requests',
        'tqdm'
    ]
)