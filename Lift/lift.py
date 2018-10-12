from SimPyLC import *

class lift (Module):
    def __init__ (self):
        Module.__init__ (self)
        #knoppen in lift
        self.knopDeurOpen = Marker(False)
        self.knopDeurDicht = Marker(False)
        self.knopNood = Marker(False)
        self.knopVerdieping1 = Marker(False)
        self.knopVerdieping2 = Marker(False)
        self.knopVerdieping3 = Marker(False)
        self.knopVerdieping4 = Marker(False)
        self.knopVerdieping5 = Marker(False)
        #knoppen op verdieping
        self.roepLift = Marker()
        self.roepLiftVerdieping = Register(3)
        self.deurOpen = Marker(False)

        self.motorAan = Marker(False)
        self.richtingMotor = Marker()
        self.positieLift = Register(1)
        self.doeDeurDicht = Marker(True)
        self.deurVergrendeld = Marker(False)
        self.Timerdeurvergrendelen = Timer()
        self.TimerDeurOpen = Timer()
        self.sensor = Marker(False)


    def sweep (self):

        #deur vergrendelen
        self.doeDeurDicht.mark(True, self.knopDeurDicht)
        self.deurVergrendeld.mark(False, self.doeDeurDicht)
        self.doeDeurDicht.mark(False, self.sensor or self.knopDeurOpen or self.deurVergrendeld)
        self.Timerdeurvergrendelen.reset(self.doeDeurDicht == False)
        self.deurVergrendeld.mark(True, self.Timerdeurvergrendelen > 2)
        self.doeDeurDicht.mark(False, self.deurVergrendeld)

        #deur naar knopVerdieping
        self.richtingMotor.mark(False ,( self.positieLift > self.roepLiftVerdieping)== True)
        self.richtingMotor.mark(True , (self.positieLift < self.roepLiftVerdieping)== True)
        self.motorAan.mark(True,(self.positieLift *0.99> self.roepLiftVerdieping or self.positieLift *1.01 < self.roepLiftVerdieping )and self.deurVergrendeld  and self.knopNood == False, False)
        self.positieLift.set( self.positieLift + 0.02, self.motorAan and self.richtingMotor, self.positieLift)
        self.positieLift.set( self.positieLift - 0.02, self.motorAan and self.richtingMotor == False, self.positieLift)


        #deur open
        self.deurOpen.mark(True, (self.positieLift *0.99< self.roepLiftVerdieping or self.positieLift *1.01> self.roepLiftVerdieping ) and self.motorAan == False and self.doeDeurDicht == False , False )
        self.deurVergrendeld.mark(False, self.deurOpen )
        self.TimerDeurOpen.reset( self.deurOpen == False or self.deurVergrendeld )
        self.deurOpen.mark(False, self.doeDeurDicht and self.TimerDeurOpen >3)
        self.doeDeurDicht.mark(True, self.TimerDeurOpen >3)
        #zodra hij op de verdieping is zal de deur steeds weer open gaan tenzij verdieping wordt veranderd





















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
