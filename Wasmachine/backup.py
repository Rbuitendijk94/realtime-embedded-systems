from SimPyLC import *

class wasmachine (Module):
    def __init__ (self):
        Module.__init__ (self)

        self.startKnop = Marker(False) #true starten , false stop
        self.deurOpen = Marker(False)  #true dicth false open
        self.programmakeuzeKnop= Register() # getal 0 tot 3 0 = katoen , 1 = wol, 2, zijde, 3 = syntetisch
        self.draaiProgramma = Register() # getal 0 tot 3 0 = katoen , 1 = wol, 2, zijde, 3 = syntetisch
        self.voorwasKnop = Marker(True)

        self.warmteElement = Marker(False) # true aan, false uit
        self.pompOpen = Marker(False) # true aan , false uit
        self.trommelSnelheid =Register() # % in snelheid
        self.trommeldraait = Marker(False) # true aan, false uit
        self.temperatuurWater = Register(15) # temperatuur van he waterWater
        self.kraanOpen = Marker(False) #true open, false dicht

        self.hoeveelheidWater = Register(5) # aantal liter water in de wasmachine max 20
        self.hoofdProgramma = Marker()
        self.zeepHoofdprogramma= Register(10)




        self.voorwasprogramma = Marker() # true starten , false niet doen
        self.zeepVoorwas = Marker()
        self.timerVoorprogrammaStart = Marker(False)
        self.timerVoorprogramma = Timer()
        self.voorProgrammaKlaar = Marker(False)
        self.uitspoelenVoorprogramma = Marker(False)
        self.timerUitspoelenVoorprogramma = Timer()


    def sweep (self):


        #self.pompOpen.mark(True, self.startKnop)
        self.hoeveelheidWater.set(self.hoeveelheidWater + 0.1, self.kraanOpen , self.hoeveelheidWater)
        self.hoeveelheidWater.set(self.hoeveelheidWater - 0.1, self.pompOpen , self.hoeveelheidWater)
        self.hoeveelheidWater.set(20, self.hoeveelheidWater >20)
        self.hoeveelheidWater.set(0, self.hoeveelheidWater <0)
        self.temperatuurWater.set((2.5/self.hoeveelheidWater)+self.temperatuurWater, self.warmteElement, self.temperatuurWater) #/wordrt 1.5


        self.deurOpen.mark(True, self.hoeveelheidWater >0 or self.trommeldraait)
        self.trommeldraait.mark(False, self.deurOpen)
        self.pompOpen.mark(False, self.hoeveelheidWater<0)
        self.startKnop.mark(False ,self.deurOpen)
        self.draaiProgramma.set(self.programmakeuzeKnop, self.startKnop ==False)
        self.startKnop.mark(False, self.draaiProgramma == self.programmakeuzeKnop, False)

        self.temperatuurWater.set(60, self.temperatuurWater> 60 and self.programmakeuzeKnop == 1)
        self.temperatuurWater.set(40, self.temperatuurWater> 40 and self.programmakeuzeKnop == 2)
        self.temperatuurWater.set(40, self.temperatuurWater> 40 and self.programmakeuzeKnop == 0)
        self.temperatuurWater.set(40, self.temperatuurWater> 40 and self.programmakeuzeKnop == 3)

        #voorwasprogramma
        self.voorwasprogramma.mark(True, self.voorwasKnop and self.startKnop)
        self.zeepVoorwas.mark(True, self.voorwasprogramma)
        self.kraanOpen.mark(True, self.zeepVoorwas and self.hoeveelheidWater <10 and( self.timerVoorprogramma) <3,False) #TIMER ANDERS ISNTELLEN
        self.hoeveelheidWater.set(10, self.hoeveelheidWater >10 and self.voorwasprogramma and self.voorProgrammaKlaar == False)
        self.warmteElement.mark(True, self.hoeveelheidWater ==10 and self.voorwasprogramma and self.voorProgrammaKlaar == False)
        self.warmteElement.mark(False,(self.programmakeuzeKnop ==1 and self.temperatuurWater ==60)or self.temperatuurWater == 40 and self.voorwasprogramma )
        self.trommelSnelheid.set(10,self.hoeveelheidWater == 10 and self.voorwasprogramma and self.warmteElement == False)
        self.trommeldraait.mark(True, self.trommelSnelheid ==10 and self.voorwasprogramma)
        self.timerVoorprogrammaStart.mark(True, self.trommelSnelheid == 10 and self.voorwasprogramma)
        self.timerVoorprogramma.reset(self.timerVoorprogrammaStart == False )
        self.trommeldraait.mark(False, self.timerVoorprogramma >3 and self.voorwasprogramma)#TIMER ANDERS ISNTELLEN
        self.pompOpen.mark(True, self.timerVoorprogramma >1.5 and self.uitspoelenVoorprogramma == False and self.voorwasprogramma)#TIMER ANDERS ISNTELLEN
        self.pompOpen.mark(False, self.hoeveelheidWater <0.1 and self.voorwasprogramma )
        self.trommelSnelheid.set(0, self.hoeveelheidWater <0.1 and self.voorwasprogramma)
        self.uitspoelenVoorprogramma.mark(True, self.timerVoorprogramma >1.5 and self.pompOpen == False and self.voorwasprogramma)
        self.kraanOpen.mark(True, self.uitspoelenVoorprogramma and self.hoeveelheidWater <10 and self.trommelSnelheid ==0 and self.timerUitspoelenVoorprogramma <3 and self.voorwasprogramma)
        self.timerUitspoelenVoorprogramma.reset(self.uitspoelenVoorprogramma == False and self.voorProgrammaKlaar == False )
        self.trommeldraait.mark(True, self.trommelSnelheid ==10 and self.uitspoelenVoorprogramma and self.hoeveelheidWater==10 and self.voorwasprogramma)
        self.trommeldraait.mark(False, self.timerUitspoelenVoorprogramma >2 and self.voorwasprogramma and self.uitspoelenVoorprogramma and self.voorwasprogramma)#TIMER ANDERS ISNTELLEN
        self.pompOpen.mark(True, self.timerUitspoelenVoorprogramma >2 and self.uitspoelenVoorprogramma and self.voorProgrammaKlaar == False and self.voorwasprogramma)#TIMER ANDERS ISNTELLEN
        self.pompOpen.mark(False, self.hoeveelheidWater <0.1 and self.voorProgrammaKlaar == False and self.voorwasprogramma)
        self.voorProgrammaKlaar.mark(True, self.hoeveelheidWater <0.1 and self.uitspoelenVoorprogramma and self.timerUitspoelenVoorprogramma >5 and self.voorwasprogramma)
        self.timerUitspoelenVoorprogramma.reset(self.voorProgrammaKlaar == True )
        self.timerVoorprogramma.reset(self.voorProgrammaKlaar == True)

        #start hoofdProgramma
        self.hoofdProgramma.mark(True, self.startKnop and (self.voorwasKnop == False or self.voorProgrammaKlaar))

