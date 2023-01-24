import pandas as pd
import json
import os

def create_cleaned_dataset():
    
    print("Merging datasets...")
  
    countries_currency = pd.read_csv('../datasets/raw/countries-currency.csv', sep=';')
    countries_iso = pd.read_csv('../datasets/raw/countries-iso.csv', sep=',')
    currencies = dict()
    
    with open("../datasets/raw/currencies.json", "r") as json_file:
        currencies = json.load(json_file)
        
    try:
        currencies = currencies['data']['currencies']['results']
    except Exception:
        raise RuntimeError("The currencies json does not have the expected structure")
    
    if len(currencies) == 0: raise RuntimeError("The currencies dataset is empty")
    
    if not os.path.exists('../datasets/clean/cleaned-countries.csv'):
        
        merge_datasets(countries_currency, countries_iso, currencies)
                    
        print("The dataset has been filtered and cleaned. You can find it in the folder: `datasets/clean/`")
    else:
        print("There is alredy a cleaned dataset in the folder: `datasets/clean/`. If you want to merge DS again, delete the existing file and rerun the script.")

def merge_datasets(countries_currency, countries_iso, currencies):
    
    with open('../datasets/clean/cleaned-countries.csv', 'w') as f:
            
        f.write("spanish_name;english_name;iso3;phone_code;currency_name;currency_code;currency_symbol\n")
        
        for index, country in countries_iso.iterrows():
            
            spanish_name = country['nombre'].strip()
            english_name = country['name'].strip()
            iso3 = country['iso3'].strip()
            try:
                phone_code = country['phone_code'].strip()
            except Exception:
                phone_code = None
            
            country_currency_entry = countries_currency.loc[countries_currency['country'] == spanish_name]
            
            if not country_currency_entry.empty:
                country_currency_entry = country_currency_entry.iloc[0]
                currency_name = country_currency_entry['currency_name'].strip()
                currency_code = country_currency_entry['currency_code'].strip()
                currency_symbol = None
                
                for currency in currencies:
                    if currency['code'] == currency_code:
                        currency_symbol = currency['symbol']
                        break
            
            else:
                currency_name = None
                currency_code = None
                currency_symbol = None
                
            
            f.write(f"{spanish_name};{english_name};{iso3};{phone_code};{currency_name};{currency_code};{currency_symbol}\n")

if __name__ == '__main__':
    create_cleaned_dataset()