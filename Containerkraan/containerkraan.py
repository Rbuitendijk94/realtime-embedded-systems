from SimPyLC import *

class containerkraan (Module):
    def __init__ (self):
        Module.__init__ (self)

        #kraan
        self.motorKraan = Marker()
        self.richtingKraan = Marker() # true is +
        self.kraanPositie = Register(4) # X positie max 10
        self.oppakkenContainer= Marker(True)

        #loopkat
        self.motorLoopkat = Marker()
        self.richtingLoopkat = Marker()
        self.loopkatPositie = Register() # Y Posistie max 5
        self.klauwenOpen = Marker()

        #spreader
        self.motorSpreader = Marker()
        self.richtingSpreader = Marker()
        self.gewichtAanwezig = Marker()
        self.spreaderPositie = Register(5) # Z poositie

        self.knopGo= Marker()
        self.knopNood = Marker()
        self.oppakXcoordinaat = Register(8)
        self.oppakYcoordinaat = Register()
        self.oppakZcoordinaat = Register(2)
        self.gewenstXcoordinaat= Register(2)
        self.gewenstYcoordinaat= Register()
        self.gewenstZcoordinaat = Register()

    def sweep (self):
        #noodknop stop alles
        self.motorKraan.mark(False, self.knopNood)
        self.motorLoopkat.mark(False, self.knopNood)
        self.motorSpreader.mark(False, self.knopNood)

        #limiten beschrijven
        self.spreaderPositie.set(1, self.spreaderPositie <1)
        self.spreaderPositie.set(5, self.spreaderPositie >5)
        self.kraanPositie.set(10, self.kraanPositie > 10)
        self.kraanPositie.set(0, self.kraanPositie <0)
        self.loopkatPositie.set(5,self.loopkatPositie>5)
        self.loopkatPositie.set(0, self.loopkatPositie<0)
        self.spreaderPositie.set(1 ,self.spreaderPositie <1)

        #overige logica
        self.motorSpreader.mark(False, self.motorKraan or self.motorLoopkat)
        self.klauwenOpen.mark(False, self.gewichtAanwezig and self.spreaderPositie != self.gewenstZcoordinaat)

##---------------------------------------------------- oppakken
        #Kraan naar container
        self.motorKraan.mark(True, self.knopGo and self.kraanPositie != self.oppakXcoordinaat and self.spreaderPositie ==5, False)
        self.richtingKraan.mark(True, self.kraanPositie < self.oppakXcoordinaat)
        self.richtingKraan.mark(False, self.kraanPositie > self.oppakXcoordinaat)
        self.kraanPositie.set(self.kraanPositie +0.25 , self.motorKraan and self.richtingKraan,  self.kraanPositie)
        self.kraanPositie.set(self.kraanPositie -0.25 , self.motorKraan and self.richtingKraan == False, self.kraanPositie)

        #loopkat oppakken container
        self.motorLoopkat.mark(True, self.knopGo and self.loopkatPositie != self.oppakYcoordinaat)
        self.richtingLoopkat.mark(True, self.loopkatPositie < self.oppakYcoordinaat)
        self.richtingLoopkat.mark(False, self.loopkatPositie > self.oppakYcoordinaat)
        self.loopkatPositie.set(self.loopkatPositie +0.25 , self.motorLoopkat and self.richtingLoopkat,  self.loopkatPositie)
        self.loopkatPositie.set(self.loopkatPositie -0.25 , self.motorLoopkat and self.richtingLoopkat == False, self.loopkatPositie)




        #open de klauw

        self.motorSpreader.mark(True, self.knopGo and self.spreaderPositie != self.oppakZcoordinaat and self.oppakXcoordinaat == self.kraanPositie and self.oppakYcoordinaat == self.loopkatPositie)
        self.motorSpreader.mark(False, self.spreaderPositie == self.oppakZcoordinaat and self.gewichtAanwezig == False)
        self.motorSpreader.mark(False ,self.oppakkenContainer== False and self.gewichtAanwezig)
        self.spreaderPositie.set(self.spreaderPositie -0.25 , self.motorSpreader and self.richtingSpreader == False and self.gewichtAanwezig == False,  self.spreaderPositie)
        self.klauwenOpen.mark(True,self.gewichtAanwezig == False and self.spreaderPositie != self.oppakZcoordinaat )
        self.richtingSpreader.mark(False,self.spreaderPositie > self.oppakZcoordinaat )
        self.richtingSpreader.mark(True,self.spreaderPositie < self.oppakZcoordinaat or (self.gewichtAanwezig == True  and self.oppakkenContainer))
        self.klauwenOpen.mark(False,self.knopGo and self.spreaderPositie == self.oppakZcoordinaat and self.oppakXcoordinaat ==  self.kraanPositie and self.loopkatPositie == self.oppakYcoordinaat)
        self.gewichtAanwezig.mark(True, self.spreaderPositie == self.oppakZcoordinaat and self.oppakXcoordinaat ==  self.kraanPositie and self.loopkatPositie == self.oppakYcoordinaat and self.klauwenOpen == False)
        self.spreaderPositie.set(self.spreaderPositie +0.25 , self.motorSpreader and self.richtingSpreader and self.gewichtAanwezig,  self.spreaderPositie)
        self.oppakkenContainer.mark(False, self.spreaderPositie == 5, self.gewichtAanwezig)
