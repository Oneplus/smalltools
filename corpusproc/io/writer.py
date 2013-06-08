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
        L = len(instance);
        for i in xrange(L):
            print >> self.fp, "%d\t%s\t%s\t%s_\t_\t%s\t%s\t_\t%s" % (
                    i + 1,
                    instance.forms[i],
                    ("_" if not instance.lemmas  else instance.lemmas[i]),
                    ("_" if not instance.postags else instance.postags[i]),
                    ("_" if not instance.heads   else str(instance.heads[i])),
                    ("_" if not instance.deprels else instance.deprels[i]),
                    ("_" if not instance.extras  else instance.extras[i]))

        print >> self.fp

class PlainWriter(Writer):
    """ """
    def write(self, instance):
        print >> self.fp, instance.raw

if __name__=="__main__":
    pass
