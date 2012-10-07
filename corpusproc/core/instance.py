

class Instance(object):
    """ basic data struct for a instance
    """
    def __init__(self):
        """
        @param  content instance in string form
        @param  format  specify format of the content
        """
        self.raw        = None
        self.forms      = None
        self.lemmas     = None
        self.cpostags   = None
        self.postags    = None
        self.heads      = None

    def __len__(self):
        if self.forms is not None:
            return len(self.forms)
        else:
            return 0

    def __str__(self):
        return "\t".join(self.forms)
