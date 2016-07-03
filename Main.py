# Program to consume data from SOAP WS and upload to PostgreSQL

import configparser
from zeep import Client

# Read the config file
config = configparser.ConfigParser()
config.read("Server.txt")
# config.read("Server_demo.txt")

# Set the variables
WSDL_URL = config.get("serverConfig", "WSDL_URL")
LOGIN    = config.get("serverConfig", "login")
PASSWORD = config.get("serverConfig", "password")



#wsdl = 'http://www.soapclient.com/xml/soapresponder.wsdl'
#client = Client(wsdl=wsdl)
#print(client.service.Method1('Zeep', 'is cool'))


# Run
client = Client(wsdl=WSDL_URL)
print(client.service.GetVehiculos(login=LOGIN, password=PASSWORD))



