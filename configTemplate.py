# configuration file template for httpTesting

serverConfigOrig = 'path/to/config/file.txt'
serverConfigDest = 'path/to/dest/file.txt'
action = 'add' # add only for now
searchTag = '</example>'

hosts = ['localhost'] 

mdtTags = {
	'tagName' : ['on', 'off']
}

urls = [
	'example.com'
]

objects = {
	'example.html' : ['GET', 'POST']
}

headers = {
	'header-name' : 'value' 
}
