#!/usr/bin/python
import requests # get the requsts library from https://github.com/requests/requests


file_name = "/Users/meghasinghrajpoot/Desktop/RPI/Data Analytics/Project/Updated/data-science-f21/data/windData/subset_M2T1NXSLV_5.12.4_20211206_170111.txt"
with open(file_name) as f:
    contents = f.readlines()

data_list = contents[139:145]
print(len(data_list))



# overriding requests.Session.rebuild_auth to mantain headers when redirected
 
class SessionWithHeaderRedirection(requests.Session):
    AUTH_HOST = 'urs.earthdata.nasa.gov'
    def __init__(self, username, password):
        super().__init__()
        self.auth = (username, password)
   # Overrides from the library to keep headers when redirected to or from
   # the NASA auth host.
    def rebuild_auth(self, prepared_request, response):
        headers = prepared_request.headers
        url = prepared_request.url
        if 'Authorization' in headers:
            original_parsed = requests.utils.urlparse(response.request.url)
            redirect_parsed = requests.utils.urlparse(url)

            if (original_parsed.hostname != redirect_parsed.hostname) and redirect_parsed.hostname != self.AUTH_HOST and original_parsed.hostname != self.AUTH_HOST:
                del headers['Authorization']
 
        return 
# create session with the user credentials that will be used to authenticate access to the data
username = "rajpom"
password= "Yahoo99@go"
 
session = SessionWithHeaderRedirection(username, password)

# the url of the file we wish to retrieve
 
counter = 140;
for lst in data_list:
 
    filename =  "./data/windData/" + str(counter) + ".nc4"   
    try:
    
        # submit the request using the session
        response = session.get(lst, stream=True)
        print(str(response.status_code) + " File name: " + filename)
    
        # raise an exception in case of http errors
        response.raise_for_status()  
        # save the file
    
        with open(filename, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=1024*1024):
                fd.write(chunk)
        counter += 1
    except requests.exceptions.HTTPError as e:
    
        # handle any errors here
        print(e)