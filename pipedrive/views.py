from rest_framework.parsers import JSONParser
import json
from django.http import JsonResponse
import requests
from rest_framework.decorators import api_view

@api_view(['POST'])
def addUpdatePerson(request):
    if request.method == 'POST':

        person = JSONParser().parse(request)	   

        params = '{"api_token": "0b1b318d194dc68914af0619d82a1fcca5dadc2d", "term": "' + person['email'][0]['value'] + '", "fields": "email", "exact_match": "true"}'
        jparams = json.loads(params)

        url = "https://empresa-teste.pipedrive.com/api/v1/persons/search"	

        headers = {"Accept": "application/json"}

        response = requests.get(url, params=jparams, headers=headers).json()        

        if (response['data'].get('items')):
            id = response['data']['items'][0]['item']['id']
            url = ("https://empresa-teste.pipedrive.com/api/v1/persons/" + (str(id)) + "?api_token=0b1b318d194dc68914af0619d82a1fcca5dadc2d")
            responseupdate = requests.put(url, json=person, headers=headers).json()        
            
            return JsonResponse({"response":"update person"},status=200)            
        else:

            url = "https://empresa-teste.pipedrive.com/api/v1/persons?api_token=0b1b318d194dc68914af0619d82a1fcca5dadc2d"	
            responseadd = requests.post(url, json=person, headers=headers).json()        
            return JsonResponse({"response":"add person"},status=201)