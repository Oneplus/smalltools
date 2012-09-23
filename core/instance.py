class Instance(object):
    """ """
    def __init__(self, content, format="CONLL", labeled=True):
        """
        @param  content instance in string form
        @param  format  specify format of the content
        """
        self.fv = None
        self.actParseTree = None

        self.forms = None
        self.lemmas = None
        self.cpostags = None
        self.postags = None
        self.feats = None
        self.heads = None
        self.deprels = None
        self.relFeats = None
        self.confidenceScore = None

        if format == "CONLL":
            lines = content.split("\n")
            self.forms = map(lambda l: l.split("\t")[1], lines)
            self.lemmas = map(lambda l: l.split("\t")[2], lines)
            self.cpostags = map(lambda l: l.split("\t")[3], lines)
            self.postags = map(lambda l: l.split("\t")[4], lines)
            self.feats = map(lambda l: l.split("\t")[5].split("|"), lines)
            self.heads = map(lambda l: int(l.split("\t")[6]), lines)
            self.deprels = map(lambda l: l.split("\t")[7] if labeled else 
                    "<no-type>", lines)

        elif format == "SEG":
            self.forms = content.split()

        elif format == "POS":
            separator = "/"
            self.forms = map(lambda wordtag: split(separator)[0], content.split())
            self.postag = map(lambda wordtag: split(separator)[1], content.split())

    def __len__(self):
        if self.forms is not None:
            return len(self.forms)
        else: return 0
