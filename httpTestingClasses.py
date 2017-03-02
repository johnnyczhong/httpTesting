import shutil
  
###########
# classes #
###########

# designed to take:
#  1 base server config location
#  1 server config destination
#  1 action (add or replace)
#  1 placeholder (location for action)
#  * mdtTags (list)
class ServerConfigModifier:
  def __init__(self, serverConfigFilePath, copyExt, serverDest, action, placeholderTag, mdtTagComboList): 
    self.origPath = serverConfigFilePath
    self.backupPath = self.makeCopy(copyExt)
    self.serverDest = serverDest
    self.mdtTagComboList = tuple(mdtTagComboList)
    self.action = action
    self.placeholderTag = placeholderTag
    self.mdtTagIndex = 0 #start at the beginning of the list, keep state
    
    
  # make copy of file at self.orig
  # new file name should be *self.orig.tmp
  def makeCopy(self, ext):
    copyPath = self.origPath + ext
    shutil.copy2(self.origPath, copyPath)
    return copyPath
  
  
   
  def modifierAction(self):
    if self.action == 'add':
      self.changePlaceholderTag()
    elif self.action == 'replace':
      self.replaceSearchTag()
    self.mdtTagIndex += 1
    

      
  def replaceSearchTag(self):
    addTag = self.mdtTagComboList[self.mdtTagIndex]

    with open(self.backupPath) as infile:
      file = infile.read()
    
    file.replace(self.placeholderTag, addTag)
    
    with open(self.origPath, 'w') as outfile:
      outfile.write(file)
      
      
      
  # search for placeholder tag and replace with newTag
  def changePlaceholderTag(self):
    addTag = ''
    subsets = self.mdtTagComboList[self.mdtTagIndex]

    for s in subsets:
      addTag += s

    with open(self.backupPath, 'r') as infile:
      file = infile.read()
    
    file = file.replace(self.placeholderTag, addTag + self.placeholderTag)
    
    with open(self.origPath, 'w') as outfile:
      outfile.write(file)
  
  
  
  # push *self.origPath to server
  def pushToServer(self):
    shutil.copy2(self.origPath, self.serverDest)
         
  def resetOriginal(self):
    shutil.copy2(self.backupPath, self.origPath)
    
# write to file or screen
class ResultsLogger:
  def __init__(self, verbose, outfile):
    self.logFile = outfile
    self.verbose = verbose
    
  
  
  
  # purpose: print to screen or print to file
  def writeToLog(self, outString):
    if not self.logFile:
      print(outString + '\n')
    else:
      with open(self.logFile, 'w+') as f:
        f.write(outString + '\n') # newline?

        
  
  # purpose: create log string
  # serverResponse is a Requests Response object
  def logging(self, resp, encoding = None):
    if encoding:
      resp.encoding = encoding
    
    msg = ''
    if self.verbose:
      msg += 'URL: {0}\n\
      # Code: {1}\n\
      # Redirected: {2}\n\
      # Headers: {3}\n\
      # Text: {4}\n\
      # Elaspsed: {5}\n'.format(resp.url, resp.status_code, resp.is_redirect,
                                resp.headers, resp.text, resp.elapsed)
    else:
      msg += '# Code: {0}\n\
      # Text: {1}\n'.format(resp.status_code, resp.text)
    
    return msg


  def logRequest(self, req):
    msg = ''

    if self.verbose:
      msg += 'URL: {0}\n\
      # Headers: {1}\n\
      # Method: {2}\n'.format(req.url, req.headers, req.method)
    else:
      msg += '# URL: {0}\n\
      # Headers: {1}\n'.format(req.url, req.headers)
    
    return msg
