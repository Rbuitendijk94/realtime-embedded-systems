from SimPyLC import *

class containerkraan (Module):
    def __init__ (self):
        Module.__init__ (self)

        self.gewichtAanwezig = Marker()

    def sweep (self):
        #self.pompOpen.mark(True, self.startKnop)
