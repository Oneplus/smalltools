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


class PostagWriter(Writer):
    """ """
    def write(self, instance):
        print >> self.fp, "\t".join(
                ["%s_%s" % (x[0], x[1]) for x in zip(instance.forms, instance.postags)])

class ConllWriter(Writer):
    """ """
    def write(self, instance):
        print >> self.fp


if __name__=="__main__":
    pass
