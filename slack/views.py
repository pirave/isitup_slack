from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import IsitupForm

from isitup.main import check

@csrf_exempt
def check_isitup(request):
	if request.method == 'POST':
		form = IsitupForm(request.POST)
		if form.is_valid():
			text = form.cleaned_data['text']

			response = check(text)

			return JsonResponse({'text': response})

	return JsonResponse({'slack-commands': ['isitup']})
