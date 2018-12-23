import threading
# import logging
import pika
import json
from bs4 import BeautifulSoup
from crawlerDB import CrawlerDB 
from crawlerQueue import CrawlerQueue
from domain import *
from configDB import *
from configRabbitMQ import *

# logging.basicConfig(level=logging.DEBUG,
#                     format='(%(threadName)-9s) %(message)s',)

class WorkersSet3(threading.Thread):

    def __init__(self, group = None, target = None, name = None,
                 args = (), kwargs = None, verbose = None):
        super(WorkersSet3, self).__init__()

        self.tableName = 'tema3'
        self.queueRecv = CrawlerQueue(RabbitMQ.HOST.value, RabbitMQ.Q2.value, True)
        self.cache = CrawlerDB(credentials.HOST.value, 
                                credentials.USER.value, 
                                credentials.PASSWORD.value, 
                                credentials.WORKSPACE.value)
        createDict = {Keys.TABLE.value: self.tableName,
                        Keys.ID.value: dataTypes.ID.value,
                        Keys.URL.value: dataTypes.URL.value, 
                        Keys.MINISTER.value: dataTypes.MINISTER.value,
                        Keys.PAP.value: dataTypes.PAP.value}
                        
        #if self.cache.checkExists(self.tableName) == 0:
        #    self.cache.create(createDict)

    def callback(self, ch, method, properties, body):
        ch.basic_ack(delivery_tag = method.delivery_tag)
        self.parser_HTML(json.loads(body.decode('utf-8')))

    def run(self):
        while True:
            self.queueRecv.get(self.callback)
        return

    def parser_HTML(self, HTML_content):
        """
        Parse the HTML content in order to get the necessary data and to insert them into database
        :type HTML_content: str
        :rtype: None
        """

        URL = list(HTML_content.keys())[0]
        body = list(HTML_content.values())[0]
        soup = BeautifulSoup(body, 'html.parser')
        
        insertDict = {}

        for link in soup.find_all('a'):
            currentLink = link.get('href')
            title = link.get('title')
            if ((currentLink.endswith('pdf') or currentLink.endswith('xlsx')) and 'paap' in currentLink.lower()) or (title and 'paap' in title.lower()):
                    insertDict[Keys.URL.value] = currentLink
                    insertDict[Keys.PAP.value] = link.contents[0]
                    insertDict[Keys.TABLE.value] = self.tableName
                    insertDict[Keys.MINISTER.value] = get_subdomain_name(URL)
                    print('====================================================================')
                    print(insertDict)


        #self.cache.insert(insertDict)