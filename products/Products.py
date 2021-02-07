import requests
import re
import csv
from bs4 import BeautifulSoup
from lxml import etree



domain = 'https://webscraper.io'
temps = []

class Crawler:
    def getPage(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def absoluteUrl(self,url):
        absoluteUrl = domain + url
        return absoluteUrl


    def search(self, site):
        bs = self.getPage(site)
        xpathSelector = etree.HTML(str(bs))
        searchResults = xpathSelector.xpath("//a[@class='title']/@href")
        for site in searchResults:
            url = self.absoluteUrl(site)
            self.contains(url)
            
    def contains(self, url):
        bs = self.getPage(url)
        xpathSelector = etree.HTML(str(bs))
        title = xpathSelector.xpath("(//div[@class='caption']/h4)[2]/text()")
        price = xpathSelector.xpath("(//div[@class='caption']/h4)[1]/text()")
        description = xpathSelector.xpath("//p[@class='description']/text()")
        Product_Title = ''
        Product_Price = ''
        Product_Description = ''

        Product_Title = Product_Title.join(title)
        Product_Price = Product_Price.join(price)
        Product_Description = Product_Description.join(description)
        
       
        products = []

        products.append(Product_Title)
        products.append(Product_Price)
        products.append(Product_Description)
        products.append(url)
        
        temps.append(products)
        
        print ("Product Title :",title)
        print ("Product Price :",price)
        print ("Product Description :",description)
        print ("Product Url :",url)

        



        
class pages (Crawler):
    
    def contain(self,targetUrl):
        super().search(targetUrl)

        bs = super().getPage(targetUrl)

        xpathSelector = etree.HTML(str(bs))
        Url_xpath = xpathSelector.xpath("//a[@rel='next']/@href")
        stringUrl = ''
        stringUrl = stringUrl.join(Url_xpath)

        if (len(stringUrl)!=0):
            Url = domain + stringUrl
            return Url
        else:
            return 0
        

Target_website = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops?page=1"
crawler = pages()
while(True):
    Target_website = crawler.contain(Target_website)
    print(Target_website)
    if Target_website == 0:
        break

with open('dataset.csv', 'a') as csvFile:
    seen = list()

    writer = csv.DictWriter(csvFile, fieldnames = ["Product Title", "Product  Price", "Product Description", "Product Url"])
    writer.writeheader()
    writer = csv.writer(csvFile, delimiter =',')
    for item in temps:
        if item in seen:
            continue
        seen.append(item)
        writer.writerow(item)
        
            
    