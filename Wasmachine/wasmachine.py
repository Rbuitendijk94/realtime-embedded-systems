from SimPyLC import *

class wasmachine (Module):
    def __init__ (self):
        Module.__init__ (self)

        self.startKnop = Marker(True) #true starten , false stop
        self.deurOpen = Marker(False)  #true dicth false open
        self.programmakeuzeKnop= Register() # getal 0 tot 3 0 = katoen , 1 = wol, 2, zijde, 3 = syntetisch
        self.draaiProgramma = Register() # getal 0 tot 3 0 = katoen , 1 = wol, 2, zijde, 3 = syntetisch
        self.voorwasKnop = Marker(False)
        self.temperatuurKnop= Register(16)

        self.trommelSnelheid =Register() # % in snelheid
        self.trommeldraait = Marker(False) # true aan, false uit

        self.pompOpen = Marker(False) # true aan , false uit
        self.kraanOpen = Marker(False) #true open, false dicht
        self.warmteElement = Marker(False) # true aan, false uit
        self.hoeveelheidWater = Register(10) # aantal liter water in de wasmachine max 20
        self.temperatuurWater = Register(15) # temperatuur van he waterWater

        self.voorwasprogramma = Marker() # true starten , false niet doen
        self.zeepVoorwas = Marker()
        self.voorwassen = Marker  (False)
        self.voorwassenCompleet= Marker(False)
        self.timerVoorprogramma = Timer()

        self.uitspoelen = Marker  (False)
        self.uitspeolenCompleet = Marker(False)
        self.uitspoelenVoorprogramma = Marker(False)
        self.timerUitspoelen = Timer()

        self.hoofdProgramma = Marker(True)
        self.zeepHoofdprogramma= Marker(True)

        self.hoofdwassen = Marker(False)
        self.hoofdwassenCompleet = Marker(False)
        self.timerHoofdprogramma = Timer()
        self.centrifugeren= Marker(False)
        self.centrifugerenCompleet = Marker(False)
        self.timerCentrifugeren = Timer()



    def sweep (self):

        self.temperatuurWater.set(self.temperatuurWater + ((world.period*3) / 4.2), self.warmteElement)
        self.temperatuurWater.set(self.temperatuurKnop, self.temperatuurWater> self.temperatuurKnop and self.warmteElement)
        self.warmteElement.mark(False, self.temperatuurKnop == self.temperatuurWater)# bi elke zetten
        self.temperatuurWater.set(15, self.hoeveelheidWater ==0)
        self.deurOpen.mark(False, self.hoeveelheidWater!= 0 or self.trommeldraait)
        self.kraanOpen.mark(False, self.deurOpen)
        self.pompOpen.mark(False, self.kraanOpen)
        self.voorwasprogramma.mark(False, self.deurOpen)
        self.hoofdProgramma.mark(False, self.deurOpen)
        self.draaiProgramma.set(self.programmakeuzeKnop, self.draaiProgramma != self.programmakeuzeKnop)
        self.temperatuurKnop.set(60, self.temperatuurKnop > 60 and self.programmakeuzeKnop == 1)
        self.temperatuurKnop.set(40, self.temperatuurKnop > 40 and self.programmakeuzeKnop == 2)
        self.voorwasprogramma.mark(True, self.voorwasKnop and self.startKnop)
        self.hoofdProgramma.mark(True, self.voorwasKnop == False and self.startKnop)

        self.pompOpen.mark(True, self.startKnop and self.hoeveelheidWater >0 and self.zeepVoorwas == False and self.voorwassen == False and self.uitspoelen ==False and self.voorwasprogramma)
        #voorwasprogramma

        self.voorwasprogramma.mark(False, self.uitspeolenCompleet and self.hoeveelheidWater ==0)
        self.zeepVoorwas.mark(True, self.voorwasprogramma and self.startKnop and self.pompOpen== False and self.hoeveelheidWater == 0 and self.voorwasprogramma)
        self.voorwassen.mark(True,   self.zeepVoorwas and self.voorwasprogramma)
        self.voorwassen.mark(False, self.voorwassenCompleet and self.voorwasprogramma)
        self.kraanOpen.mark(True, self.zeepVoorwas and self.voorwasprogramma and self.voorwassenCompleet == False and self.pompOpen == False and self.voorwassen and self.voorwasprogramma)
        self.hoeveelheidWater.set(10, self.hoeveelheidWater>10 and self.kraanOpen and self.voorwassen and self.voorwasprogramma)
        self.kraanOpen.mark(False, self.hoeveelheidWater == 10 and self.voorwassen  and self.voorwasprogramma)
        self.warmteElement.mark(True, self.hoeveelheidWater ==10 and self.kraanOpen == False and self.pompOpen == False and self.voorwassen and self.voorwasprogramma)
        self.warmteElement.mark(False, self.temperatuurKnop == self.temperatuurWater and self.voorwassen)
        self.trommelSnelheid.set(10, self.warmteElement == False and self.pompOpen == False and self.kraanOpen== False and self.trommeldraait == False and self.voorwassenCompleet == False and  self.voorwasprogramma and self.voorwassen)
        self.trommeldraait.mark(True, self.trommelSnelheid ==10 and self.voorwassenCompleet == False and self.voorwassen and self.voorwasprogramma)
        self.trommeldraait.mark(False, self.voorwassenCompleet and self.voorwasprogramma)
        self.voorwassenCompleet.mark(True, self.timerVoorprogramma> 3 and self.voorwasprogramma)
        self.trommelSnelheid.set(0.,self.voorwassenCompleet and self.timerVoorprogramma >3 and self.voorwasprogramma)
        self.timerVoorprogramma.reset(self.timerVoorprogramma >3 or self.trommeldraait ==False or self.voorwassenCompleet == True)
        self.pompOpen.mark(True, self.voorwassenCompleet and self.trommelSnelheid ==0 and self.uitspoelen == False and self.voorwasprogramma)
        self.uitspoelen.mark(True, self.voorwassenCompleet and self.hoeveelheidWater ==0 and self.voorwasprogramma)
        self.kraanOpen.mark(True, self.voorwassenCompleet and self.trommelSnelheid ==0 and self.pompOpen == False and self.uitspoelen and self.voorwasprogramma)
        self.hoeveelheidWater.set(10, self.hoeveelheidWater>10 and self.kraanOpen and self.uitspoelen and self.voorwasprogramma)
        self.kraanOpen.mark(False, self.hoeveelheidWater == 10 and self.uitspoelen and self.voorwasprogramma)
        self.trommelSnelheid.set(10, self.hoeveelheidWater ==10 and self.kraanOpen == False and self.pompOpen == False and self.uitspoelen and self.voorwasprogramma)
        self.trommeldraait.mark(True, self.trommelSnelheid ==10 and self.uitspeolenCompleet == False and self.uitspoelen and self.voorwasprogramma)
        self.trommeldraait.mark(False, self.uitspeolenCompleet  and self.voorwasprogramma)
        self.uitspeolenCompleet.mark(True, self.timerUitspoelen> 3  and self.voorwasprogramma)
        self.trommelSnelheid.set(0.,self.uitspeolenCompleet and self.timerUitspoelen >3 and self.voorwasprogramma)
        self.pompOpen.mark(True, self.uitspeolenCompleet and self.voorwasprogramma  )
        self.timerUitspoelen.reset(self.timerUitspoelen >3 or self.trommeldraait ==False or self.uitspeolenCompleet == True)
        self.timerUitspoelen.reset( self.uitspoelen == False)

        #hoofdProgramma
        self.pompOpen.mark(True, self.startKnop and self.hoeveelheidWater >0 and self.zeepHoofdprogramma == False  and self.hoofdporgramma)
        self.zeepHoofdprogramma.mark(True, self.hoofdProgramma and self.startKnop and self.pompOpen == False and self.hoeveelheidWater == 0 and self.hoofdProgramma)
        self.hoofdwassen.mark(True, self.hoofdProgramma and self.zeepHoofdprogramma )






        self.hoeveelheidWater.set(self.hoeveelheidWater +(2*world.period),self.kraanOpen)
        self.hoeveelheidWater.set(20, self.hoeveelheidWater>20 and self.kraanOpen)
        self.kraanOpen.mark(False, self.hoeveelheidWater == 20)
        self.pompOpen.mark(False, self.hoeveelheidWater == 0)
        self.hoeveelheidWater.set(self.hoeveelheidWater -(2*world.period),self.pompOpen)
        self.hoeveelheidWater.set(0, self.hoeveelheidWater <0 )