'''
        self.klauwenOpen.mark(False,self.spreaderPositie == self.oppakZcoordinaat)
        self.gewichtAanwezig.mark(True, self.spreaderPositie == self.oppakZcoordinaat and self.klauwenOpen)
        self.spreaderPositie.set(self.spreaderPositie -0.25 , self.motorSpreader and self.richtingSpreader == False and self.klauwenOpen == False, self.spreaderPositie)




#-----------------------------------------------------------brengen naar nieuwe locatiee

        #kraan naar bestemming brengen
       #self.motorKraan.mark(True, self.knopGo and (self.kraanPositie *0.99 > self.gewenstXcoordinaat or self.kraanPositie *1.01 < self.gewenstXcoordinaat ),False)
        self.motorKraan.mark(True, self.knopGo and self.kraanPositie != self.gewenstXcoordinaat and self.spreaderPositie ==5, False)
        self.richtingKraan.mark(True, self.kraanPositie < self.gewenstXcoordinaat)
        self.richtingKraan.mark(False, self.kraanPositie > self.gewenstXcoordinaat)
        self.kraanPositie.set(self.kraanPositie +0.25 , self.motorKraan and self.richtingKraan,  self.kraanPositie)
        self.kraanPositie.set(self.kraanPositie -0.25 , self.motorKraan and self.richtingKraan == False, self.kraanPositie)

        #loopkat naar bestemming
        self.motorLoopkat.mark(True, self.knopGo and self.loopkatPositie != self.gewenstYcoordinaat)
        self.richtingLoopkat.mark(True, self.loopkatPositie < self.gewenstYcoordinaat)
        self.richtingLoopkat.mark(False, self.loopkatPositie > self.gewenstYcoordinaat)
        self.loopkatPositie.set(self.loopkatPositie +0.25 , self.motorLoopkat and self.richtingLoopkat,  self.loopkatPositie)
        self.loopkatPositie.set(self.loopkatPositie -0.25 , self.motorLoopkat and self.richtingLoopkat == False, self.loopkatPositie)


        #overige logica
        self.knopGo.mark(False, self.kraanPositie == self.gewenstXcoordinaat and self.loopkatPositie == self.gewenstYcoordinaat and self.spreaderPositie == self.gewenstZcoordinaat)






        •----- Fysica van hijskraan: er is een marker die aangeeft of er een last aan het mechanisme hangt. Als de last zakt en op de grond of een andere container komt te staan, wordt deze marker False.
        • De motoren voor de wielen, de loopkat en het hijsmechanisme kunnen aan- en uitgeschakeld worden en van draairichting veranderd. Hierdoor beweegt de kraan.
        • De gebruiker kan de co¨ordinaten van een op te pakken container (zoveelste in voor/achterrichting, zoveelste in links/rechtsrichting, zoveelste stapellaag) en die van een bestemming opgeven, en vervolgens op de “go”-knop drukken. De kraan beweegt dan zelf naar de opgegeven plek, pakt de container op, brengt deze naar de bestemming en laat hem weer zakken.

        '''
