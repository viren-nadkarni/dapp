from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import PlayApp


def search(requests): 
    template = loader.get_template('search.html')
    return HttpResponse(template.render(template))


def results(requests): 
    template = loader.get_template('results.html')
    if requests.method == 'GET':
        search_term = requests.GET.get('search_term')

    # search database for the term
    try:
        output = PlayApp.objects.get(app_name__contains=search_term)
    except:
        # else web scrape
        pass
        # and cache in db

    return HttpResponse(output)


def app(requests, entry_name): 
    output = entry_name
    return HttpResponse(output)

