"""
Hypoco - kalkulačka výšky hypotéky a hypotekárnej splátky.
Vypočíta maximálnu možnú výšku hypotekárneho úveru na základe príjmu žiadateľov, ich záväzkov, počtu nezaopatrených detí, na základe úroku aký vedia získať v banke a na základe doby splatnosti. Program vracia výšku hypotéky a mesačnej splátky.
Autor: Marcel Ružička, ruzicka_marcel@yahoo.com
"""

from numpy_financial import pmt


class Ziadatel:

  # Pevne premenne. Stanovuje zakon:

  zivotne_minimum_ziadatela = 210.20
  zivotne_minimum_spoluziadatela = 146.64
  zivotne_minimum_na_dieta = 95.96
  povinna_rezerva = 40
  

  # Vstupy o ziadateloch a zavazkoch:

  def __init__(self):
    self.celkovy_prijem = None
    while not self.celkovy_prijem:
      self.celkovy_prijem = input("\nAký je čistý mesačný príjem žiadateľa? \nPríjem: ")
      if "." not in self.celkovy_prijem and "," not in self.celkovy_prijem:
        try:
          self.celkovy_prijem = round(float(self.celkovy_prijem), 2)
        except ValueError:
          self.celkovy_prijem = None
          print("CHYBA: Zadajte platné číslo!")
      elif self.celkovy_prijem.count(".") == 1:
        try:
          self.celkovy_prijem = round(float(self.celkovy_prijem), 2)
        except ValueError:
          self.celkovy_prijem = None
          print("CHYBA: Zadajte platné číslo!")
      elif self.celkovy_prijem.count(",") == 1:
        try:
          self.celkovy_prijem = self.celkovy_prijem.replace(",", ".")
          self.celkovy_prijem = round(float(self.celkovy_prijem), 2)
        except ValueError:
          self.celkovy_prijem = None
          print("CHYBA: Zadajte platné číslo!")
          
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
          print("CHYBA: Zadajte platné číslo alebo \"0\"!")
      elif self.prijem_spoluziadatela.count(".") == 1:
        try:
          self.prijem_spoluziadatela = round(float(self.prijem_spoluziadatela), 2)
        except ValueError:
          self.prijem_spoluziadatela = None
          print("CHYBA: Zadajte platné číslo alebo \"0\"!")
      elif self.prijem_spoluziadatela.count(",") == 1:
        try:
          self.prijem_spoluziadatela = self.prijem_spoluziadatela.replace(",", ".")
          self.prijem_spoluziadatela = round(float(self.prijem_spoluziadatela), 2)
        except ValueError:
          self.prijem_spoluziadatela = None
          print("CHYBA: Zadajte platné číslo alebo \"0\"!")
    
    self.zostatok_uverov = None
    while not self.zostatok_uverov:
      self.zostatok_uverov = input("\nMá žiadateľ (príp. spolužiadateľ) úver? Ak áno, uveďte zostatok. Inak uveďte \"0\" \nZostatok spolu: ")
      if self.zostatok_uverov == "0":
        self.zostatok_uverov = 0
        break
      elif "." not in self.zostatok_uverov and "," not in self.zostatok_uverov:
        try:
          self.zostatok_uverov = round(float(self.zostatok_uverov), 2)
        except ValueError:
          self.zostatok_uverov = None
          print("CHYBA: Zadajte platné číslo alebo \"0\"!")
      elif self.zostatok_uverov.count(".") == 1:
        try:
          self.zostatok_uverov = round(float(self.zostatok_uverov), 2)
        except ValueError:
          self.zostatok_uverov = None
          print("CHYBA: Zadajte platné číslo alebo \"0\"!")
      elif self.zostatok_uverov.count(",") == 1:
        try:
          self.zostatok_uverov = self.zostatok_uverov.replace(",", ".")
          self.zostatok_uverov = round(float(self.zostatok_uverov), 2)
        except ValueError:
          self.zostatok_uverov = None
          print("CHYBA: Zadajte platné číslo alebo \"0\"!")
    
    if self.zostatok_uverov > 0:
      self.splatky = None
      while not self.splatky:
        self.splatky = input("\nAká je mesačná výška splátok existujúcich úverov? \nVýška splátok: ")
        if "." not in self.splatky and "," not in self.splatky:
          try:
            self.splatky = round(float(self.splatky), 2)
          except ValueError:
            self.splatky = None
            print("CHYBA: Zadajte celkovú sumu mesačných splátok úverov!")
        elif self.splatky.count(".") == 1:
          try:
            self.splatky = round(float(self.splatky), 2)
          except ValueError:
            self.splatky = None
            print("CHYBA: Zadajte celkovú sumu mesačných splátok úverov!")
        elif self.splatky.count(",") == 1:
          try:
            self.splatky = self.splatky.replace(",", ".")
            self.splatky = round(float(self.splatky), 2)
          except ValueError:
            sself.splatky = None
            print("CHYBA: Zadajte celkovú sumu mesačných splátok úverov!")
    else:
      self.splatky = 0
      
    self.pocet_deti = None
    while not self.pocet_deti:
      try:
        self.pocet_deti = int(input("\nPočet nezaopatrených detí: "))
        if self.pocet_deti == 0:
          break
      except ValueError:
        self.pocet_deti = None
        print("CHYBA: Zadajte počet detí alebo \"0\"!")
           
    if self.prijem_spoluziadatela > 0:
      self.spoluziadatel = True
      self.celkovy_prijem += self.prijem_spoluziadatela
      self.celkovy_prijem = round(float(self.celkovy_prijem), 2)
      
  
  # Suhrn o ziadateloch:

  def __repr__(self):
    if self.spoluziadatel == False and self.pocet_deti == None:
      return "\n\nBEZ SPOLUŽIADATEĽA \nPRÍJEM: {} EUR \nEXISTUJÚCE SPLÁTKY: {} EUR/m \nZOSTATOK ÚVEROV: {} EUR \nŽIVOTNÉ MINIMUM: {} EUR/m \n\n".format(self.celkovy_prijem, self.splatky, self.zostatok_uverov, self.zivotne_minimum_spolu())
    elif self.spoluziadatel == True and self.pocet_deti == None:
      return "\n\nSPOLUŽIADATEĽ - Áno \nCELKOVÝ PRÍJEM: {} EUR \nEXISTUJÚCE SPLÁTKY: {} EUR/m \nZOSTATOK ÚVEROV: {} EUR \nŽIVOTNÉ MINIMUM: {} EUR/m \n\n".format(self.celkovy_prijem, self.splatky, self.zostatok_uverov, self.zivotne_minimum_spolu())
    elif self.spoluziadatel == False and self.pocet_deti != None:
      return "\n\nBEZ SPOLUŽIADATEĽA \nPRÍJEM: {} EUR \nPOČET NEZAOPATRENÝCH DETÍ: {} \nEXISTUJÚCE SPLÁTKY: {} EUR/m \nZOSTATOK ÚVEROV: {} EUR \nŽIVOTNÉ MINIMUM: {} EUR/m \n\n".format(self.celkovy_prijem, self.pocet_deti, self.splatky, self.zostatok_uverov, self.zivotne_minimum_spolu())
    else:
      return "\n\nSPOLUŽIADATEĽ - Áno \nCELKOVÝ PRÍJEM: {} EUR \nPOČET NEZAOPATRENÝCH DETÍ: {} \nEXISTUJÚCE SPLÁTKY: {} EUR/m \nZOSTATOK ÚVEROV: {} EUR \nŽIVOTNÉ MINIMUM: {} EUR/m \n\n".format(self.celkovy_prijem, self.pocet_deti, self.splatky, self.zostatok_uverov, self.zivotne_minimum_spolu())
    
  
  # Vypocet zivotneho minima:

  def zivotne_minimum_spolu(self):
    self.zivotne_minimum = self.zivotne_minimum_ziadatela
    if self.spoluziadatel == True:
      self.zivotne_minimum += self.zivotne_minimum_spoluziadatela
    if self.pocet_deti:
      self.zivotne_minimum += (self.pocet_deti * self.zivotne_minimum_na_dieta)
    return round(float(self.zivotne_minimum), 2)

  
  # Vypocet DTI parametra:

  def dti(self):
    self.max_vyska_uveru_podla_dti = (self.celkovy_prijem * 12 * 8) - self.zostatok_uverov
    return round(float(self.max_vyska_uveru_podla_dti), 2)
  
  
  # Vypocet DSTI parametra:

  def dsti(self):
    self.max_splatka = (self.celkovy_prijem - self.zivotne_minimum_spolu()) * (float(100 - self.povinna_rezerva) / 100) - self.splatky
    return round(float(self.max_splatka), 2) 
    
