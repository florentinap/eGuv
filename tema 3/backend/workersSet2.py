import threading
# import logging
import pika
import json
import requests
import urllib
from time import sleep
from itertools import cycle
from urllib.error import URLError, HTTPError
from htmlParser import HTMLTagParser
from socket import error as SocketError
from crawlerQueue import CrawlerQueue
from configRabbitMQ import *
from proxyProvider import *


# logging.basicConfig(level=logging.DEBUG,
#                     format='(%(threadName)-9s) %(message)s',)

class WorkersSet2(threading.Thread):

    def __init__(self, group = None, target = None, name = None,
                 args=(), kwargs = None, verbose = None):
        super(WorkersSet2, self).__init__()

        self.queueRecv = CrawlerQueue(RabbitMQ.HOST.value, RabbitMQ.Q1.value, True)
        self.queueSend = CrawlerQueue(RabbitMQ.HOST.value, RabbitMQ.Q2.value, True)

        self.proxy_pool = cycle(get_proxies())

    def callback(self, ch, method, properties, body):
        ch.basic_ack(delivery_tag = method.delivery_tag)
        self.gather_HTML_content(body)

    def run(self):
        while True:
            self.queueRecv.get(self.callback)
        return

    def gather_HTML_content(self, page_url):
        """
        Convert raw response data into readable information and checks for proper html formatting
        :type page_url: str
        :rtype: None
        """

        html_string = ''
        try:
            page_url = page_url.decode('ascii')

            sleep(1)
            proxy = next(self.proxy_pool)
            proxy = urllib.request.ProxyHandler({'http': proxy})
            opener = urllib.request.build_opener(proxy)
            urllib.request.install_opener(opener)
            response = urllib.request.urlopen(page_url)

            header = response.getheader('Content-Type')
            if 'text/html' in header:
                html = response.read()
                try:
                    html_string = html.decode('utf-8')
                except UnicodeDecodeError as e:
                    html_string = html.decode('latin-1')

                sendDict = {page_url: html_string}
                self.queueSend.set(json.dumps(sendDict))
        # [Errno 104] Connection reset by peer python
        except SocketError as e:
            print('[WorkerSet2] Connection reset')
            return set()
        # [Errno 111] Connection refused
        except URLError:
            print('[WorkerSet2] Cannot connect')
            return set()
        # HTTP Error 404: Not Found 
        except HTTPError:
            print('[WorkerSet2] Cannot download page ' + page_url)
            return set()
        except Exception as e:
            print(str(e))
            return set()
        return html_string
