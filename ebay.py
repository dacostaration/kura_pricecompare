# ebay.py

import sys 
import http.client
from urllib import parse
import json
import ast
import re

# API: https://rapidapi.com/augsmachado/api/ebay-data-scraper/

# URL encode user product input
# @param: prod
# @return: URL-safe product "string" value
# This function will convert characters that cannot be used in a URL to their URL-safe format [%2A, etc.]
# https://dev.to/serhatteker/convert-strings-to-be-url-safe-1b05
def cleanProd(prod):
    return parse.quote(prod)

# clean API object string
# @param: pr
# @return: line item price as a "float" data type
# Expected Formats:
#   a. index:0, price:$20.00
#   b. index:1, price:C $529.00 to C $619.00
def cleanPrice(pr):
    ret=0.00
    mylist = re.findall(r'\$[1-9]\d*(?:\.\d{2})?(?=\s|$)', pr)
    # print(">> mylist:")
    # print(mylist)
    if len(mylist) == 0:
        ret = 0.00
    elif len(mylist) == 1:
        ret = round(float(mylist[0].replace('$','')), 2)
    else:
        low = float(mylist[0].replace('$',''))
        high = float(mylist[1].replace('$',''))
        ret = round((low+high)/2, 2)
    return ret

# CONFIGURATION #############################################################################
# TEST flag
# Manually manipulated in order to print certain items to the console when testing the script
test=False       #....default test value = false
if len(sys.argv) > 2:
    if sys.argv[2] == 'true': 
        test=True

# testLimit: Used to force terminate loop through product listings
testLimit=False
testLimitLimit=3
channel="eBay"

# print(">> in ebay.py")
# print(sys.argv)
# print(f"test:{test}")

# print(sys.argv[1])      # input product to search
if len(sys.argv) < 2:
    # print("error: no valid input")
    exit("ERROR: no valid input")
