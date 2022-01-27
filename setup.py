import setuptools
with open("README.md", "r") as fh:
  long_description = fh.read()


setuptools.setup(
  name="flask-serialize",
  version="0.0.1",
  author="张斌",
  author_email="786017877@163.com",
  description="一个针对于flask框架的序列化工具",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/pypa/sampleproject",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)