'''
        #start hoofdporgramma
        self.hoofdProgramma.mark(True, self.voorwasprogramm == False and self.startKnop)
        self.zeepHoofdprogramma.set(self.zeepHoofdprogramma-0.1, self.hoofdProgramma, self.zeepHoofdprogramma )
        self.zeepHoofdprogramma.set(0 , self.zeepHoofdprogramma <0)
        self.kraanOpen.mark(True, self.zeepHoofdprogramma ==0 and self.hoofdProgramma)
        self.hoeveelheidWater.set(self.hoeveelheidWater + 0.2, self.hoeveelheidWater <10 and self.zeepHoofdprogramma ==0 and self.kraanOpen)
        self.kraanOpen.mark(False, self.hoeveelheidWater == 10)
        #zet timer voor wol of zijde op 2 minuten
        # zet timer voor katoen of  syntetisch op 3 min
        #self.trommelSnelheid.set(20, self.draaiProgramma == 0, 10)
    #    self.trommelSnelheid.set(0, self.timerKlaar)# timer voorbij is
    #    self.trommeldraait.mark(False, self.hoofdProgramma and self.timerKlaar ==False and self.zeepHoofdprogramma <0 and self.trommelSnelheid != 0)
    #    self.pompOpen.mark(True, self.hoofdProgramma and self.zeepHoofdprogramma > 0 and self.timerKlaar and self.hoeveelheidWater <0.2 and self.kraanOpen)
'''

        #start het programma naar keuze als het gestard wort
'''
from SimPyLC import *
    def sweep (self):
        self.hoeveelheidWater.set(self.hoeveelheidWater + 0.5, self.kraanOpen , self.hoeveelheidWater)
        self.hoeveelheidWater.set(self.hoeveelheidWater - 0.05, self.pompOpen , self.hoeveelheidWater)
        self.hoeveelheidWater.set(20, self.hoeveelheidWater >20)
        self.temperatuurWaterKcal.set((self.temperatuurWaterKcal)+1.5,self.warmteElement, self.hoeveelheidWater*4.2)
        self.temperatuurWater.set(14 + self.temperatuurWaterKcal/self.hoeveelheidWater/4.2)
warmt het water op
        self.hoeveelheidWater.set(self.hoeveelheidWater + 0.5, self.kraanOpen , self.hoeveelheidWater)
        self.hoeveelheidWater.set(self.hoeveelheidWater - 0.05, self.pompOpen , self.hoeveelheidWater)
        self.hoeveelheidWater.set(20, self.hoeveelheidWater >20)
        self.temperatuurWater.set((1.5/self.hoeveelheidWater)+self.temperatuurWater, self.warmteElement, self.temperatuurWater)
 water warmt op v2
'''
