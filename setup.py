from setuptools import setup, find_namespace_packages


setup(
    name="pkt-trail-api-schema",
    version="0.0.1",
    author="Abhijit Gadgil",
    description="Schema support for Agent and API communication. Using JSON RPC 2.0 Schema.",
    packages=find_namespace_packages(include="pkttrail.*"),
    install_requires=["marshmallow"]
)
