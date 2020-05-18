import requests
'''
data = {
    'street': 'Drottninggatan 45',
    'postalcode': '11121',
    'locality': 'Stockholm',
    'response_format': 'json',
    'api_key': '3bb5596dd455959defeb3cd2085c871e'
}
'''
data = {
    'street': 'Lindhult Höjden 5',
    'postalcode': '51990',
    'locality': 'Horred',
    'response_format': 'json',
    'api_key': '3bb5596dd455959defeb3cd2085c871e'
}

{'street': 'Vassevägen 11', 'postalcode': '51930', 'locality': 'Horred', 'response_format': 'json', 'api_key': '3bb5596dd455959defeb3cd2085c871e'}


print(data)
response = requests.post('https://valid.geposit.se/1.7/validate/address/se', data=data)
response.raise_for_status()
data = response.json()

if((int)(data['response']['is_valid']) == 1):
    print("Address was correct")
    #print(data)
else:
    print("Address was incorrect")

    print("Errors in address")
    print(data['response']['errors'])

    print("Suggestion(s) to use instead:")
    print(data['response']['suggestions'])
