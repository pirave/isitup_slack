from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import IsitupForm, TTCForm
from .routes import routes

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

def _get_data(url):
    headers = { 'Accept-Encoding': 'gzip, deflate', }
    r = requests.get(url, headers=headers)
    return ET.fromstring(r.text)

def search_for_route_number(route_text):
    for key, value in routes.iteritems():
        if route_text.lower() in key.lower():
            return value

def handle_route(route_text):
    # search routes
    # if int, then just continue
    try:
        route_number = int(route_text)
    except ValueError:
        route_number = search_for_route_number(route_text)
        if not route_number:
            return 'No results found for ' + route_text

    url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=ttc&r=' + str(route_number)
    root = _get_data(url)

    def stringify_stop(stop):
        fmt_str = '[%s]: %s'
        fmt_args = (stop.attrib['stopId'], stop.attrib['title'])
        return fmt_str % fmt_args
    
    response = map(stringify_stop, root.findall('./route/stop/[@stopId]'))
    text = '\n'.join(response)

    return text

def handle_next(bus_stop_number):
    url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=ttc&stopId=' + bus_stop_number
    root = _get_data(url)

    def stringify_prediction(prediction):
        fmt_str = '[%s] %s minutes away'
        fmt_args = (prediction.attrib['branch'], prediction.attrib['minutes'])
        return fmt_str % fmt_args
    
    response = map(stringify_prediction, root.findall('./predictions/direction/prediction'))
    text = '\n'.join(response)

    return text

def handle_route_list():
    url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=ttc'
    root = _get_data(url)

    def stringify_route(route):
        fmt_str = '[%s]: %s'
        fmt_args = (route.attrib['tag'], route.attrib['title'].split('-')[1])
        return fmt_str % fmt_args
    
    response = map(stringify_route, root.findall('./route'))
    text = '\n'.join(response)

    return text

def handle_invalid_command(param):
    return 'u suck'

@csrf_exempt
def check_ttc(request):
    if request.method == 'POST':
        form = TTCForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']

            # todo parse text
            # ugh we have to split by space
            split = text.split(' ')
            command = split[0]
            params = split[1:]

            command_map = {
                'route': handle_route,
                'next': handle_next,
                'list': handle_route_list
            }
            func = command_map.get(command, handle_invalid_command)

            return JsonResponse({ 'text': func(*params) })

    return JsonResponse({'slack-commands': ['ttc']})
