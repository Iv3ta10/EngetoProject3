# Projekt: Elections Scraper

This project is designed to retrieve election results from a given URL and save those results into a CSV file.

## Installation

- Create a new virtual environment:  
  `python3 -m venv moje_virtualni_prostredi`
- Activate it:  
  `source moje_virtualni_prostredi/bin/activate`  
  – activation for Linux and macOS  
  `moje_virtualni_prostredi\Scripts\Activate.ps1`  
  – activation for Windows
- Install the required libraries:  
  `pip3 install -r requirements.txt`
- Run the script using two arguments:

1. The URL of the administrative area (the link you want to scrape)
2. The name of the output file (must have a .csv extension)

### Example of running the project:

`python3 main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100" results.csv`
