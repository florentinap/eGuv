from enum import Enum

class credentials(Enum):
    HOST = 'localhost'
    USER = 'root'
    PASSWORD = 'flory95'
    WORKSPACE = 'egov'

class Keys(Enum):
    TABLE = 'table'
    ID  = 'id'
    URL = 'url'
    MINISTER = 'minister'
    PAP = 'pap'

class dataTypes(Enum):
    ID = 'INT AUTO_INCREMENT PRIMARY KEY'
    URL = 'VARCHAR(50)'
    MINISTER = 'TEXT',
    PAP = 'TEXT'
