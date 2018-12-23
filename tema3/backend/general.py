import os
import re
import unidecode
from collections import OrderedDict

def create_project_dir(directory):
    """
    Each website is a separate project (folder)
    :type directory: str
    :rtype: None
    """ 

    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)


def create_data_files(project_name, base_url):
    """
    Create queue and crawled files (if not created)
    :type project_name: str
    :type base_url: str
    :rtype: None
    """ 

    queue = os.path.join(project_name , 'queue.txt')
    crawled = os.path.join(project_name, 'crawled.txt')
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')


def write_file(path, data):
    """
    Create a new file
    :type path: str
    :type data: str
    :rtype: None
    """ 

    with open(path, 'w') as f:
        f.write(data)


def append_to_file(path, data):
    """
    Add data onto an existing file
    :type path: str
    :type data: str
    :rtype: None
    """ 

    with open(path, 'a') as file:
        file.write(data + '\n')


def delete_file_contents(path):
    """
    Delete the contents of a file
    :type path: str
    :rtype: None
    """ 

    open(path, 'w').close()


def file_to_set(file_name):
    """
    Read a file and convert each line to set items
    :type file_name: str
    :rtype: Set[str]
    """ 

    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


def set_to_file(links, file_name):
    """
    Iterate through a set, each item will be a line in a file
    :type links: List[str]
    :type file_name: str
    :rtype: None
    """ 

    with open(file_name, "w") as f:
        for l in sorted(links):
            f.write(l+"\n")
