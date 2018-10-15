from SimPyLC import *

class containerkraan (Module):
    def __init__ (self):
        Module.__init__ (self)

        #kraan
        self.motorKraan = Marker()
        self.richtingKraan = Marker() # true is +
        self.kraanPositie = Register(4) # X positie max 10


        #loopkat
        self.motorLoopkat = Marker()
        self.richtingLoopkat = Marker()
        self.loopkatPositie = Register() # Y Posistie max 5
        self.klauwenOpen = Marker()

        #spreader
        self.motorHijsmeganisme = Marker()
        self.richintHijsmeganisme = Marker()
        self.gewichtAanwezig = Marker()
        self.spreaderPositie = Register() # Z poositie

        self.knopGo= Marker()
        self.knopNood = Marker()
        self.gewenstXcoordinaat= Register(2)
        self.gewenstYcoordinaat= Register()
        self.gewenstZcoordinaat = Register()

    def sweep (self):
        #noodknop stop alles
        self.motorKraan.mark(False, self.knopNood)
        self.motorLoopkat.mark(False, self.knopNood)
        self.motorHijsmeganisme.mark(False, self.knopNood)

        #limiten beschrijven
        self.spreaderPositie.set(1, self.spreaderPositie <1)
        self.spreaderPositie.set(5, self.spreaderPositie >5)
        self.kraanPositie.set(10, self.kraanPositie > 10)
        self.kraanPositie.set(0, self.kraanPositie <0)
        self.loopkatPositie.set(5,self.loopkatPositie>5)
        self.loopkatPositie.set(0, self.loopkatPositie<0)

        #kraan naar bestemming brengen
       #self.motorKraan.mark(True, self.knopGo and (self.kraanPositie *0.99 > self.gewenstXcoordinaat or self.kraanPositie *1.01 < self.gewenstXcoordinaat ),False)
        self.motorKraan.mark(True, self.knopGo and self.kraanPositie != self.gewenstXcoordinaat, False)
        self.richtingKraan.mark(True, self.kraanPositie < self.gewenstXcoordinaat)
        self.richtingKraan.mark(False, self.kraanPositie > self.gewenstXcoordinaat)
        self.kraanPositie.set(self.kraanPositie +0.25 , self.motorKraan and self.richtingKraan,  self.kraanPositie)
        self.kraanPositie.set(self.kraanPositie -0.25 , self.motorKraan and self.richtingKraan == False, self.kraanPositie)


        self.motorLoopkat.mark(True, self.knopGo and self.loopkatPositie != self.gewenstYcoordinaat)




        self.knopGo.mark(False, self.kraanPositie == self.gewenstXcoordinaat and self.loopkatPositie == self.gewenstYcoordinaat and self.spreaderPositie == self.gewenstZcoordinaat)



















        
        '''
        •----- Fysica van hijskraan: er is een marker die aangeeft of er een last aan het mechanisme hangt. Als de last zakt en op de grond of een andere container komt te staan, wordt deze marker False.
        • De motoren voor de wielen, de loopkat en het hijsmechanisme kunnen aan- en uitgeschakeld worden en van draairichting veranderd. Hierdoor beweegt de kraan.
        • De gebruiker kan de co¨ordinaten van een op te pakken container (zoveelste in voor/achterrichting, zoveelste in links/rechtsrichting, zoveelste stapellaag) en die van een bestemming opgeven, en vervolgens op de “go”-knop drukken. De kraan beweegt dan zelf naar de opgegeven plek, pakt de container op, brengt deze naar de bestemming en laat hem weer zakken.
        • De kraan kan niet bewegen als de spreader niet minstens op niveau 5 hangt.
        • De klauwen kunnen niet geopend worden als er een last aan de kraan hangt.
        • De spreader kan niet omlaag als de kraan beweegt.
         • -------De kraan kan niet verder rijden dan het eind van de rails.
         • -------De loopkat kan niet verder rijden dan het eind van de balk.
        • -----------De spreader kan niet hoger dan niveau 5, en niet lager dan niveau 1.
        • Als de kraan in zowel de voor/achterrichting als in de links/rechtsrichting moet bewegen, gebeurt dit tegelijkertijd.
        •---------- Als de noodstop wordt ingedrukt, stopt het systeem.
        '''
