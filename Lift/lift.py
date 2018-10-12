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
        self.knopVerdieping3 = Marker(True)
        self.knopVerdieping4 = Marker(False)
        self.knopVerdieping5 = Marker(True)
        #knoppen op verdieping
        self.verdieping1 = Marker()
        self.verdieping2 = Marker()
        self.verdieping3 = Marker()
        self.verdieping4 = Marker()
        self.verdieping5 = Marker()


        self.LiftLogica = Register(-1)
        self.deurOpen = Marker(False)

        self.motorAan = Marker(False)
        self.richtingMotor = Marker(True)
        self.positieLift = Register(-1)
        self.doeDeurDicht = Marker(True)
        self.deurVergrendeld = Marker(False)
        self.Timerdeurvergrendelen = Timer()
        self.TimerDeurOpen = Timer()
        self.sensor = Marker(False)


    def sweep (self):
        #logica
        self.positieLift.set(3, self.positieLift>3)
        self.positieLift.set(-1, self.positieLift <-1)


        #deur vergrendelen
        self.doeDeurDicht.mark(True, self.knopDeurDicht)
        self.deurVergrendeld.mark(False, self.doeDeurDicht)
        self.doeDeurDicht.mark(False, self.sensor or self.knopDeurOpen or self.deurVergrendeld)
        self.Timerdeurvergrendelen.reset(self.doeDeurDicht == False)
        self.deurVergrendeld.mark(True, self.Timerdeurvergrendelen > 2)
        self.doeDeurDicht.mark(False, self.deurVergrendeld)

        #deur naar knopVerdieping'
        self.positieLift.set( self.positieLift + 0.02, self.motorAan and self.richtingMotor)
        self.positieLift.set( self.positieLift - 0.02, self.motorAan and self.richtingMotor == False)
        self.richtingMotor.mark(False , self.positieLift > self.LiftLogica)
        self.richtingMotor.mark(True , self.positieLift < self.LiftLogica)
        self.motorAan.mark(True, self.positieLift > self.LiftLogica or  self.positieLift < self.LiftLogica, False )
        self.motorAan.mark(False, self.deurVergrendeld == False or self.knopNood)
        self.motorAan.mark(False,(self.positieLift +0.02> self.LiftLogica and self.positieLift -0.02 < self.LiftLogica ))


        #deur open
        self.deurOpen.mark(True, (self.positieLift *0.99< self.LiftLogica or self.positieLift *1.01> self.LiftLogica ) and self.motorAan == False and self.doeDeurDicht == False , False )
        self.deurVergrendeld.mark(False, self.deurOpen )
        self.TimerDeurOpen.reset( self.deurOpen == False or self.deurVergrendeld )
        self.deurOpen.mark(False, self.doeDeurDicht and self.TimerDeurOpen >5)
        self.doeDeurDicht.mark(True, self.TimerDeurOpen >5)
        #zodra hij op de verdieping is zal de deur steeds weer open gaan tenzij verdieping wordt veranderd


        #zijn er 2 geselecteerd?
        self.richtingMotor.mark(True, self.positieLift < self.LiftLogica and (self.knopVerdieping5 or self.knopVerdieping4  or self.knopVerdieping3 or  self.knopVerdieping2),False )

        #als lift naar boven moet
        self.LiftLogica.set(3,  self.knopVerdieping5 or self.verdieping5)
        self.LiftLogica.set(2,  self.knopVerdieping4 or self.verdieping4)
        self.LiftLogica.set(1,  self.knopVerdieping3 or self.verdieping3)
        self.LiftLogica.set(0,  self.knopVerdieping2 or self.verdieping2)
        self.LiftLogica.set(-1, self.knopVerdieping1 or self.verdieping1)
        #als lift naar beneden gaat



        #knop uit zetten als lift op verdieping is
        self.knopVerdieping1.mark(False, self.LiftLogica == -1 and self.deurOpen and  (self.positieLift +0.02> self.LiftLogica and self.positieLift -0.02))
        self.knopVerdieping2.mark(False, self.LiftLogica == 0 and self.deurOpen and  (self.positieLift +0.02> self.LiftLogica and self.positieLift -0.02))
        self.knopVerdieping3.mark(False, self.LiftLogica == 1 and self.deurOpen and  (self.positieLift +0.02> self.LiftLogica and self.positieLift -0.02))
        self.knopVerdieping4.mark(False, self.LiftLogica == 2 and self.deurOpen and  (self.positieLift +0.02> self.LiftLogica and self.positieLift -0.02))
        self.knopVerdieping5.mark(False, self.LiftLogica == 3 and self.deurOpen and  (self.positieLift +0.02> self.LiftLogica and self.positieLift -0.02))

        #knop uit zetten als lift op verdieping is
        self.verdieping1.mark(False, self.LiftLogica == -1 and self.deurOpen and  (self.positieLift +0.02> self.LiftLogica and self.positieLift -0.02))
        self.verdieping2.mark(False, self.LiftLogica == 0 and self.deurOpen and  (self.positieLift +0.02> self.LiftLogica and self.positieLift -0.02))
        self.verdieping3.mark(False, self.LiftLogica == 1 and self.deurOpen and  (self.positieLift +0.02> self.LiftLogica and self.positieLift -0.02))
        self.verdieping4.mark(False, self.LiftLogica == 2 and self.deurOpen and  (self.positieLift +0.02> self.LiftLogica and self.positieLift -0.02))
        self.verdieping5.mark(False, self.LiftLogica == 3 and self.deurOpen and  (self.positieLift +0.02> self.LiftLogica and self.positieLift -0.02))


