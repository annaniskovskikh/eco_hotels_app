# -*- coding: utf-8 -*-

import sys
from selenium import webdriver
import time
import csv

def list_cities_traduction(fic):
    """
    This function reads an input file with cities
    and returns a dictionary :
    key -- city; value -- translation.
    @param fic -- input file
    @return cities -- dictionary
    """
    cities = {}
    with open(fic, 'r') as fic:
        for line in fic:    
            city_trad = line.split('\t')
            city = city_trad[0].lower()
            trad = city_trad[1].strip('\n')
            cities[city] = trad

    return cities


def check_status_eco_hotel(driver, city, trad):
    """
    This function gets hotels titles and information
    about services - if eco-friendly exists,
    so it prints a hotel name as a key and 'YES' as value,
    otherwise it prints a hotel name as a key with 'no' as value.
    @param driver -- a driver created
    @param city -- a city to examine 
    @param trad -- a translation of a city
    @return dico_hotels -- dictionary of a hotel title + its eco status
    """
    url = f"https://www.nh-hotels.fr/booking/hotels/{city}?fini=24/08/2021&fout=30/08/2021&nadults1=2&nchilds1=0&nbabies1=0&destinationId={trad}"
    driver.get(url)
    link_hotels = driver.find_elements_by_class_name("js-hotel-title")
    href_hotels = [href_hotel.get_attribute('href') for href_hotel in link_hotels]

    dico_hotels = {}
    for href_hotel in href_hotels:
        driver.get(href_hotel)

        name_hotel = driver.find_element_by_xpath('//h2[@class="h3"]').text
        services = driver.find_elements_by_class_name("color-primary")
        services_text = [service.text for service in services]

        status_eco = ''
        if "Eco-friendly" in services_text:
            status_eco = "YES"
        else:
            status_eco = "no"
        dico_hotels[name_hotel] = status_eco
                
    return dico_hotels


def write_csv_file(dico):
    """
    This function creates an output file with cities,
    hotels titles and eco status, nothing is returned.
    @param dico -- dictionary with information on hotels
    (city, name, eco status)
    """
    with open("statistics_eco_friendly_hotels.csv", "w") as fic:
        fic_writer = csv.writer(fic, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        fic_writer.writerow(['City', 'Hotel title', 'Status ECO'])
        for city, items in dico.items():
            try:
                for hotel in items:
                    fic_writer.writerow([city, hotel, items[hotel]])
            except:
                fic_writer.writerow([city, None, None])


def main():
    input_fic = sys.argv[1]
    dico_cities = list_cities_traduction(input_fic)

    # create instance of webdriver
    driver = '/home/anna/Documents/M2/TechWeb/geckodriver'
    driver = webdriver.Firefox(executable_path=driver)

    dico_all_hotels = {}
    for city, trad in dico_cities.items():
        dico_hotels = check_status_eco_hotel(driver, city, trad)
        dico_all_hotels[city.capitalize()] = dico_hotels

    write_csv_file(dico_all_hotels)

if __name__ == "__main__":
    main()