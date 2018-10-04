from SimPyLC import *

class lift (Module):
    def __init__ (self):
        Module.__init__ (self)
        self.mijnTimer = Timer()
        self.motorAan = Marker(True) # true motoraan false motoruit
        self.positieLift = Register() # waar bevind lift zich nu getal tussen -1 en 3
        self.gewensteVerdieping = Register() #getal tussen -1 en 3

        self.snelheidLift = Register() #snelheid van de lift
        self.noodknop = Marker(False)


    def sweep (self):
        self.motorAan.mark( False, self.noodknop)
        self.snelheidLift.set(0.2)
        self.snelheidLift.set(0,self.positieLift %1 ==1)
        self.positieLift.set(self.positieLift + self.snelheidLift,(self.mijnTimer % 1)>0.95)# ,((self.mijnTimer % 1) ==1))



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
