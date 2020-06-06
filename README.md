# hypoco
Kalkulačka, ktorá vypočíta maximálnu možnú výšku hypotekárneho úveru a jeho mesačnú splátku.

class Ziadatel berie vstupy: 
 - príjem
 - príjem spolužiadateľa (ak má, inak None)
 - splátky (existujúce splátky, ak má úver, inak 0)
 - zostatok úverov (ak má úver, inak 0)
 - počet nezaopatrených detí (ak má, inak None)
 
 Vstupy sú dané v poradí, ako je uvedené vyššie. Ak žiadateľ má iba príjem, môže ostatné vstupy vynechať. Podobne, ak má príjem žiadateľ a spolužiadateľ, môže vynechať ostatné vstupy. Ak potrebuje zadať niektorý ďalší paramater, ale parameter medzi tým nejestvuje, musí uviesť None alebo 0, ako je uvedené vyššie.
 
 class Hypoteka berie vstupy:
  - doba splatnosti v rokoch
  - úroková sadzba
  
 Kalkulačka vráti základné údaje o klientovi, maximálnu možnú výšku hypotekárneho úveru (podľa bankových štandardov, na základe porovnania DTI a DSTI) a jeho splátku.
