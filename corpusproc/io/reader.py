from corpusproc.core import Instance

class Reader(object):
    """ construct the reader with file handle. """
    def __init__(self, fp):
        self.fp = fp;

    """ to be overwrited. """
    def get(self):
        pass

    def seek(self, offset, whence=0):
        self.fp.seek(offset, whence)

class SegmentReader(Reader):
    """ """
    def get(self):
        line = self.fp.readline()

        if line == "":
            return None

        line = line.strip()

        inst = Instance()
        inst.forms = line.split()
        inst.raw   = "".join(inst.forms)

        return inst

class PostagReader(Reader):
    """ """
    def get(self):
        line = self.fp.readline()

        if line == "":
            return None

        line = line.strip()

        inst = Instance()
        inst.forms   = [word.rsplit("_")[0] for word in line.split()]
        inst.postags = [word.rsplit("_")[1] for word in line.split()]
        inst.raw     = "".join(inst.forms)

        return inst

class ConllReader(Reader):
    """ """
    def get(self):
        return None

class PlainReader(Reader):
    """ """
    def get(self):
        line = self.fp.readline()
        if line == "":
            return None
        line = line.strip()
        inst = Instance()
        inst.raw = line

        return inst

if __name__=="__main__":
    reader = SegmentReader(open("./data/segment.sample", "r"))

    while True:
        inst = reader.get()

        if inst is None:
            break

        print inst
