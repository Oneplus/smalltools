#from corpusproc.core import Instance

class Writer(object):
    """ base class for writer """
    def __init__(self, fp):
        self.fp = fp

    def write(self, instance):
        pass

class SegmentWriter(Writer):
    """ """
    def write(self, instance):
        print >> self.fp, "\t".join(instance.forms)

if __name__=="__main__":
    pass
