# ==============
# comboTester.py
# ==============

##################
# in-information #
##################
# in configFile: 
#  1 baseArl file location
#  1 modification location
#  * mdtTags (list)
#  * headers (list)
#  * urls (list)
#  * objects (list)

########
# main #
########

from importlib.machinery import SourceFileLoader
import argparse # cmd-line arg parsing
import requests # http://docs.python-requests.org/en/master/
import httpTestingFunctions as htf 
import httpTestingClasses as htc

def main():
  
  bool_args = {
    '-v' : {'long' : '--verbose',
           'action' : 'store_true',
           'help' : 'Turn on verbose logging and debug lines.'
           },
    '-sl' : {'long' : '--stateless',
             'action' : 'store_true',
             'help' : 'run asynchronously since tests do not depend on server state.'
             },
    '-nh' : {'long' : '--no-headers',
             'action' : 'store_true',
             'help' : 'Run the set of test combinations with no headers added to request.'
             },
    '-c' : {'long' : '--copy-config',
            'action' : 'store_true',
            'help' : 'Make copy of server config file.'
           },
    '-iter' : {'long' : '--iterative',
               'action' : 'store_true',
               'help' : 'Iterative headers instead of generating header combinations.'
           }
    }
  
  type_args = {
    '-o' : {'long' : '--output',
            'type' : str,
            'nargs' : 1,
            'help' : 'File to save test result logs to.'
          },
    '-e' : {'long' : '--extension',
            'type' : str,
            'nargs' : 1,
            'help' : 'Custom Extension for temp copy config file.'
      },
    '-to' : {'long' : '--timeout',
             'type' : int,
             'nargs' : 1,
             'help' : 'Manually set timeout for requests (time for bytes to be received). Default is 5s.'
      }
    }
  
  parser = argparse.ArgumentParser(description='Parse options for comboTester.py.')
  parser.add_argument('configFile', type = str, nargs = 1, required = True, help = 'The input test config file to use for generating test combos.')
    
  for hash in bool_args.keys():
    parser.add_argument(hash, hash['long'], action = hash['action'], help = hash['help'])

  for hash in type_args.keys():
    parser.add_argument(hash, hash['long'], nargs = hash['nargs'], help = hash['help'])
    
  args = parser.parse_args()
  
  configFile = SourceFileLoader('configFile', args.configFile[0]).load_module() # imports config file
  # access configFile resources via configFile.blah
  
  # set loop for test combinations with no headers
  min = 1 if args.nh else 0
  
  # set extension
  ext = args.e if args.e else '.bkp' 
  
  # set timeout for returning bytes
  to = args.to if args.to else 5
    
  # get list of header subset combinations
  headerSubsets = htf.generateHeaderCombinations(configFile.headers, min, len(configFile.headers.keys()))
  
  # get list of all metadata combinations
  metadataSubsets = htf.generateMetadataCombinations(configFile.mdtTags)
  
  # create resultsLogger object, set outfile/verbose
  rl = htc.ResultsLogger(args.v, args.o)
    
  # make configMod objects, currently automatically makes copy.
  # in future, might want to allow option to make copy
  # serverConfigFilePath, copyExt, serverDest, action, placeholderTag, mdtTagComboList
  try:
    scm = htc.ServerConfigModifier(configFile.serverConfigOrig, ext, configFile.serverConfigDest, 
                               configFile.action, configFile.searchTag, metadataSubsets)
  except Exception as e:
    msg = '# copy failed: {}\n\
    # modification name: {}\n'.format(e, scm.modName)
    rl.writeToLog(msg)

  # loop0: iterate over mdtTagComboList
  for i in range(len(scm.mdtTagComboList)):
    htf.pushServerConfigModification(scm, rl)

    # loop1: iterate over hosts list
    for ho in configFile.hosts: # host list
      cHeader = {}
      cHeader['Hosts'] = ho

      # loop2: iterate through urls list
      for u in configFile.urls:

        # loop3: iterate through objects hash
        for obj, methods in configFile.objects.items(): # object/endpoint hash

          for method in methods: # loop4: iterate through methods list

            # loop5: iterate over header subsets/combinations
            for hs in headerSubsets: # header subset list
              headersHash = htf.constructHeadersHash(hs, configFile.headers)

              # construct request object from hosts, objects, headers
              req = requests.Request(method, url = u + obj, headers = {**headersHash, **cHeader}, timeout = to)
              session = requests.Session()

              try:
                resp = session.send(req)
                logMsg = rl.logging(resp) # optional argument to preset encoding
                rl.writeToLog(logMsg)
              except Exception as e:
                exceptionMsg = '# server config filename: {0} \n\
                # url: {1} \n\
                # exception msg: {2} \n'.format(scm.origPath, req.url, e)
                rl.writeToLog(exceptionMsg)


  # reset the original from the backup
  scm.resetOriginal()
                                     
# if __name__ == '__main__':
#   main()
