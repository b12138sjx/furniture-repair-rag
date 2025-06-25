from setuptools import setup, find_packages

setup(
    name="furniture-repair-rag",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "langchain",
        "python-multipart",
        "pydantic"
    ]
)
