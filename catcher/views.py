from .models import LogModel
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from .serializers import LogSerializer
import requests
import json
from rest_framework import generics
from rest_framework.decorators import api_view

class LogList(generics.ListAPIView):
	serializer_class = LogSerializer	

	def get_queryset(self):			
		wh = self.request.query_params.get('wh')
		if (wh == 'all'):
			return LogModel.objects.all()		
		else:
			return LogModel.objects.filter(typewh=wh)
		

@api_view(['POST'])
def rdstationWebhook(request):
	if request.method == 'POST':
	
		contact = JSONParser().parse(request)

		if (contact['leads'][0].get('email') != None):				

			#{"name":"Leonardo Salvadori","email":[{"value":"leonardosalvadori7@gmail.com","primary": true}],"phone":[{"value":"54 999920559","primary": true}]}
				
			custom_fields = (
			'"eee9f244086d43dcc73af2bfbe5acafee3824b0d": "' + contact['leads'][0]['custom_fields']['Endereço:'] + 
			'", "4f692966571437bbad998fc9562a610cfd550fd4": "' + contact['leads'][0]['city'] + 
			'", "2a42509630ead9be56958d382416decfdaff8663": "' + contact['leads'][0]['state'] + 
			'", "3919dd4c708996b1a92f260ab9b5158eb862a1ad": "' + contact['leads'][0]['custom_fields']['CPF/CNPJ:'] + 
			'", "4f002a7b50ef8856998131671b240013731f271b": "' + contact['leads'][0]['job_title'] + '"')

			person = '{"name":"' + contact['leads'][0]['name'] + '","email":[{"value":"' + contact['leads'][0]['email'] + '","primary": true}],"phone":[{"value":"' + contact['leads'][0]['personal_phone'] + '","primary": true}], ' + custom_fields + '}'
			person = json.loads(person)

			url = "http://127.0.0.1:8000/pipedrive/addUpdatePerson/"	

			headers = {"Accept": "application/json"}

			response = requests.post(url, headers=headers, json=person).json()

			log = LogModel(origin = 'rdstation > pipedrive', operation=response['response'], payload=person, typewh='rdstation')
			log.save()
			
			return JsonResponse(response,status=200)	
		else:
			log = LogModel(origin = 'rdstation > pipedrive - FAIL', operation='invalid json', payload=contact, typewh='rdstation')
			log.save()
			return JsonResponse({"response":"invalid json"},status=400)		
			

@api_view(['POST'])
def pipedriveWebhook(request):
	if request.method == 'POST':			

		contact = JSONParser().parse(request)

		if (contact['meta'].get('change_source') != None):

			if (contact['meta']['change_source'] == "app"):

				if (contact['meta']['action'] == 'deleted'):

					url = ('http://127.0.0.1:8000/rdstation/addUpdateDeleteContact/?email=' + contact['previous']['email'][0]['value'])	

					response = requests.delete(url).json()

					log = LogModel(origin = 'Deleted pipedrive', operation=response['response'], payload=contact['previous']['email'][0]['value'], typewh='pipedrive')
					log.save()

					return JsonResponse(response,status=200)					

				else:

					person = ('{"name": "' + contact['current']['name'] + '"' + 
					',"job_title": "' + contact['current']['4f002a7b50ef8856998131671b240013731f271b'] + '","personal_phone": "' + contact['current']['phone'][0]['value'] + 
					'","city": "' + contact['current']['4f692966571437bbad998fc9562a610cfd550fd4'] + '","state": "' + contact['current']['2a42509630ead9be56958d382416decfdaff8663'] +'"}')
					person = json.loads(person)

					url = ('http://127.0.0.1:8000/rdstation/addUpdateDeleteContact/?email=' + contact['current']['email'][0]['value'])	
					headers = {"Accept": "application/json"}

					response = requests.post(url, headers=headers, json=person).json()

					log = LogModel(origin = 'pipedrive > rdstation', operation=response['response'], payload=person, typewh='pipedrive')
					log.save()

					return JsonResponse(response,status=200)		
		else:
			log = LogModel(origin = 'pipedrive > rdstation - FAIL', operation='invalid json', payload=contact, typewh='pipedrive')
			log.save()
			return JsonResponse({"response":"invalid json"},status=400)		