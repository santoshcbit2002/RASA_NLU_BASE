from bs4 import BeautifulSoup
import requests
import pprint

def scrapper_func(filename):
    r  = requests.get("https://en.wikipedia.org/wiki/Classification_of_Indian_cities")
    soup = BeautifulSoup(r.text,'html.parser')
    tag=soup.find_all('td')
    tag1=tag[0].text
    tag2=tag[1].text
    tag3=tag[2].text
    tag4=tag[3].text
    cities=[i.replace('\n','').lower().strip() for i in tag4.split(',')+tag2.split(',')]
    with open(filename, mode="w") as outfile: 
        for i in cities:
            outfile.write("%s\n" % i)
    print('***  Look up for City Loaded ***')