from html.parser import HTMLParser
from urllib import parse

class HTMLTagParser(HTMLParser):
    """
    HTML parser that overrides the handler methods
    :type HTMLParser: HTMLParser
    """

    def __init__(self):
        super().__init__()
        self.links = set()

    def setup(self, base_url, domain):
        """
        :type base_url: str
        :type domain: str
        :rtype: None
        """
        
        self.base_url = base_url
        self.domain = domain

    def handle_starttag(self, tag, attrs):
        """
        Function called when an opening tag is encountered
        :type tag: str
        :type attrs: List[str]
        :rtype: None
        """

        # handle the encounter of an opening tag <a>
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)
                    # return only internal URL
                    if self.domain in url:
                        self.links.add(url)

    def get_page_links(self):
        """
        Return all discovered url in current page 
        """
        
        return self.links
