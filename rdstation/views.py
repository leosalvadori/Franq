from logging import raiseExceptions
from rest_framework import generics
from rest_framework.parsers import JSONParser
from .models import AuthModel
from .serializers import AuthSerializer, TokenRequestSerializer
from django.http import JsonResponse
import requests
from django.conf import settings
from rest_framework.decorators import api_view
from datetime import datetime, timedelta
import pytz

class AuthList(generics.ListAPIView):
	serializer_class = AuthSerializer	

	def get_queryset(self):	
		return AuthModel.objects.all()		

class TokenRequest:
    def __init__(self, refresh_token, client_id=None, client_secret=None):
        self.client_id = settings.RDSTATION_SETTINGS.get('client_id')
        self.client_secret = settings.RDSTATION_SETTINGS.get('client_secret')
        self.refresh_token = refresh_token

#@api_view(['POST'])
#def authupdatetoken(request):
def authupdatetoken():
	utc=pytz.UTC

	token = AuthModel.objects.get(pk=1)
	TokenDate = token.updated_at.replace(tzinfo=utc)+timedelta(seconds=token.expires_in)
	DateToday = datetime.now().replace(tzinfo=utc)

	if (TokenDate < DateToday):

		token_request = TokenRequestSerializer(TokenRequest(refresh_token=token.refresh_token))
		url = "https://api.rd.services/auth/token"	
		response = requests.request("POST", url, data=token_request.data)

		data = AuthSerializer(instance=token, data=response.json())

		if data.is_valid():
			data.save()
			return response['access_token']		
	else:
		return token.access_token

@api_view(['POST','DELETE'])
def addUpdateDeleteContact(request):
	if request.method == 'POST':
		token = authupdatetoken()

		mail = request.GET.get('email')
		contact = JSONParser().parse(request)			

		url = ('https://api.rd.services/platform/contacts/email:' + mail)

		headers = {
			"Accept": "application/json",
			"Content-Type": "application/json",
			"Authorization": ("Bearer " + token)
		}
		response = requests.patch(url, json=contact, headers=headers)			
		return JsonResponse({"response":"update/create contact"},status=200)        

	if request.method == 'DELETE':
		token = authupdatetoken()

		mail = request.GET.get('email')

		url = ('https://api.rd.services/platform/contacts/email:' + mail)

		headers = {
			"Accept": "application/json",
			"Content-Type": "application/json",
			"Authorization": ("Bearer " + token)
		}
				
		response = requests.delete(url, headers=headers)			
		return JsonResponse({"response":"deleted contact"},status=200) 
