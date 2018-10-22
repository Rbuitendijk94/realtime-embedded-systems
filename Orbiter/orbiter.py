import numpy as np
import math

from SimPyLC import *



class orbiter (Module):
    def __init__ (self):
        Module.__init__ (self)
        self.positieX = Register()
        self.positieY = Register()
        self.snelheidVX = Register()
        self.snelheidVY = Register()
        self.versnellingAX = Register()
        self.versnellingAY = Register()
        self.orientatie = Register()

        #Aarde
        self.positieAardeX = Register()
        self.positieAardeY = Register()
        self.positieMarsX = Register()
        self.positieMarsY = Register()

        self.snelheidMarsVX = Register()
        self.snelheidMarsVY = Register()

        self.simulatietijd = Register()
        self.tijdversneller = Register(1)
        self.raketFase = Register(1) # 4 fases



    def sweep (self):

        #timer
        #32000000 1 seconde
        self.simulatietijd.set(self.simulatietijd + (world.period * self.tijdversneller))

        #baan van de Aarde
        self.positieAardeX.set(1.5*10**11 * np.cos((2 * np.pi * self.simulatietijd) /( 3.2*10**7)))
        self.positieAardeY.set(1.5*10**11 * np.sin((2* np.pi * self.simulatietijd)/(3.2*10**7)))

        #baan van mars



        #versnelling berekenen

        #controller

        #fase 1 versnellingsfase

        #fase2 de afremmingsfase

        #fase3 orbit insertion fase

        #fase4 baan om mars
