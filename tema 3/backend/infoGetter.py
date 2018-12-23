from parserMain import *
from urllib.request import urlopen

def getProductInfo(URL):    
    """
    Get the product's info 
    :type URL: str
    :rtype: dict
    """
    
    response = urlopen(URL)
    header = response.getheader('Content-Type')
    if 'text/html' in header:
        html = response.read()
        try:
            html_string = html.decode('utf-8')
        except UnicodeDecodeError as e:
            html_string = html.decode('latin-1')
    targetProductInfo = selectParser(URL, html_string)
    return targetProductInfo
