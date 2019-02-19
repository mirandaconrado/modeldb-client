from setuptools import setup

setup(
    name="verta",
    version="0.6.0",
    packages=[
        "verta",
        "verta._protos.modeldb",
    ],
    install_requires=[
        "googleapis-common-protos==1.5.6",
        "grpcio==1.17.1",
        "protobuf==3.6.1",
        "requests==2.21.0",
    ],
)
