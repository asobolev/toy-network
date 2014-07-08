"""
>>> import imp
>>> foo = imp.new_module("foo")
>>> foo_code = open("/home/andrey/projects/invariance/nest-build/lib/python2.7/site-packages/nest/hl_api.py", "r").read()
>>> exec foo_code in foo.__dict__
>>> foo.Foo.__module__
'foo'
>>>
"""

import imp
import uuid

nest_package_path = "/home/andrey/projects/invariance/nest-build/lib/" \
                "python2.7/site-packages/nest/"

nest_api_path = "/home/andrey/projects/invariance/nest-build/lib/" \
                "python2.7/site-packages/nest/hl_api.py"

nest_kernel_path = "/home/andrey/projects/invariance/nest-build/lib/" \
                "python2.7/site-packages/nest/pynestkernel.so"


def build_nest_module(api_module_path):
    module = imp.new_module("nest_" + uuid.uuid4().hex)
    module_code = open(api_module_path, "rb").read()
    exec module_code in module.__dict__
    import ipdb
    ipdb.set_trace()
    return module


class NetworkOne(object):

    def __init__(self):
        self.nst_one = build_nest_module(nest_kernel_path)
        self.nst_one.SetKernelStatus({"overwrite_files": True})


class NetworkTwo(object):

    def __init__(self):
        self.nst_two = build_nest_module(nest_kernel_path)
        self.nst_two.SetKernelStatus({"overwrite_files": False})


if __name__ == "__main__":

    import nest
    assert(nest.GetKernelStatus()["overwrite_files"] == False)

    n1 = NetworkOne()

    import ipdb

    assert(nest.GetKernelStatus()["overwrite_files"] == True)

    n2 = NetworkTwo()

    assert(nest.GetKernelStatus()["overwrite_files"] == False)