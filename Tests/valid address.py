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
    'postalcode': '51930',
    'locality': 'Horred',
    'response_format': 'json',
    'suggestions': '1',
    'api_key': '3bb5596dd455959defeb3cd2085c871e'
}

#print(data)
response = requests.post('https://valid.geposit.se/1.7/validate/address/se', data=data)
response.raise_for_status()
data = response.json()
print('data:')
print(data)
print('response:')
print(data.get('response'))
print('suggestions:')
#d.get('a', {'j': 'NA'})['j']
#d.get('a', {}).get('j', 'NA')

#print(data.get('response'),{'query': 'NA'})['query']
#d.get('a', {}).get('j')
print(data.get('response', {}).get('suggestions'))
print(data.get('response', {}).get('errors'))
print('=================')

if (int)(data['response']['is_valid']) == 1:
    print("Address was correct")
    #print(data)
else:
    print("Address was incorrect")

    print("Errors in address")
    print(data['response']['errors'])
    print(data)
    suggestions = (data['response']['suggestions'])
    #print(len(suggestions))
    suggest = suggestions[0]
    print(suggestions)
    print()
    print(suggest)
    print()
    hela_respons =(data['response'])
    print(hela_respons)
    street = suggest.get('street') + ' ' + suggest.get('street_number') + ' ' + suggest.get('extra_number') + ' ' + suggest.get('letter')
    postalcode = suggest.get('postalcode')
    localityx = suggest.get('locality')
    print(street)
    print(postalcode)
    print(localityx)

    #print(data['response']['street'])

    print("Suggestion(s) to use instead:")
    #print(data['response']['suggestions'])
    #'suggestions': [{'address_type': 'NC', 'street': 'Lindhult Höjden', 'street_number': '5', 'extra_number': '', 'letter': '', 'postalcode': '51990', 'locality': 'Horred', 'errors': {'302': 'Felaktigt postnummer'}}]
