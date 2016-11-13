from django.http import JsonResponse
from django.shortcuts import render

from .forms import IsitupForm, TTCForm

from isitup.main import check

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

			response = check(text)

			return JsonResponse({'text': response})

	return JsonResponse({'slack-commands': ['isitup']})
