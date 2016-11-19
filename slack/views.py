from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import IsitupForm, TTCForm

from isitup.main import check
import requests
import xml.etree.ElementTree as ET

@csrf_exempt
def check_isitup(request):
	if request.method == 'POST':
		form = IsitupForm(request.POST)
		if form.is_valid():
			text = form.cleaned_data['text']

			response = check(text)

			return JsonResponse({'text': response})

	return JsonResponse({'slack-commands': ['isitup']})


@csrf_exempt
def check_ttc(request):
	if request.method == 'POST':
		form = TTCForm(request.POST)
		if form.is_valid():
			text = form.cleaned_data['text']

			url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=ttc&r=' + text
			headers = { 'Accept-Encoding': 'gzip, deflate', }
			r = requests.get(url, headers = headers)
                        root = ET.fromstring(r.text)

                        # import ipdb; ipdb.set_trace()
			response = map(lambda x: x.attrib['title'], root.findall('./route/stop/[@title]'))
                        text = '\n'.join(response)
			return JsonResponse({'text': text })


	return JsonResponse({'slack-commands': ['ttc']})
