import sys
from domain import *
from general import *
from ministere import *
from workers import Workers

def main(argv):
    NUMBER_OF_THREADS = 16
    HOMEPAGES = [gouvenmentSites['mcin'][1]]

    for HOMEPAGE in HOMEPAGES:
    	PROJECT_NAME = get_domain(HOMEPAGE)
    	DOMAIN_NAME = get_domain_name(HOMEPAGE)

    	workers = Workers(NUMBER_OF_THREADS)
    	workers.create_workers(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

if __name__ == "__main__":
    main(sys.argv)