class Hypoteka:

  # Zadanie parametrov pozadovanej hypoteky:

  def __init__(self):
    self.doba_splatnosti_v_rokoch = None
    while not self.doba_splatnosti_v_rokoch:
      self.doba_splatnosti_v_rokoch = input("Akú dobu splatnosti chcete zvoliť? \nPočet rokov: ")
      if "." not in self.doba_splatnosti_v_rokoch and "," not in self.doba_splatnosti_v_rokoch:
        try:
          self.doba_splatnosti_v_rokoch = round(float(self.doba_splatnosti_v_rokoch), 1)
        except ValueError:
          self.doba_splatnosti_v_rokoch = None
          print("CHYBA: Zadajte požadovanú dobu splatnosti!")
      elif self.doba_splatnosti_v_rokoch.count(".") == 1:
        try:
          self.doba_splatnosti_v_rokoch = round(float(self.doba_splatnosti_v_rokoch), 1)
        except ValueError:
          self.doba_splatnosti_v_rokoch = None
          print("CHYBA: Zadajte požadovanú dobu splatnosti!")
      elif self.doba_splatnosti_v_rokoch.count(",") == 1:
        try:
          self.doba_splatnosti_v_rokoch = self.doba_splatnosti_v_rokoch.replace(",", ".")
          self.doba_splatnosti_v_rokoch = round(float(self.doba_splatnosti_v_rokoch), 1)
        except ValueError:
          self.doba_splatnosti_v_rokoch = None
          print("CHYBA: Zadajte požadovanú dobu splatnosti!")
    
    self.urokova_sadzba = None
    while not self.urokova_sadzba:
      self.urokova_sadzba = input("\nAkú úrokovú sadzbu ponúka banka? \nÚrok: ")
      if "." not in self.urokova_sadzba and "," not in self.urokova_sadzba:
        try:
          self.urokova_sadzba = round(float(self.urokova_sadzba), 2)
        except ValueError:
          self.urokova_sadzba = None
          print("CHYBA: Zadajte úrokovú sadzbu!")
      elif self.urokova_sadzba.count(".") == 1:
        try:
          self.urokova_sadzba = round(float(self.urokova_sadzba), 2)
        except ValueError:
          self.urokova_sadzba = None
          print("CHYBA: Zadajte úrokovú sadzbu!")
      elif self.urokova_sadzba.count(",") == 1:
        try:
          self.urokova_sadzba = self.urokova_sadzba.replace(",", ".")
          self.urokova_sadzba = round(float(self.urokova_sadzba), 2)
        except ValueError:
          self.urokova_sadzba = None
          print("CHYBA: Zadajte úrokovú sadzbu!")
    
    
    # Default parameter, od ktoreho zacne prepocet moznej zhodnej ponuky hypoteky:
    self.mozna_vyska_uveru = 10000
    # Vyvolanie vypoctu:
    self.vypocet()
   

  # Vysledok vypoctu:

  def __repr__(self):
    return "\n\nMOŽNÁ VÝŠKA ÚVERU: {} EUR \nÚROKOVÁ SADZBA: {} %\nSPLÁTKA: {:6.2f} EUR/m \nSPLATNOSŤ: {} rokov \n\n".format(self.mozna_vyska_uveru, self.urokova_sadzba, self.bezna_splatka, self.doba_splatnosti_v_rokoch)  


  # Metoda vypoctu:

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
   

  # Metoda pre opakovanie vypoctu:

  def prepocet(self):
    prepocet = input("\nŽeláte si prepočítať hypotéku s iným úrokom alebo s inou dobou splatnosti? \n A (Áno) / N (Nie) \n")
    while prepocet != "A" and prepocet != "a" and prepocet != "N" and prepocet != "n":
      print("\nNeplatný príkaz!")
      prepocet = input("Zadajte \"A\", ak chcete prepočítať hypotekárnu ponuku, alebo \"N\", ak si želáte skončiť.\n ")
    if prepocet == "A" or prepocet == "a":
      uver = Hypoteka()
      print(uver)
      self.prepocet()
    if prepocet == "N" or prepocet == "n":
      print("\nĎakujeme, že používate HYPOCO!\n")
    return
      

ziadatel = Ziadatel()
print(ziadatel)
uver = Hypoteka()
print(uver)
uver.prepocet()
  

  






  
