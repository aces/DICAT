class ClassTool():
    """
    Not used!  Useful for development as inheritable class  MyClass(ClassTool).
    """
    #no constructor
    def __repr__(self):
        attributes =[]
        for key in sorted(self.__dict__):
            attributes.append('%s=%s' %(key, getattr(self, key)))
        return ', '.join(attributes)

    def gatherattributes(self):
        attributes =[]
        for key in sorted(self.__dict__):
            attributes.append('%s' %(key))
        return ', '.join(attributes)

    def getframesize(self):
        print str(self.winfo_width())

