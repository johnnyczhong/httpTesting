# configuration file template for httpTesting

serverConfigOrig = 'path/to/config/file.txt'
serverConfigDest = 'path/to/dest/file.txt'

# "add" will add the tag in front of the search tag.
# "replace" will replaced the string with your tag
action = 'add' # add or replace
searchTag = '</example>'

mdtTags = {
	'tagName' : ['on', 'off']
}

urls = [
	'http://example.com/'
]

objects = {
	'example.html' : ['GET', 'POST']
}

headers = {
	'header-name' : 'value' 
}

constantHeaders = {
	'cheader-name' : 'value'
}
