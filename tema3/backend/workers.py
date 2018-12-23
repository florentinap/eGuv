import threading
from workersSet1 import WorkersSet1
from workersSet2 import WorkersSet2
from workersSet3 import WorkersSet3


# handle the three sets of workers for the crawler
class Workers:

    number_of_workers_set1 = 1
    number_of_workers_set2 = 1
    number_of_workers_set3 = 1

    # set the number of workers for every set
    def __init__(self, number_of_workers):
        self.number_of_workers_set1 = number_of_workers
        self.number_of_workers_set2 = number_of_workers
        self.number_of_workers_set3 = number_of_workers

    # create the three sets of workers
    def create_workers(self, project_name, homepage, domain_name):
        for _ in range(self.number_of_workers_set2):
            worker = WorkersSet2()
            worker.daemon = True
            worker.start()

        for _ in range(self.number_of_workers_set3):
            worker = WorkersSet3()
            worker.daemon = True
            worker.start()
        
        workerMaster = WorkersSet1(project_name = project_name, base_url = homepage, domain_name = domain_name)
        workerMaster.daemon = True
        workerMaster.crawl_page(homepage)

        for _ in range(self.number_of_workers_set1):
            worker = WorkersSet1(project_name = project_name, base_url = homepage, domain_name = domain_name)
            worker.daemon = True
            worker.start()
            
        workerMaster.crawl()