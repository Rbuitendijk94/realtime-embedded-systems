from SimPyLC import *

class lift (Module):
    def __init__ (self):
        Module.__init__ (self)
        self.knopDeurOpen = Marker(False)

        self.motorAan = Marker(False)
        self.richtingMotor = Marker()
        self.positieLift = Register()
        self.doeDeurDicht = Marker(True)
        self.deurVergrendeld = Marker(False)
        self.Timerdeurvergrendelen = Timer()
        self.sensor = Marker(False)


    def sweep (self):
        self.positieLift.set( self.positieLift + 0.02, self.motorAan and self.richtingMotor)
        self.positieLift.set( self.positieLift - 0.02, self.motorAan and self.richtingMotor == False)

        #deur vergrendelen
        self.doeDeurDicht.mark(False, self.sensor or self.knopDeurOpen or self.deurVergrendeld)
        self.Timerdeurvergrendelen.reset(self.doeDeurDicht == False)
        self.deurVergrendeld.mark(True, self.Timerdeurvergrendelen > 2)





























'''
from SimPyLC import *

class lift (Module):
    def __init__ (self):
        Module.__init__ (self)
        self.mijnTimer = Timer()
        self.motorAan = Marker(True) # boolean
        self.positieLift = Register() # pos lift
        self.richtingMotor = Marker()
        self.snelheidLift = Register(-0.05) #snelheid van de lift
        self.noodknop = Marker(False)


    def sweep (self):
        self.positieLift.set( self.positieLift + self.snelheidLift,self.motorAan, self.richtingMotor)
        self.motorAan.mark( False ,self.positieLift> 3 or self.positieLift <-1) # max verdieping
        self.motorAan.mark (False,self.noodknop )
'''
