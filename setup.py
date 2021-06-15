from setuptools import setup, find_packages

setup(name="bb_parser",
      version="0.0.3",
      description="A parser for Blood Bowl 2 replay files",
      author="Grégoire Juge",
      author_email="gregoire.juge@gmail.com",
      packages=find_packages(where="src"),
      package_dir={"": "src"},
      install_requires=["lxml"],
      entry_points={
        'console_scripts': [
            'bb2_parser=bb_parser.cli:main',
        ]
      },
      extras_require={
            "dev": ["coverage"],
      },
      license="Apache 2.0")
