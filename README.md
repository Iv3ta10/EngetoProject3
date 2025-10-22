# Projekt: Elections Scraper

Tento projekt je vytvořen k získávání výsledků voleb ze zadaného odkazu. Tyto výsledky ukládá do souboru CSV.

## Instalace

- Vytvoř si nové virtuální prostředí  
  `python3 -m venv moje_virtualni_prostredi`
- Aktivuj jej  
  `source moje_virtualni_prostredi/bin/activate` - aktivace pro Linux a MacOS  
  `moje_virtualni_prostredi\Scripts\Activate.ps1` - aktivace pro Windows
- Nainstaluj potřebné knihovny:  
  `pip3 install -r requirements.txt`
- Spusť soubor za pomoci dvou argumentů:

1. URL adresa územního celku (odkaz, který chceš scrapovat)
2. Název výstupního souboru (soubor musí mít příponu .csv)

př. spuštění projektu:
`python3 main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100" results.csv`
