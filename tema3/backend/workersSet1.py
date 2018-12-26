import threading
# import logging
import pika
import requests
import urllib
from urllib.request import Request
from domain import *
from general import *
from time import sleep
from itertools import cycle
from urllib.error import URLError, HTTPError
from htmlParser import HTMLTagParser
from socket import error as SocketError
from commonQueue import CommonQueue
from crawlerQueue import CrawlerQueue
from configRabbitMQ import *
from proxyProvider import *

# logging.basicConfig(level=logging.DEBUG,
#                     format='(%(threadName)-9s) %(message)s',)

class WorkersSet1(threading.Thread):

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''

    def __init__(self, group = None, target = None, name = None,
                 args = (), kwargs = None, verbose = None, 
                 project_name = None, base_url = None, domain_name = None):
        super(WorkersSet1, self).__init__()

        self.project_name = project_name
        self.base_url = base_url
        self.domain_name = domain_name
        self.queue_file = self.project_name + '/queue.txt'
        self.crawled_file = self.project_name + '/crawled.txt'
        self.queueSend = CrawlerQueue(RabbitMQ.HOST.value, RabbitMQ.Q1.value, True)

        self.proxy_pool = cycle(get_proxies())

        self.boot()

    def boot(self):
        """
        Create directory and queue files 
        :rtype: None
        """

        create_project_dir(self.project_name)
        create_data_files(self.project_name, self.base_url)
        CommonQueue.queue = file_to_set(self.queue_file)
        CommonQueue.crawled = file_to_set(self.crawled_file)

    def crawl_page(self, page_url):
        """
        Fill queue and updates files
        :type page_url: str
        :rtype: None
        """

        if page_url not in CommonQueue.crawled:
            print('Queue ' + str(len(CommonQueue.queue)) + ' | Crawled  ' + str(len(CommonQueue.crawled)))
            links = self.gather_links(page_url)
            self.add_links_to_queue(links)
            CommonQueue.queue.remove(page_url)
            CommonQueue.crawled.add(page_url)
            self.update_files()

    def gather_links(self, page_url):
        """
        Convert raw response data into readable information, insert current URL into Q1 queue and returns all URL from the HTML content
        :type page_url: str
        :rtype: List[str]
        """

        html_string = ''
        try:
            page_url = page_url.replace(' ', '%20')
            page_url = page_url.encode('ascii', 'ignore').decode('ascii')

            try:
                sleep(1)
                req = Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
                response = urllib.request.urlopen(req)
                header = response.getheader('Content-Type')

                if 'text/html' in header:
                    html = response.read()
                    try:
                        html_string = html.decode('utf-8')
                    except UnicodeDecodeError as e:
                        html_string = html.decode('latin-1')
                        
                finder = HTMLTagParser()
                finder.setup(self.base_url, self.project_name)
                finder.feed(html_string)
            # [Errno 104] Connection reset by peer python
            except SocketError as e:
                print('[WorkerSet1] Connection reset ' + page_url)
                return set()
            # [Errno 111] Connection refused
            except URLError:
                print('[WorkerSet1] Cannot connect ' + page_url)
                return set()
            # HTTP Error 404: Not Found 
            except HTTPError:
                print('[WorkerSet1] Cannot download page ' + page_url)
                return set()
        except Exception as e:
            print(str(e))
            return set()

        self.queueSend.set(page_url)
        return finder.get_page_links()

    def add_links_to_queue(self, links):
        """
        Save queue data to project files
        :type page_url: List[str]
        :rtype: None
        """

        for url in links:
            if (url in CommonQueue.queue) or (url in CommonQueue.crawled):
                continue
            if self.domain_name != get_domain_name(url):
                continue
            CommonQueue.queue.add(url)

    def update_files(self):
        """
        Write links in file
        :rtype: None
        """

        set_to_file(CommonQueue.queue, self.queue_file)
        set_to_file(CommonQueue.crawled, self.crawled_file)

    def run(self):
        self.work()

    def work(self):
        """
        Do the next job in the queue
        """

        while True:
            url = CommonQueue.commonqueue.get()
            self.crawl_page(url)
            CommonQueue.commonqueue.task_done()

    def create_jobs(self):
        """
        Each queued link is a new job
        """

        for link in file_to_set(self.queue_file):
            CommonQueue.commonqueue.put(link)
        CommonQueue.commonqueue.join()
        self.crawl()

    def crawl(self):
        """
        Check if there are items in the queue, if so crawl them
        """
        
        queued_links = file_to_set(self.queue_file)
        if len(queued_links) > 0:
            self.create_jobs()