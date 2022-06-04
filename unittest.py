url = 'https://us.shein.com/'
def get_product(url):
    'This is the function used to extract product details of desired products.'
    import requests
    from datetime import date 
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.webdriver import Chrome
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By

    response = requests.get(url)

    # Make sure we get the homepage
    if response.status_code == 200:
        print("Success")
    else:
        print("Failure")

    # Here we get a soup object of SHEIN homepage
    results_page = BeautifulSoup(response.content,'lxml')

    # I will only extract dress products for the purpose of this data challenge only.
    dress_url = results_page.find("a",{"title":"DRESSES"})['href'] # a link to dress category

    # Repeat and get a soup object for dress category
    new_response = requests.get(dress_url)
    if new_response.status_code == 200:
        print("Success")
    else:
        print("Failure")
    dress_page = BeautifulSoup(new_response.content,'lxml')

    # Then we will get a list of dress products on the first page.
    dress_list = dress_page.findAll("section",{"role":"listitem"})
    product_link = list()
    for dress in dress_list:
        product_link.append(dress.find('a')['href'])

    # For demonstration purpose, I will only extract product information for first ten dresses
    product_dic = dict() # Initilize empty to store product information
    for i in range(10):
        url = 'https://us.shein.com' + product_link[i]
        service = Service('/Applications/chromedriver')
        driver = webdriver.Chrome(service=service)
        driver.get(url)

        # display_name (str)
        try:
            display_name = driver.find_element(By.CLASS_NAME, 'product-intro__head-name')
            product_dic[i]= {'display_name':display_name.text}
        except:
            product_dic[i]= {'display_name':'N/A'}

        # color list (each product has multiple avaliable colors)
        try:
            colors  = driver.find_elements(By.CLASS_NAME, 'product-intro__color-radio')
            color_list = [elem.get_attribute('aria-label') for elem in colors]
            product_dic[i]['color'] = color_list
        except:
            product_dic[i]['color'] = []

        # size (list)
        try:
            size = driver.find_elements(By.CLASS_NAME, 'product-intro__size-radio')
            size_list = [elem.get_attribute('aria-label') for elem in size]
            product_dic[i]['size'] = size_list
        except:
            product_dic[i]['size'] = []

        # price (str)
        try:
            price = driver.find_element(By.CLASS_NAME, 'original')
            product_dic[i]['price'] = price.text
        except:
            product_dic[i]['price'] = 'N/A'

        # product_url (str)
        product_dic[i]['product_url'] = url

        # image_links (list)
        try:
            img = driver.find_element(By.CLASS_NAME, 'product-intro__thumbs')
            imgs = img.find_elements(By.TAG_NAME, 'img')
            image_links = [elem.get_attribute('src') for elem in imgs]
            product_dic[i]['image_links'] = image_links
        except:
            product_dic[i]['image_links'] = []

        # brand_name (str)
        product_dic[i]['brand_name'] = "SHEIN"

        # description (str)
        # Since SHEIN updates its SKU very quickly, it doesn't provide a description for those products
        product_dic[i]['description'] = 'N/A'

        # scrapped_date (date)
        product_dic[i]['date'] = date.today()

        # low_level (str)
        product_dic[i]['low_level'] = 'dress' #As I decided early.

        # gender (str)
        product_dic[i]['gender'] = 'Women' #SHEIN seems to assume buyers' default gender is female

        # secondhand (bool)
        product_dic[i]['secondhand'] = False #Given SHEIN only sells firsthand products
        
    return product_dic