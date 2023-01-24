from bs4 import BeautifulSoup
from selenium import webdriver

def extract_data():
    
    driver_options = webdriver.ChromeOptions()
    driver_options.headless = False
    driver = webdriver.Chrome(options=driver_options)

    driver.get('https://www.sport-histoire.fr/es/Geografia/Lista_monedas_de_los_paises.php')
    soup = BeautifulSoup(driver.page_source, 'lxml')
    
    country_counter = 0
    
    table = soup.find('tbody')
    
    with open('../../datasets/raw/countries.csv', 'w') as f:
        
        f.write("country;currency_name;currency_code\n")
    
        for row in table.find_all('tr'):
            
            try:
                country = row.find('a').get_text().strip()
                currency_name = row.find_all('td')[1].get_text().strip()
                currency_code = row.find_all('td')[2].get_text().strip()
            
                f.write("%s;%s;%s\n" % (country, currency_name, currency_code))
                country_counter += 1
            
            except Exception:
                continue

    print("Se han extraido %d paises" % country_counter)

if __name__ == '__main__':
    extract_data()