import itertools

#############
# functions #
#############

# purpose: send request to server
# returns: Requests Response Object
def sendRequestObject(r):
  m = r.method.lower()
  
  if m == 'get':
    resp = requests.get(r.url, headers = r.headers, params = r.params,
                       data = r.data, timeout = r.timeout)
  elif m == 'post':
    resp = requests.post(r.url, headers = r.headers, params = r.params,
                       data = r.data, timeout = r.timeout)
  return resp # response object


def constructHeadersHash(headersList, headersHash):
  outHash = {}
  for h in headersList:
    outHash[h] = headersHash[h]
  return outHash


# purpose: generates all possible combinations of headers keys of given size
# returns: a list of all subsets (list of list/array of arrays)
def generateHeaderCombinations(headersHash, minSize, maxSize):
  headersList = headersHash.keys()
  headerCombinationsList = []
  
  for i in range(minSize, maxSize+1):
    for subset in itertools.combinations(headersList):
      headerCombinationsList.append(subset)
  
  return headerCombinationsList


# takes ServerConfigModifier object and logger
# runs through the workflow
def pushServerConfigModification(scm, logger):
  try:
    scm.modifierAction()
  except Exception as e:
    msg = '# change to copy failed: {}\n\
    # modification name: {}'.format(e, scm.modName)
    logger.writeToLog(msg)

  try:
    scm.pushToServer()
  except Exception as e:
    msg = '# push to server failed: {}\n\
    # modification name: {}\n'.format(e, scm.modName)
    logger.writeToLog(msg)


# in: mdtTags = {
#   'option1': ['on', 'off'],
#   'option2' : ['on', 'off'],
#   }
# out: mdtOptionsList = [ '<option1> on </option1> <option2> on </option2>',
# '<option1> on </option1> <option2> off </option2>',
# '<option1> off </option1> <option2> on </option2>',
# '<option1> off </option1> <option2> off </option2>'
# ]

# purpose: generate list of combinations
def generateMetadataCombinations(mdtHash):
  combinationsList = []
  for k, v in mdtHash.items():
    innerList = []
    for i in v:
      tag = '<{0}> {1} </{0}>'.format(k, i)
      innerList.append(tag)
    combinationsList.append(innerList)
  
  # takes list of raw data and generates combinations 
  return [ x for x in itertools.product (*combinationsList) ]
    