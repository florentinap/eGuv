import MySQLdb

def getAllMinisters():
	mydb = MySQLdb.connect(host = 'localhost', user = 'root', passwd = 'flory95', db = 'egov', use_unicode = True, charset = 'utf8')
	cursor = mydb.cursor()

	query = 'SELECT nume, url FROM ministere'
	try:
		cursor.execute(query)
	except Exception as e:
		print (e)

	header = [x[0] for x in cursor.description]
	data = cursor.fetchall()[1:]
	cursor.close()

	result = []
	for d in data:
		nume = d[0]
		url = d[1]
		result.append(dict(zip(header, (nume, url))))

	return result

def getPap(minister):
	mydb = MySQLdb.connect(host = 'localhost', user = 'root', passwd = 'flory95', db = 'egov', use_unicode = True, charset = 'utf8')
	cursor = mydb.cursor()

	query = 'SELECT url FROM tema3 WHERE minister=\'' + minister + '\''
	try:
		cursor.execute(query)
	except Exception as e:
		print (e)

	header = [x[0] for x in cursor.description]
	data = cursor.fetchall()[1:]
	cursor.close()

	result = []
	for d in data:
		url = d[0]
		result.append(url)
	return result

def getData():
	result = []
	ministers = getAllMinisters()
	for m in ministers:
		paps = getPap(m['url'].split('//')[1][:-1])
		result.append({'nume': m['nume'], 'url': m['url'], 'paps': paps})
	
	return result