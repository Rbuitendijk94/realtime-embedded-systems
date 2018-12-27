from SimPyLC import *

class wasmachine (Module):
    def __init__ (self):
        Module.__init__ (self)

        self.startKnop = Marker(True) #true starten , false stop
        self.programmakeuzeKnop= Register() # getal 0 tot 3 0 = katoen , 1 = wol, 2, zijde, 3 = syntetisch
        self.voorwasKnop = Marker(True)
        self.temperatuurKnop= Register(16)


        self.trommeldraait = Marker(False) # true aan, false uit
        self.pompOpen = Marker(False) # true aan , false uit
        self.kraanOpen = Marker(False) #true open, false dicht
        self.warmteElement = Marker(False) # true aan, false uit
        self.deurOpen = Marker(False)  #true dicth false open

        self.hoeveelheidWater = Register(0) # aantal liter water in de wasmachine max 20
        self.temperatuurWater = Register(15) # temperatuur van he waterWater
        self.trommelSnelheid =Register() # % in snelheid
        self.draaiProgramma = Register() # getal 0 tot 3 0 = katoen , 1 = wol, 2, zijde, 3 = syntetisch

        self.voorwasprogramma = Marker() # true starten , false niet doen
        self.zeepVoorwas = Marker()

        self.voorwassen = Marker  (False)
        self.voorwassenCompleet= Marker(False)
        self.timerVoorprogramma = Timer()

        self.uitspoelenVoorwas = Marker  (False)
        self.uitspoelenVoorwasCompleet = Marker(False)
        self.timeruitspoelenVoorwas = Timer()

        self.hoofdProgramma = Marker(False)
        self.zeepHoofdprogramma= Marker(False)

        self.hoofdwassen = Marker(False)
        self.hoofdwassenCompleet = Marker(False)
        self.timerHoofdprogramma = Timer()


        self.uitspoelen = Marker  (False)
        self.uitspoelenCompleet = Marker(False)
        self.timerUitspoelen = Timer()

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

        self.hoofdProgramma.mark(True, self.hoeveelheidWater == 0 and self.uitspoelenVoorwasCompleet and self.voorwassenCompleet)
        self.voorwasprogramma.mark(False, self.hoofdProgramma)
        self.voorwassen.mark(False, self.hoofdProgramma)
        self.voorwassenCompleet.mark(False, self.hoofdProgramma)
        self.uitspoelenVoorwas.mark(False, self.hoofdProgramma)
        self.uitspoelenVoorwasCompleet.mark(False, self.hoofdProgramma)
        self.voorwassenCompleet.mark(False, self.hoofdProgramma)
        self.zeepVoorwas.mark(False, self.hoofdProgramma)

        self.hoofdProgramma.mark(False, self.centrifugerenCompleet and self.hoeveelheidWater == 0)
        self.hoofdwassenCompleet.mark(False, self.hoofdProgramma == False)
        self.uitspoelenCompleet.mark(False, self.hoofdProgramma == False)
        self.uitspoelen.mark(False, self.hoofdProgramma == False)
        self.zeepHoofdprogramma.mark(False, self.hoofdProgramma == False)
        self.centrifugeren.mark(False, self.hoofdProgramma == False)
        self.centrifugerenCompleet.mark(False, self.hoofdProgramma == False)
        self.hoofdwassen.mark(False, self.hoofdProgramma == False)

        #pre
        self.pompOpen.mark(True, self.startKnop and self.hoeveelheidWater >0 and self.zeepVoorwas == False and self.voorwassen == False and self.uitspoelenVoorwas ==False and self.voorwasprogramma)
        #voorwasprogramma
        self.voorwasprogramma.mark(False, self.startKnop == False)
        self.hoofdProgramma.mark(False, self.startKnop == False)
        self.voorwasprogramma.mark(False, self.uitspoelenVoorwasCompleet and self.hoeveelheidWater ==0)
        self.zeepVoorwas.mark(True, self.voorwasprogramma and self.startKnop and self.pompOpen== False and self.hoeveelheidWater == 0 and self.voorwasprogramma)
        self.voorwassen.mark(True,   self.zeepVoorwas and self.voorwasprogramma)
        self.voorwassen.mark(False, self.voorwassenCompleet and self.voorwasprogramma)
        self.kraanOpen.mark(True, self.zeepVoorwas and self.voorwasprogramma and self.voorwassenCompleet == False and self.pompOpen == False and self.voorwassen and self.voorwasprogramma)
        self.hoeveelheidWater.set(10, self.hoeveelheidWater>10 and self.kraanOpen and self.voorwassen and self.voorwasprogramma)
        self.kraanOpen.mark(False, self.hoeveelheidWater == 10 and self.voorwassen  and self.voorwasprogramma)
        self.warmteElement.mark(True, self.hoeveelheidWater ==10 and self.kraanOpen == False and self.pompOpen == False and self.voorwassen and self.voorwasprogramma)
        self.warmteElement.mark(False, self.temperatuurKnop == self.temperatuurWater and self.voorwassen and self.voorwasprogramma)
        self.trommelSnelheid.set(10, self.warmteElement == False and self.pompOpen == False and self.kraanOpen== False and self.trommeldraait == False and self.voorwassenCompleet == False and  self.voorwasprogramma and self.voorwassen)
        self.trommeldraait.mark(True, self.trommelSnelheid ==10 and self.voorwassenCompleet == False and self.voorwassen and self.voorwasprogramma)
        self.trommeldraait.mark(False, self.voorwassenCompleet and self.voorwasprogramma)
        self.voorwassenCompleet.mark(True, self.timerVoorprogramma> 3 and self.voorwasprogramma)
        self.trommelSnelheid.set(0.,self.voorwassenCompleet and self.timerVoorprogramma >3 and self.voorwasprogramma)
        self.timerVoorprogramma.reset(self.timerVoorprogramma >3 or self.trommeldraait ==False or self.voorwassenCompleet == True or self.hoofdProgramma or self.uitspoelen)
        self.pompOpen.mark(True, self.voorwassenCompleet and self.trommelSnelheid ==0 and self.uitspoelenVoorwas == False and self.voorwasprogramma)
        self.uitspoelenVoorwas.mark(True, self.voorwassenCompleet and self.hoeveelheidWater ==0 and self.voorwasprogramma)
        self.kraanOpen.mark(True, self.voorwassenCompleet and self.trommelSnelheid ==0 and self.pompOpen == False and self.uitspoelenVoorwas and self.voorwasprogramma)
        self.hoeveelheidWater.set(10, self.hoeveelheidWater>10 and self.kraanOpen and self.uitspoelenVoorwas and self.voorwasprogramma)
        self.kraanOpen.mark(False, self.hoeveelheidWater == 10 and self.uitspoelenVoorwas and self.voorwasprogramma)
        self.trommelSnelheid.set(10, self.hoeveelheidWater ==10 and self.kraanOpen == False and self.pompOpen == False and self.uitspoelenVoorwas and self.voorwasprogramma)
        self.trommeldraait.mark(True, self.trommelSnelheid ==10 and self.uitspoelenVoorwasCompleet == False and self.uitspoelenVoorwas and self.voorwasprogramma)
        self.trommeldraait.mark(False, self.uitspoelenVoorwasCompleet  and self.voorwasprogramma)
        self.uitspoelenVoorwasCompleet.mark(True, self.timeruitspoelenVoorwas> 3  and self.voorwasprogramma)
        self.trommelSnelheid.set(0.,self.uitspoelenVoorwasCompleet and self.timeruitspoelenVoorwas >3 and self.voorwasprogramma)
        self.pompOpen.mark(True, self.uitspoelenVoorwasCompleet and self.voorwasprogramma  )
        self.hoeveelheidWater.set(0, self.hoeveelheidWater <0 and self.voorwasprogramma)
        self.pompOpen.mark(False,  self.hoeveelheidWater == 0 and self.voorwasprogramma)

        #hoofdProgramma
        self.zeepHoofdprogramma.mark(True, self.hoofdProgramma and self.startKnop and self.pompOpen == False and self.hoeveelheidWater == 0)
        self.hoofdwassen.mark(True, self.zeepHoofdprogramma and self.hoofdProgramma)
        self.hoofdwassen.mark(False,self.hoofdwassenCompleet and self.hoofdProgramma)
        self.kraanOpen.mark(True, self.hoofdProgramma and self.zeepHoofdprogramma and self.hoofdwassen and self.hoeveelheidWater< 10 and self.hoofdwassenCompleet== False  )
        self.hoeveelheidWater.set(10,self.hoeveelheidWater>10 and self.hoofdProgramma )
        self.kraanOpen.mark(False, self.hoeveelheidWater==10)
        self.warmteElement.mark(True, self.hoeveelheidWater==10 and self.kraanOpen== False and self.pompOpen == False and self.hoofdProgramma and self.hoofdwassen)
        self.warmteElement.mark(False, self.temperatuurKnop == self.temperatuurWater and self.hoofdProgramma)
        self.trommelSnelheid.set(20, self.hoofdProgramma and (self.programmakeuzeKnop == 0 or self.programmakeuzeKnop ==1 ) and self.warmteElement == False and self.temperatuurWater == self.temperatuurKnop)
        self.trommelSnelheid.set(10, self.hoofdProgramma and (self.programmakeuzeKnop == 2 or self.programmakeuzeKnop ==3 )and self.warmteElement == False)
        self.trommeldraait.mark(True, (self.trommelSnelheid == 20 or self.trommelSnelheid ==10 ) and self.hoofdwassenCompleet == False and self.hoofdProgramma)
        self.trommeldraait.mark(False, self.hoofdwassenCompleet and self.hoofdProgramma)
        self.hoofdwassenCompleet.mark(True,(self.programmakeuzeKnop == 0 or self.programmakeuzeKnop ==3 ) and self.timerHoofdprogramma >4 and self.hoofdProgramma)
        self.hoofdwassenCompleet.mark(True,(self.programmakeuzeKnop == 1 or self.programmakeuzeKnop ==2 ) and self.timerHoofdprogramma >4 and self.hoofdProgramma)
        self.timerHoofdprogramma.reset(self.timerHoofdprogramma> 20 or  self.hoofdwassenCompleet == True or self.hoofdwassen == False or self.trommelSnelheid == 0 or self.trommeldraait == False or self.hoofdProgramma == False)
        self.trommelSnelheid.set(0.,self.hoofdwassenCompleet  and self.hoofdProgramma)
        self.pompOpen.mark(True,  self.hoofdwassenCompleet and self.trommelSnelheid ==0 and self.uitspoelen == False and self.hoofdProgramma)
        self.uitspoelen.mark(True, self.hoofdwassenCompleet and self.hoeveelheidWater == 0 and self.hoofdProgramma)
        self.kraanOpen.mark(True, self.hoofdwassenCompleet and self.trommelSnelheid ==0 and self.pompOpen == False and self.uitspoelen and self.hoofdProgramma and self.uitspoelenCompleet == False)
        self.hoeveelheidWater.set(10, self.hoeveelheidWater>10 and self.kraanOpen and self.uitspoelen and self.hoofdProgramma)
        self.kraanOpen.mark(False, self.hoeveelheidWater == 10 and self.uitspoelen and self.hoofdProgramma)
        self.trommelSnelheid.set(10, self.hoeveelheidWater ==10 and self.kraanOpen == False and self.pompOpen == False and self.uitspoelen and self.hoofdProgramma)
        self.trommeldraait.mark(True, self.trommelSnelheid ==10 and self.uitspoelenCompleet == False and self.uitspoelen and self.hoofdProgramma)
        self.trommeldraait.mark(False, self.uitspoelenCompleet  and self.hoofdProgramma)
        self.uitspoelenCompleet.mark(True, self.timerUitspoelen> 2  and self.hoofdProgramma)
        self.trommelSnelheid.set(0.,self.uitspoelenCompleet and self.timerUitspoelen >3 and self.hoofdProgramma)
        self.pompOpen.mark(True, self.uitspoelenCompleet and self.hoofdProgramma and self.hoeveelheidWater !=0  )

        #in de opdracht staat er niet dat er nieuw water bij moet komen?
        self.centrifugeren.mark(True, self.uitspoelenCompleet and self.hoofdwassenCompleet and self.hoeveelheidWater == 0 and self.hoofdProgramma)
        self.trommelSnelheid.set(20, self.centrifugeren and self.hoofdProgramma)
        self.trommeldraait.mark(True, self.centrifugeren and self.trommelSnelheid !=0)
        self.trommeldraait.mark(False, self.timerCentrifugeren > 4 )
        self.centrifugerenCompleet.mark(True, self.timerCentrifugeren>4)
        self.pompOpen.mark(True, self.hoeveelheidWater> 0 and self.centrifugerenCompleet == True and self.hoofdProgramma)
        self.startKnop.mark(False, self.hoeveelheidWater == 0 and self.centrifugerenCompleet)
        self.timerCentrifugeren.reset( self.centrifugeren == False or self.timerCentrifugeren >5 or self.centrifugerenCompleet or self.trommelSnelheid == 0)

        self.timeruitspoelenVoorwas.reset(self.timerUitspoelen >3 or self.trommeldraait ==False or self.uitspoelenVoorwasCompleet == True or self.hoofdProgramma or self.voorwassen)
        self.timerUitspoelen.reset(self.timerUitspoelen >3 or self.trommeldraait ==False or self.uitspoelenCompleet == True or self.centrifugeren) #voorwasprogramma niet zeker
        self.timerUitspoelen.reset( self.uitspoelen == False)
        self.timerVoorprogramma.reset( self.voorwasprogramma == False)
        self.hoeveelheidWater.set(self.hoeveelheidWater +(2*world.period),self.kraanOpen)
        self.hoeveelheidWater.set(20, self.hoeveelheidWater>20 and self.kraanOpen)
        self.kraanOpen.mark(False, self.hoeveelheidWater == 20)
        self.pompOpen.mark(False, self.hoeveelheidWater == 0)
        self.hoeveelheidWater.set(self.hoeveelheidWater -(2*world.period),self.pompOpen)
        self.hoeveelheidWater.set(0, self.hoeveelheidWater <0)
