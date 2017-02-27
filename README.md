# httpTesting - Python 3.4
A tool to test requests against various combinations of server configurations and headers

# Workflow:
- 1. iterate over mdtTag subsets
- 2. iterate over host list
- 3. build Request object from url, object, method, and headers
- 4. make request
- 5. log response


# future features:
- a wrapper to have tool run against multiple server config files
  - also depending on servers hit and state-dependency, could run tests asynchronously
- stateless functionality - for RESTful testing (async)
- more action types (delete)
- option for no server configuration file
- iterative approach to headers and metadata tag changes
