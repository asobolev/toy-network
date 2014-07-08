"""
>>> import imp
>>> foo = imp.new_module("foo")
>>> foo_code = "a = 5"
>>> exec foo_code in foo.__dict__
>>> foo.Foo.__module__
'foo'
>>>
"""


class NetworkOne(object):

    def __init__(self):
        self.nst_one = __import__("nest")
        self.nst_one.SetKernelStatus({"overwrite_files": True})


class NetworkTwo(object):

    def __init__(self):
        self.nst_two = __import__("nest")
        self.nst_two.SetKernelStatus({"overwrite_files": False})


if __name__ == "__main__":

    import nest
    assert(nest.GetKernelStatus()["overwrite_files"] == False)

    n1 = NetworkOne()

    import ipdb

    assert(nest.GetKernelStatus()["overwrite_files"] == True)

    n2 = NetworkTwo()

    assert(nest.GetKernelStatus()["overwrite_files"] == False)