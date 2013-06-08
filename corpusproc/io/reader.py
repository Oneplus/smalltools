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
        line = self.fp.readline()
        if not line:
            return None

        inst = Instance()
        inst.forms   = []
        inst.postags = []
        inst.heads   = []
        inst.deprels = []
        inst.extras  = []
        inst.raw = ""
        line = line.strip()
        while len(line) > 0:
            splits = line.split()
            inst.forms.append( splits[1] )
            inst.postags.append( splits[3] )
            inst.heads.append( int(splits[6]) )
            inst.deprels.append( splits[7] )
            if splits[9] != "_":
                inst.extras.append( splits[7] )
            inst.raw += splits[1]

            line = self.fp.readline()
            if not line:
                break

            line = line.strip()

        if len(inst.extras) == 0:
            inst.extras = None
        return inst

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
