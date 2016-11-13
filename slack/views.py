from django.http import JsonResponse
from django.shortcuts import render

from .forms import IsitupForm, TTCForm

from isitup.main import check
import requests

def check_isitup(request):
	if request.method == 'POST':
		form = IsitupForm(request.POST)
		if form.is_valid():
			text = form.cleaned_data['text']

			response = check(text)

			return JsonResponse({'text': response})

	return JsonResponse({'slack-commands': ['isitup']})


def check_ttc(request):
	if request.method == 'POST':
		form = TTCForm(request.POST)
		if form.is_valid():
			text = form.cleaned_data['text']

			# r = requests.get('http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=ttc&r=%s' % text)
			url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=ttc&r=' + text
			headers = { 'Accept-Encoding': 'gzip, deflate', }
			r = requests.get(url, headers = headers)

			return JsonResponse({'text': t.text})

	return JsonResponse({'slack-commands': ['ttc']})
