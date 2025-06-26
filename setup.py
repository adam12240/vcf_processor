from setuptools import setup, find_packages

setup(
    name="vcf_processor",
    version="0.1.0",
    py_modules=["vcf_processor"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "vcf_processor=vcf_processor:main",
        ],
    },
    author="Szabó Ádám",
    description="VCF fájl feldolgozó eszköz",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)
