"""
Hypo_kalkulacka - kalkulacka vysky hypoteky a hypotekarnej splatky
Vypocita maximalnu moznu vysku hypotekarneho uveru na zaklade prijmu ziadatelov, ich zavazkov, poctu nezaopatrenych deti, na zaklade uroku aky vedia ziskat v banke a na zaklade doby splatnosti. Program vracia vysku hypoteky a mesacnej splatky.
Autor: Marcel Ruzicka, ruzicka_marcel@yahoo.com
"""

from numpy_financial import pmt

class Ziadatel:
  zivotne_minimum_ziadatela = 210.20
  zivotne_minimum_spoluziadatela = 146.64
  zivotne_minimum_na_dieta = 95.96
  povinna_rezerva = 40
  
  def __init__(self, prijem, prijem_spoluziadatela=None, splatky=0, zostatok_uverov=0, pocet_deti=None):
    self.celkovy_prijem = prijem
    self.spoluziadatel = False
    self.prijem_spoluziadatela = prijem_spoluziadatela
    self.splatky = splatky
    self.zostatok_uverov = zostatok_uverov
    self.pocet_deti = pocet_deti
    if prijem_spoluziadatela > 0:
      self.spoluziadatel = True
      self.celkovy_prijem = prijem + prijem_spoluziadatela
      
  def __repr__(self):
    if self.spoluziadatel == False and self.pocet_deti == None:
      return "Bez spoluziadatela \nPrijem: {} EUR \nExistujuce splatky: {} EUR/m \nZostatok uverov: {} EUR \n".format(self.celkovy_prijem, self.splatky, self.zostatok_uverov)
    elif self.spoluziadatel == True and self.pocet_deti == None:
      return "Spoluziadatel - Ano \nCelkovy prijem: {} EUR \nExistujuce splatky: {} EUR/m \nZostatok uverov: {} EUR \n".format(self.celkovy_prijem, self.splatky, self.zostatok_uverov)
    elif self.spoluziadatel == False and self.pocet_deti != None:
      return "Bez spoluziadatela \nPrijem {} EUR \nPocet nezaopatrenych deti: {} \nExistujuce splatky: {} EUR/m \nZostatok uverov: {} EUR \n".format(self.celkovy_prijem, self.pocet_deti, self.splatky, self.zostatok_uverov)
    else:
      return "Spoluziadatel - Ano \nCelkovy prijem: {} EUR \nPocet nezaopatrenych deti: {} \nExistujuce splatky: {} EUR/m \nZostatok uverov: {} EUR \n".format(self.celkovy_prijem, self.pocet_deti, self.splatky, self.zostatok_uverov)
    
  def zivotne_minimum_spolu(self):
    self.zivotne_minimum = self.zivotne_minimum_ziadatela
    if self.spoluziadatel == True:
      self.zivotne_minimum += self.zivotne_minimum_spoluziadatela
    if self.pocet_deti != None:
      self.zivotne_minimum += (self.pocet_deti * self.zivotne_minimum_na_dieta)
    return self.zivotne_minimum

  def dti(self):
    self.max_vyska_uveru_podla_dti = (self.celkovy_prijem * 12 * 8) - self.zostatok_uverov
    return self.max_vyska_uveru_podla_dti
  
  def dsti(self):
    self.max_splatka = (self.celkovy_prijem - self.zivotne_minimum_spolu()) * (float(100 - self.povinna_rezerva) / 100) - self.splatky
    return self.max_splatka 
    
class Hypoteka:
  def __init__(self, doba_splatnosti_v_rokoch, urokova_sadzba):
    self.doba_splatnosti_v_rokoch = doba_splatnosti_v_rokoch
    self.urokova_sadzba = urokova_sadzba
    self.mozna_vyska_uveru = 10000
    self.vypocet()
    
  def __repr__(self):
    return "Mozna vyska uveru: {} EUR \nUrokova sadzba: {} %\nSplatka: {:6.2f} EUR/m \nSplatnost: {} rokov \n".format(self.mozna_vyska_uveru, self.urokova_sadzba, self.bezna_splatka, self.doba_splatnosti_v_rokoch)
    
  def vypocet(self):
    self.dsti_splatka = ziadatel.dsti()
    self.dti_vyska_uveru = ziadatel.dti()
    self.bezna_splatka = (pmt(((self.urokova_sadzba)/100)/12, 12*self.doba_splatnosti_v_rokoch, self.mozna_vyska_uveru)) * (-1)
    self.zvysena_splatka = (pmt(((self.urokova_sadzba+2)/100)/12, 12*self.doba_splatnosti_v_rokoch, self.mozna_vyska_uveru)) * (-1)
    rozdiel = self.zvysena_splatka - self.dsti_splatka
    if rozdiel < 0:
      rozdiel = rozdiel * (-1)
    while rozdiel > 10:
      self.mozna_vyska_uveru += 1000
      self.bezna_splatka = (pmt(((self.urokova_sadzba)/100)/12, 12*self.doba_splatnosti_v_rokoch, self.mozna_vyska_uveru)) * (-1)
      self.zvysena_splatka = (pmt(((self.urokova_sadzba+2)/100)/12, 12*self.doba_splatnosti_v_rokoch, self.mozna_vyska_uveru)) * (-1)
      rozdiel = self.zvysena_splatka - self.dsti_splatka
      if rozdiel < 0:
        rozdiel = rozdiel * (-1)
      if self.dti_vyska_uveru <= self.mozna_vyska_uveru:
        break   
    return self.mozna_vyska_uveru, self.bezna_splatka
    
# Ziadatel(self, prijem, prijem_spoluziadatela, splatky, zostatok_uverov, pocet_deti)
ziadatel = Ziadatel(1200, 640, 0, 0, 4)
print(ziadatel)

# Hypoteka(self, doba_splatnosti_v_rokoch, urokova_sadzba)
uver = Hypoteka(30, 1.5)
print(uver)





  