'''
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
        self.knopVerdieping3 = Marker(True)
        self.knopVerdieping4 = Marker(True)
        self.knopVerdieping5 = Marker(False)
        #knoppen op verdieping
        self.verdieping1 = Marker()
        self.verdieping2 = Marker()
        self.verdieping3 = Marker()
        self.verdieping4 = Marker()
        self.verdieping5 = Marker()


        self.LiftLogica = Register(-1)
        self.deurOpen = Marker(False)

        self.motorAan = Marker(False)
        self.richtingMotor = Marker(True)
        self.positieLift = Register(-1)
        self.doeDeurDicht = Marker(True)
        self.deurVergrendeld = Marker(False)
        self.Timerdeurvergrendelen = Timer()
        self.TimerDeurOpen = Timer()
        self.sensor = Marker(False)


    def sweep (self):
        #logica
        self.positieLift.set(3, self.positieLift>3)
        self.positieLift.set(-1, self.positieLift <-1)


        #deur vergrendelen
        self.doeDeurDicht.mark(True, self.knopDeurDicht)
        self.deurVergrendeld.mark(False, self.doeDeurDicht)
        self.doeDeurDicht.mark(False, self.sensor or self.knopDeurOpen or self.deurVergrendeld)
        self.Timerdeurvergrendelen.reset(self.doeDeurDicht == False)
        self.deurVergrendeld.mark(True, self.Timerdeurvergrendelen > 2)
        self.doeDeurDicht.mark(False, self.deurVergrendeld)

        #deur naar knopVerdieping'
        self.positieLift.set( self.positieLift + 0.02, self.motorAan and self.richtingMotor)
        self.positieLift.set( self.positieLift - 0.02, self.motorAan and self.richtingMotor == False)
        self.richtingMotor.mark(False , self.positieLift > self.LiftLogica)
        self.richtingMotor.mark(True , self.positieLift < self.LiftLogica)
        self.motorAan.mark(True, self.positieLift > self.LiftLogica or  self.positieLift < self.LiftLogica, False )
        self.motorAan.mark(False, self.deurVergrendeld == False or self.knopNood)
        self.motorAan.mark(False,(self.positieLift +0.02> self.LiftLogica and self.positieLift -0.02 < self.LiftLogica ))



        #deur open
        self.deurOpen.mark(True, (self.positieLift *0.99< self.LiftLogica or self.positieLift *1.01> self.LiftLogica ) and self.motorAan == False and self.doeDeurDicht == False , False )
        self.deurVergrendeld.mark(False, self.deurOpen )
        self.TimerDeurOpen.reset( self.deurOpen == False or self.deurVergrendeld )
        self.deurOpen.mark(False, self.doeDeurDicht and self.TimerDeurOpen >3)
        self.doeDeurDicht.mark(True, self.TimerDeurOpen >3)
        #zodra hij op de verdieping is zal de deur steeds weer open gaan tenzij verdieping wordt veranderd


        #verdieping logica
        #als lift naar boven moet
        self.LiftLogica.set(3, self.richtingMotor and self.positieLift <3 and(self.knopVerdieping5 or self.verdieping5))
        self.LiftLogica.set(2, self.richtingMotor and self.positieLift <2 and(self.knopVerdieping4 or self.verdieping4))
        self.LiftLogica.set(1, self.richtingMotor and self.positieLift <1 and(self.knopVerdieping3 or self.verdieping3))
        self.LiftLogica.set(0, self.richtingMotor and self.positieLift <0 and(self.knopVerdieping2 or self.verdieping2))

        #als lift naar beneden gaat
        self.LiftLogica.set(-1, self.richtingMotor == False and self.positieLift >0 and(self.knopVerdieping1 or self.verdieping1))
        self.LiftLogica.set(0, self.richtingMotor == False and self.positieLift >0 and(self.knopVerdieping2 or self.verdieping2))
        self.LiftLogica.set(1, self.richtingMotor == False and self.positieLift >0 and(self.knopVerdieping3 or self.verdieping3))
        self.LiftLogica.set(2, self.richtingMotor == False and self.positieLift >0 and(self.knopVerdieping4 or self.verdieping4))

        #knop uit zetten als lift op verdieping is
        self.knopVerdieping1.mark(False, self.LiftLogica == -1 and self.deurOpen and  (self.positieLift +0.02> self.LiftLogica and self.positieLift -0.02))
        self.knopVerdieping2.mark(False, self.LiftLogica == 0 and self.deurOpen and  (self.positieLift +0.02> self.LiftLogica and self.positieLift -0.02))
        self.knopVerdieping3.mark(False, self.LiftLogica == 1 and self.deurOpen and  (self.positieLift +0.02> self.LiftLogica and self.positieLift -0.02))
        self.knopVerdieping4.mark(False, self.LiftLogica == 2 and self.deurOpen and  (self.positieLift +0.02> self.LiftLogica and self.positieLift -0.02))
        self.knopVerdieping5.mark(False, self.LiftLogica == 3 and self.deurOpen and  (self.positieLift +0.02> self.LiftLogica and self.positieLift -0.02))

        #knop uit zetten als lift op verdieping is
        self.verdieping1.mark(False, self.LiftLogica == -1 and self.deurOpen and  (self.positieLift +0.02> self.LiftLogica and self.positieLift -0.02))
        self.verdieping2.mark(False, self.LiftLogica == 0 and self.deurOpen and  (self.positieLift +0.02> self.LiftLogica and self.positieLift -0.02))
        self.verdieping3.mark(False, self.LiftLogica == 1 and self.deurOpen and  (self.positieLift +0.02> self.LiftLogica and self.positieLift -0.02))
        self.verdieping4.mark(False, self.LiftLogica == 2 and self.deurOpen and  (self.positieLift +0.02> self.LiftLogica and self.positieLift -0.02))
        self.verdieping5.mark(False, self.LiftLogica == 3 and self.deurOpen and  (self.positieLift +0.02> self.LiftLogica and self.positieLift -0.02))
'''
