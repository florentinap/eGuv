import pika

class CrawlerQueue:

    def __init__(self, host, queue, durable = True): 
        """
        Connect to RabbitMQ queue
        :type host: str
        :type queue: str
        :type durable: bool
        :rtype: None
        """  

        self.queue = queue
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host = host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue = queue, durable = durable)

    def get(self, callback, prefetch_count = 1):
        """
        Get data from queue
        :type callback: 
        :type prefetch_count: int
        :rtype: None
        """  

        self.channel.basic_qos(prefetch_count = prefetch_count)
        self.channel.basic_consume(callback, queue = self.queue)
        self.channel.start_consuming()

    def set(self, message, exchange = '', delivery_mode = 2):
        """
        Insert data into queue
        :type message: str
        :type exchange: str
        :type delivery_mode: int
        :rtype: None
        """  

        self.channel.basic_publish(exchange = exchange,
                      routing_key = self.queue,
                      body = message,
                      properties = pika.BasicProperties(
                         delivery_mode = delivery_mode, 
                      ))