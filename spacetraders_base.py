#======================================================================================
# Usage notes:
#  You'll need to have Python 3 installed as well as the following libraries:
#   requests
#   json
#   
#  You'll need pip to be installed so that you have manage your libraries.
#  install pip (MacOS)
#  brew install pip
#
#  install pip (Windows)
#  Go to https://www.python.org/downloads/
#   download the latest version. Double click on it once it's downloaded to start the install
#   Check the box that says "Add Python X.X to PATH".
#  Once the install is complete open a command line and run the following commands to verify the install:
#   python --version
#   pip --version
#
#  Once the install is verified use the following commands to install the needed libraries:
#   pip install requests
#   pip install json
#======================================================================================

import argparse
import requests
import json

# Define the base URL of the RESTful API
BASE_URL      = "https://api.spacetraders.io"
API_VERSION   = "/v2"
API_ACTION    = "/register"
CONTENT_TYPE  = {"Content-Type" : "application/json"}

# list of tokens for Agents
AGENTS = { 
    "RPGACE1968": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiUlBHQUNFMTk2OCIsInZlcnNpb24iOiJ2Mi4xLjUiLCJyZXNldF9kYXRlIjoiMjAyNC0wMi0yNSIsImlhdCI6MTcwODkwODkyNCwic3ViIjoiYWdlbnQtdG9rZW4ifQ.Cy7mzFYhy_2fI-il54RgsHV1PR0PXGVYhQf_EEdGYF5VBWnx1iYS3PXSCR6xI3B9lW9Ee4k5vVMYVtWNGCPCr52OOun3JhGz-8kjJNo9yNq_tw8L9RakQi7T-eOGxSs5i5cuKHPbiZ0CMPKhxfRkqCFzxHEAgizSYAzArvf_qpeBWLrTRMKt4bjB0b456ViVpftD4TlmDo9NjXXBWZacTfvFHY9MQXWOhvub57nVCrGWCXBHjH2aNcq0kF-H8jBRKJXWxt8XWysjcV8imzEZQXSLex4RK0jNWwxDlwNzwxdXTonxcic9CpCYCvkL-ZorN9odImy3SJX2AVc591wDiw",
}


#====================================    
# Setup basic headers 
#====================================
def getBasicHeader(callsign):
    headers={ "Content-Type" : "application/json", "Authorization" : "Bearer "+AGENTS[callsign]}
    return headers

#====================================    
# Function to display beautified JSON
#====================================
def json_dumper(json_in):
    formatted_json = json.dumps(json_in, indent=4)
    print(formatted_json)

#====================================    
# Function to handle registration
#====================================
def register(params):
    faction, callsign = params
    print("faction: ",faction)
    print("callsign: ",callsign)
    # Make the API request for action one
    json_payload = { "symbol":callsign, "faction":faction}
    print(json_payload)
    response = requests.post(BASE_URL + API_VERSION + "/register", headers=CONTENT_TYPE, json=json_payload)
    # Process the response as needed
    json_dumper(response.json())
    print("IMPORTANT: Save the data above. You will not be able to easily retrieve it later.")

#====================================    
# Function to show agent info
#====================================
def show_agent(params):
    callsign = params[0]
    print("callsign: ", callsign)
    headers = getBasicHeader(callsign)
    # Make the API request for action two
    response = requests.get(BASE_URL + API_VERSION + "/my/agent", headers=headers)
    # Process the response as needed
    json_dumper(response.json())

#====================================    
# Function to view location
#====================================
def show_location(params):
    callsign, system, waypoint = params
    print("system: ", system)
    print("waypoint: ", waypoint)
    print("callsign: ", callsign)
    headers = getBasicHeader(callsign)
    # Make the API request for action two
    response = requests.get(BASE_URL + API_VERSION + "/systems/" + system + "/waypoints/" + waypoint, headers=headers)
    # Process the response as needed
    json_dumper(response.json())

#====================================    
# Function to view my contracts
#====================================
def show_contracts(params):
    callsign = params[0]
    print("callsign: ", callsign)
    headers = getBasicHeader(callsign)
    # Make the API request for action two
    response = requests.get(BASE_URL + API_VERSION + "/my/contracts", headers=headers)
    # Process the response as needed
    json_dumper(response.json())

#====================================    
# Function to accept a contract
#====================================
def accept_contract(params):
    callsign, contractId = params
    print("callsign: ", callsign)
    print("contractID: ", contractId)
    headers = getBasicHeader(callsign)
    # Make the API request for action two
    response = requests.post(BASE_URL + API_VERSION + "/my/contracts/" + contractId + "/accept", headers=headers)
    # Process the response as needed
    json_dumper(response.json())

#====================================    
# Function to find waypoints with various traits
#====================================
def show_location(params):
    callsign, system, traits = params
    print("system: ", system)
    print("traits: ", traits)
    print("callsign: ", callsign)
    headers = getBasicHeader(callsign)
    # Make the API request for action two
    response = requests.get(BASE_URL + API_VERSION + "/systems/" + system + "/waypoints?traits=" + traits, headers=headers)
    # Process the response as needed
    json_dumper(response.json())


#=====================================
# Mainline code
#=====================================
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Script to perform actions using a RESTful API")
    parser.add_argument("action", help="Action to perform")
    parser.add_argument("params", nargs=argparse.REMAINDER, help="Additional parameters")
    args = parser.parse_args()

    # Determine which action to perform
    action = args.action.lower()  # Convert action to lowercase for case-insensitive matching
    params = args.params
    
    # Switch/case structure to handle different actions
    if action == "register":
        register(params)

    elif action == "show_agent":
        show_agent(params)

    elif action == "location":
        show_location(params)

    elif action == "contracts":
        show_contracts(params)

    elif action == "accept_contract":
        accept_contract(params)

    else:
        print("Invalid action. Please specify a valid action.")

if __name__ == "__main__":
    main()