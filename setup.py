from distutils.core import setup
setup(
    name="normlap",
    version="0.0.2",
    description="A package enable normlize the overlap between networks. It also provides the method for randomizing network and randomizing subnetworks based on maximum entropy framework.",
    author="bingjie",
    py_modules=["normlap.Formatter","normlap.Helper","normlap.Pipeline","normlap.RandomNetwork","normlap.RandomSubnetwork"]
)
