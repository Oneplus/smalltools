#!/usr/bin/env python
import os
import sys

try:
    # module has been installed
    from corpusproc.utils import sbc2dbc, dbc2sbc
except:
    # module not installed
    bin_path = os.path.realpath(__file__)
    bin_dir  = os.path.split(bin_path)[0]
    root_dir = os.path.join(bin_dir, "..")
    sys.path.append(root_dir)

    from corpusproc.utils import sbc2dbc, dbc2sbc

if __name__=="__main__":
    try:
        fp=open(sys.argv[1], "r")
    except:
        print >> sys.stderr, "Failed to open file"
        exit(1)

    for line in fp:
        print sbc2dbc(line.strip().decode("utf8")).encode("utf8")
