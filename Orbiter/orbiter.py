import numpy as np
import math

from SimPyLC import *



class orbiter (Module):
    def __init__ (self):
        Module.__init__ (self)
        self.positiRaketeX = Register()
        self.positieRaketY = Register()
        self.snelheidRaketVX = Register()
        self.snelheidRaketVY = Register()
        self.versnellingRaketAX = Register()
        self.versnellingRaketAY = Register()
        self.orientatieRaket = Register() #hoek naar mikput
        self.stuwkrachtRaket = Register() #op hoeveel vermogen raket staat 0/100
        self.mikpuntRaket = Register() # naar welk punt de raket mikt

        #Aarde
        self.positieAardeX = Register()
        self.positieAardeY = Register()
        self.positieMarsX = Register()
        self.positieMarsY = Register()

        self.snelheidMarsVX = Register()
        self.snelheidMarsVY = Register()

        self.simulatietijd = Register()
        self.tijdversneller = Register(1)
        self.raketFase = Register(0) # 4 fases



    def sweep (self):

        #timer
        #32000000 1 cyclus
        self.simulatietijd.set(self.simulatietijd + (world.period * self.tijdversneller))

        #baan van de Aarde
        self.positieAardeX.set(1.5*10**11 * np.cos((2 * np.pi * self.simulatietijd) /( 3.2*10**7)))
        self.positieAardeY.set(1.5*10**11 * np.sin((2* np.pi * self.simulatietijd)/(3.2*10**7)))

        #baan van mars
        self.positieMarsX.set((1.5*10**11)*1.5 * np.cos((2 * np.pi * self.simulatietijd) /((3.2*10**7)*1.9)))
        self.positieMarsY.set((1.5*10**11)*1.5 * np.sin( (2*np.pi *self.simulatietijd)/((3.2*10**7)*1.9))  )


        #versnelling berekenen
        self.versnellingRaketAX.set(((self.stuwkrachtRaket * 10000)/10000))#laatste is massa raket

        #controller berekenen vermogen raket en orientatie

        #fase 0 standby op de aarde staan wachten
        self.positiRaketeX.set((6.4*10**6) +1.5*10**11 * np.cos((2 * np.pi * self.simulatietijd) /( 3.2*10**7)), self.raketFase == 0)
        self.positieRaketY.set((465*self.simulatietijd)+1.5*10**11 * np.sin((2* np.pi * self.simulatietijd)/(3.2*10**7)),self.raketFase == 0)
        self.orientatieRaket.set(0, self.raketFase ==0)

        #fase 1 versnellingsfase
        self.stuwkrachtRaket.set(100, self.raketFase ==1)
        self.mikpuntRaket.set(self.positieMarsY + 3.6 *10**6, self.raketFase ==1)
        self.orientatieRaket.set()
        #probleem met het bepalen van de hoek van de orbiter
        #fase2 de afremmingsfase

        #fase3 orbit insertion fase

        #fase4 baan om mars
