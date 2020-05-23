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
  
  def __init__(self):
    self.celkovy_prijem = None
    while not self.celkovy_prijem:
      self.celkovy_prijem = input("\nAký je čistý mesačný príjem žiadateľa? \nPríjem: ")
      if "." not in self.celkovy_prijem and "," not in self.celkovy_prijem:
        try:
          self.celkovy_prijem = round(float(self.celkovy_prijem), 2)
        except ValueError:
          self.celkovy_prijem = None
          print("Zadajte platné číslo")
      elif self.celkovy_prijem.count(".") == 1:
        try:
          self.celkovy_prijem = round(float(self.celkovy_prijem), 2)
        except ValueError:
          self.celkovy_prijem = None
          print("Zadajte platné číslo")
      elif self.celkovy_prijem.count(",") == 1:
        try:
          self.celkovy_prijem = self.celkovy_prijem.replace(",", ".")
          self.celkovy_prijem = round(float(self.celkovy_prijem), 2)
        except ValueError:
          self.celkovy_prijem = None
          print("Zadajte platné číslo")
          
    self.spoluziadatel = False
    
    self.prijem_spoluziadatela = None
    while not self.prijem_spoluziadatela:
      self.prijem_spoluziadatela = input("\nAk má žiadateľ spolužiadateľa, zadajte výšku jeho čistého mesačného príjmu. Ak nie, zadajte \"0\". \nPríjem spolužiadateľa: ")
      if self.prijem_spoluziadatela == "0":
        self.prijem_spoluziadatela = 0
        break
      elif "." not in self.prijem_spoluziadatela and "," not in self.prijem_spoluziadatela:
        try:
          self.prijem_spoluziadatela = round(float(self.prijem_spoluziadatela), 2)
        except ValueError:
          self.prijem_spoluziadatela = None
          print("Zadajte platné číslo alebo 0")
      elif self.prijem_spoluziadatela.count(".") == 1:
        try:
          self.prijem_spoluziadatela = round(float(self.prijem_spoluziadatela), 2)
        except ValueError:
          self.prijem_spoluziadatela = None
          print("Zadajte platné číslo alebo 0")
      elif self.prijem_spoluziadatela.count(",") == 1:
        try:
          self.prijem_spoluziadatela = self.prijem_spoluziadatela.replace(",", ".")
          self.prijem_spoluziadatela = round(float(self.prijem_spoluziadatela), 2)
        except ValueError:
          self.prijem_spoluziadatela = None
          print("Zadajte platné číslo alebo 0")
    
    self.zostatok_uverov = input("\nMá žiadateľ (príp. spolužiadateľ) úver? Ak áno, uveďte zostatok. Inak uveďte \"0\" \nZostatok spolu: ")
    if "," in self.zostatok_uverov:
      self.zostatok_uverov = self.zostatok_uverov.replace(",", ".")
      self.zostatok_uverov = round(float(self.zostatok_uverov), 2)
    else:
      self.zostatok_uverov = round(float(self.zostatok_uverov), 2)
    
    if self.zostatok_uverov > 0:
      self.splatky = input("\nAká je mesačná výška splátok existujúcich úverov? \nVýška splátok: ")
      if "," in self.splatky:
        self.splatky = self.splatky.replace(",", ".")
        self.splatky = round(float(self.splatky), 2)
      else:
        self.splatky = round(float(self.splatky), 2)
    else:
      self.splatky = 0
      
    self.pocet_deti = int(input("\nPočet nezaopatrených detí: "))
    
    if self.prijem_spoluziadatela > 0:
      self.spoluziadatel = True
      self.celkovy_prijem += self.prijem_spoluziadatela
      self.celkovy_prijem = round(float(self.celkovy_prijem), 2)
      
  def __repr__(self):
    if self.spoluziadatel == False and self.pocet_deti == None:
      return "\n\nBez spolužiadateľa \nPríjem: {} EUR \nExistujúce splátky: {} EUR/m \nZostatok úverov: {} EUR \n\n".format(self.celkovy_prijem, self.splatky, self.zostatok_uverov)
    elif self.spoluziadatel == True and self.pocet_deti == None:
      return "\n\nSpolužiadateľ - Áno \nCelkový príjem: {} EUR \nExistujúce splátky: {} EUR/m \nZostatok úverov: {} EUR \n\n".format(self.celkovy_prijem, self.splatky, self.zostatok_uverov)
    elif self.spoluziadatel == False and self.pocet_deti != None:
      return "\n\nBez spolužiadateľa \nPríjem {} EUR \nPočet nezaopatrených detí: {} \nExistujúce splátky: {} EUR/m \nZostatok úverov: {} EUR \n\n".format(self.celkovy_prijem, self.pocet_deti, self.splatky, self.zostatok_uverov)
    else:
      return "\n\nSpolužiadateľ - Áno \nCelkový príjem: {} EUR \nPočet nezaopatrených detí: {} \nExistujúce splátky: {} EUR/m \nZostatok úverov: {} EUR \n\n".format(self.celkovy_prijem, self.pocet_deti, self.splatky, self.zostatok_uverov)
    
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
  def __init__(self):
    self.doba_splatnosti_v_rokoch = input("Akú dobu splatnosti chcete zvoliť? \nPočet rokov: ")
    if "," in self.doba_splatnosti_v_rokoch:
      self.doba_splatnosti_v_rokoch = self.doba_splatnosti_v_rokoch.replace(",", ".")
      self.doba_splatnosti_v_rokoch = round(float(self.doba_splatnosti_v_rokoch), 1)
    else:
      self.doba_splatnosti_v_rokoch = round(float(self.doba_splatnosti_v_rokoch), 1)
    
    self.urokova_sadzba = input("\nAkú úrokovú sadzbu ponúka banka? \nÚrok: ")
    if "," in self.urokova_sadzba:
      self.urokova_sadzba = self.urokova_sadzba.replace(",", ".")
      self.urokova_sadzba = round(float(self.urokova_sadzba), 2)
    else:
      self.urokova_sadzba = round(float(self.urokova_sadzba), 2)
    
    self.mozna_vyska_uveru = 10000
    self.vypocet()
    
  def __repr__(self):
    return "\n\nMožná výška úveru: {} EUR \nÚroková sadzba: {} %\nSplátka: {:6.2f} EUR/m \nSplatnosť: {} rokov \n\n".format(self.mozna_vyska_uveru, self.urokova_sadzba, self.bezna_splatka, self.doba_splatnosti_v_rokoch)
    
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
    
  def prepocet(self):
    prepocet = input("\nŽeláte si prepočítať hypotéku s iným úrokom alebo s inou dobou splatnosti? \n A (Áno) ")
    while prepocet != "A" and prepocet != "a":
      print("\nNeplatný príkaz.")
      prepocet = input("Zadajte \"A\", ak chcete prepočítať hypotekárnu ponuku.\n ")
    if prepocet == "A" or prepocet == "a":
      uver = Hypoteka()
      print(uver)
      self.prepocet()
      

ziadatel = Ziadatel()
print(ziadatel)
uver = Hypoteka()
print(uver)
uver.prepocet()
  
if __name__ == "__main__":
  main()
  






  
