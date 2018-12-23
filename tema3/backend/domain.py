from urllib.parse import urlparse

def get_subdomain_name(url):
    """
    Get the sub domain name (name.example.ro)
    :type url: str
    :rtype: str
    """  

    try:
        return urlparse(url).netloc
    except:
        return 'Cannot get sub domain name from %s. Make sure URL is correct.' % (url)

def get_domain_name(url):
    """
    Get the domain name (example.ro)
    :type url: str
    :rtype: str
    """  
    try:
        results = get_subdomain_name(url).split('.')
        return results[-2] + '.' + results[-1]
    except:
        return 'Cannot get domain name from %s. Make sure URL is correct.' % (url)
    
def get_domain(url):
    """
    Get domain (example)
    :type url: str
    :rtype: str
    """ 

    try:
        result = get_subdomain_name(url).split('.')
        return result[-2]
    except:
        return 'Cannot get domain from %s. Make sure URL is correct.' % (url)