else:
    # print(f"let's search {channel} for this thing...[{sys.argv[1]}]")
    urlProd=cleanProd(sys.argv[1])
    
    # API: https://rapidapi.com/augsmachado/api/ebay-data-scraper/
    conn = http.client.HTTPSConnection("ebay-data-scraper.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "8750ff5319mshacf7e441d65582dp1089abjsn933f4eee7715",
        'X-RapidAPI-Host': "ebay-data-scraper.p.rapidapi.com"
        }

    if not test:
        # print(">> NOT TEST")
        # "/products?page_number=1&product_name=macbook%20air&country=canada"
        req="/products?page_number=1&product_name="+urlProd+"&country=canada"
        conn.request("GET", req, headers=headers)

        res = conn.getresponse()
        data = res.read()

        # remove new line characters from data - this produces malformed objects and complicates data processing
        data2=(data.decode("utf-8"))
        data2=data2.strip()     #..........strip used to clean object string of new line characters
        data=ast.literal_eval(data2)    #........ast library's method "literal_eval" used to rebuild true object from string


    else:
        # print(">> TEST")
        data=[{"product_id":"123456","name":"","condition":"Brand New","price":"$20.00","discount":"","product_location":"","logistics_cost":"","description":"Brand New","link":"https://ebay.com/itm/123456?hash=item28caef0a3a:g:E3kAAOSwlGJiMikD&amdata=enc%3AAQAHAAAAsJoWXGf0hxNZspTmhb8%2FTJCCurAWCHuXJ2Xi3S9cwXL6BX04zSEiVaDMCvsUbApftgXEAHGJU1ZGugZO%2FnW1U7Gb6vgoL%2BmXlqCbLkwoZfF3AUAK8YvJ5B4%2BnhFA7ID4dxpYs4jjExEnN5SR2g1mQe7QtLkmGt%2FZ%2FbH2W62cXPuKbf550ExbnBPO2QJyZTXYCuw5KVkMdFMDuoB4p3FwJKcSPzez5kyQyVjyiIq6PB2q%7Ctkp%3ABlBMULq7kqyXYA","thumbnail":"https://ir.ebaystatic.com/rs/v/fxxj3ttftm5ltcqnto1o4baovyl.png"},{"product_id":"393531906094","name":"","condition":"Excellent - Refurbished","price":"C $529.00 to C $619.00","discount":"","product_location":"","logistics_cost":"Free shipping","description":"Excellent - Refurbished","link":"https://www.ebay.ca/itm/393531906094?epid=19042851646&hash=item5ba054582e:g:93cAAOSwvEJgbLW8&amdata=enc%3AAQAHAAAA4KnXrw1ED%2BLBgrvBussKQ2H6TW4cLTOa9XnF%2FyDFa%2BwqcoSpeCLjaRQT0%2FXWsS6SR1mD174Sao4e%2FIdfqXliIYy6gbtRsFW2XD%2FH0tNc7RCTgTeDTYxe%2FtnjZaX9E0HnJA64mxWsja9GX9BH%2FU92cpFTte3je4p7Wi3YPmuZODAOpkWwRaGCir5U%2BguIGUeLy4vWDznXAwq23v3g62ywJSaZfjEb%2FwqO81yVZHKQa%2FDPuEILdX16QBzhz8XIeDW%2Fszr%2BAFpEmnwotkvMjx461uEBMUsuiD%2F6DU1nTpsjDIL9%7Ctkp%3ABFBMqMz19uVg","thumbnail":"https://i.ebayimg.com/thumbs/images/g/93cAAOSwvEJgbLW8/s-l225.jpg"},{"product_id":"394038344492","name":"","condition":"Excellent - Refurbished","price":"C $419.00 to C $520.00","discount":"","product_location":"","logistics_cost":"Free shipping","description":"Excellent - Refurbished","link":"https://www.ebay.ca/itm/394038344492?epid=17035818063&hash=item5bbe83fb2c:g:eJoAAOSwhAxgbLQQ&amdata=enc%3AAQAHAAAA4EmQyBY442X0CQhVUnyqVZS3UUJI5xkQpa%2FbIJBNIQXXUoFNh0mkjrVn8cVgOYXkUq7thHe786AXgJTdBo59jjskWT2JupD17xti0YY4vgezPQwTdZtTkHisvgoni2mlCFNJ4%2F1MEsb3DKPWnGJqEfQs2cNNtvZp3G2A9nWh7o5jWMnLEeYhvsZvAlnS%2Buw%2Fm7d2WzFbyaLcJ6I0gtohRKKSsaCax3unSHUAgCukZ%2By7bTnxgAUvsUSfeb%2BuDt2Rj8rwFu%2FB5ta2mUPxN8axlDbVShRjMqcHEe4EzeH26cgv%7Ctkp%3ABFBMqMz19uVg","thumbnail":"https://i.ebayimg.com/thumbs/images/g/eJoAAOSwhAxgbLQQ/s-l225.jpg"},{"product_id":"394038312599","name":"","condition":"Excellent - Refurbished","price":"C $499.00 to C $540.00","discount":"","product_location":"","logistics_cost":"Free shipping","description":"Excellent - Refurbished","link":"https://www.ebay.ca/itm/394038312599?epid=13034214288&hash=item5bbe837e97:g:k2MAAOSwCYBhsSsd&amdata=enc%3AAQAHAAAA4GPbN8IF4bbgd0Y5Q2juaZF%2FYWpci9pir5uh0Kv9w18l%2BZ8VnKrjIslPixV85xtGnH2bNcwG2N%2Fd84qhBYOtMoONKwP7kVD3G5vkVybA7bwjO04RUcWXapVII2yQdqh%2BEpAuIaLgk6eK5Tc6hUsqDvk3b%2BNxRBzYdg9UVfLV2vuqDtsIpsS0NN6d4L%2FzlFjy8XXjXfqLP%2FNQiDhH7qiwxaKb7wieBucWD4%2F1i8oQl9dZlhBNfD9xoN1jHrpCrOl3CHpI0LdTY4lLtx746YBDeI01BG0P%2BPW%2B2yevUL3j5feH%7Ctkp%3ABFBMqMz19uVg","thumbnail":"https://i.ebayimg.com/thumbs/images/g/k2MAAOSwCYBhsSsd/s-l225.jpg"},{"product_id":"393776000362","name":"","condition":"Very Good - Refurbished","price":"C $455.00 to C $535.00","discount":"","product_location":"","logistics_cost":"Free shipping","description":"Very Good - Refurbished","link":"https://www.ebay.ca/itm/393776000362?epid=9037957801&hash=item5baee0ed6a:g:k2MAAOSwCYBhsSsd&amdata=enc%3AAQAHAAAA4KxBKyVhWfFPL%2BVkDacCQiVuxVvZaKti485Vvhx2i8qJgbtC1XluPYBCxW5fJD57yH0Mveac61ZbWri08lzcItiNOpq2mth9LvQu9Yo1NTFKc4TFZUI4QXBMN5FiMkjKql6uUm0i6EuKJNUxu7ZSh%2BOK60hNPQOJXtvzJSF99C7mWMtYp8hY5PaOSi7NbY0BkhAc7F6CBtGCJltB9f%2BeWxFwaNtKLCFPt3I6RkqnvCleLCtjVHJjl6JrvVBFL%2FDJ1SGwd%2BUbB%2Bi8m%2Bitx0cXoHvvvGqyBkiD32oEyOxESmHt%7Ctkp%3ABFBMqMz19uVg","thumbnail":"https://i.ebayimg.com/thumbs/images/g/k2MAAOSwCYBhsSsd/s-l225.jpg"},{"product_id":"144195215991","name":"","condition":"Good - Refurbished","price":"C $404.37","discount":"","product_location":"from United States","logistics_cost":"+C $25.71 shipping estimate","description":"Free 2-Day Shipping | 1 YEAR WARRANTY| Free ReturnsGood - Refurbished","link":"https://www.ebay.ca/itm/144195215991?epid=17035818063&hash=item2192b46277:g:N0MAAOSw9JVhO7M9&amdata=enc%3AAQAHAAAA4Pwx%2B9rRlgnr3YWmsRQ1aI9kE%2BAiceDlKp92mjyXnP2yLMSc0XnPmVvHGNVck0xCJa2nCXOK0%2FjtnNh6NdDrzDIEeEEOzIs%2F9vx%2BBpg6C4yVPVAPpsA04HwraJlqDWkKsR7FJbxLFMbHjn%2Bb5GnJDUvItcKoTyfx8fRX9df%2BUN%2BjK784fuG9NO5pRxXagBecIF96QKRf52GWnFz2SfQWsRRQELCwrBUduP4lR8BRmCnMwQIPSZFOW3Sc3FtzC%2FWTnDbq5y2G9O4MKXTHLRgz%2FTtzaJyCztc%2FomW5jkSbgDd3%7Ctkp%3ABk9SR6jM9fblYA","thumbnail":"https://i.ebayimg.com/thumbs/images/g/N0MAAOSw9JVhO7M9/s-l225.jpg"}]

    # let's search eBay for this thing...[iphone 11]
    # [{"product_id":"123456","name":"","condition":"Brand New","price":"$20.00","discount":"","product_location":"","logistics_cost":"","description":"Brand New"
    # ,"link":"https://ebay.com/itm/123456?hash=item28caef0a3a:g:E3kAAOSwlGJiMikD&amdata=enc%3AAQAHAAAAsJoWXGf0hxNZspTmhb8%2FTJCCurAWCHuXJ2Xi3S9cwXL6BX04zSEiVaDMCvsUbApftgXEAHGJU1ZGugZO%2FnW1U7Gb6vgoL%2BmXlqCbLkwoZfF3AUAK8YvJ5B4%2BnhFA7ID4dxpYs4jjExEnN5SR2g1mQe7QtLkmGt%2FZ%2FbH2W62cXPuKbf550ExbnBPO2QJyZTXYCuw5KVkMdFMDuoB4p3FwJKcSPzez5kyQyVjyiIq6PB2q%7Ctkp%3ABlBMULq7kqyXYA"
    # ,"thumbnail":"https://ir.ebaystatic.com/rs/v/fxxj3ttftm5ltcqnto1o4baovyl.png"},
    # ---------------------------

    datadecoded=data        
    minPrice=0.00
    maxPrice=0.00
    avgPrice=0.00
    totPrice=0.00
    cc=0
    # for itm in datadecoded:
    for index, item in enumerate(datadecoded):
        # print(f"index:{index}, item: {item}")   # item:{item.price}")
        # print(f"index:{index}, item.product_id:{item['product_id']}")    #, data[itm]:{datadecoded[cc]}")
        # print(f"index:{index}, price:{item['price']}")
        curPriceStr=item['price']
        curPrice=cleanPrice(curPriceStr)
        # curPrice=float(curPriceStr[1:])
        if minPrice == 0.00:
            minPrice = curPrice
        if curPrice < minPrice:
            minPrice=curPrice
        if curPrice >= maxPrice:
            maxPrice=curPrice
        
        totPrice+=curPrice
        cc+=1
        if testLimit:
            if cc > (testLimitLimit-1):
                break

    avgPrice = round((totPrice/cc), 2)
    totPrice=round(totPrice,2)

    # result string
    # "minPrice:{minPrice},maxPrice:{maxPrice},totPrice:{totPrice},count:{cc},avgPrice:{avgPrice}"
    resStr = "minPrice:"+str(minPrice)+"|maxPrice:"+str(maxPrice)+"|totPrice:"+str(totPrice)+"|listingsChecked:"+str(cc)+"|avgPrice:"+str(avgPrice)
    if test:
        print(resStr)

exit(resStr)