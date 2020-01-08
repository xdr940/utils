
from example_pkg_xdr94.part_1 import out
out()

from example_pkg_xdr94.part_2 import testC
a = testC()

from example_pkg_xdr94 import name,version
print(name,version)

import sys
for item in sys.path:
    print(item)