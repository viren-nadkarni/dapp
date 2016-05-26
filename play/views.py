import requests
import lxml.html

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist

from .models import PlayApp

APP_SEARCH_URL = 'https://play.google.com/store/search?c=apps&q={}'
APP_DETAILS_URL = 'https://play.google.com/store/apps/details?id={}'


def search(request): 
    template = loader.get_template('search.html')
    return HttpResponse(template.render(template))


def results(request): 
    template = loader.get_template('results.html')
    if request.method == 'GET':
        search_term = request.GET.get('search_term')

    # search database for the term
    try:
        output = PlayApp.objects.filter(app_name__contains=search_term)
    except:
        # else web scrape
        pass

    return HttpResponse( template.render( context={'search_results': output} ) )


def app(request, app_id): 
    template = loader.get_template('app.html')

    try:
        # check if the said app details are available in db
        output = PlayApp.objects.get(app_id__iexact=app_id)

        # the source field will indicate where the details have been pulled from
        source = 'cache'

    except ObjectDoesNotExist:
        # app details are not cached
        # so we scrape app info
        store_page = requests.get( APP_DETAILS_URL.format( app_id ) ).text
        tree = lxml.html.fromstring(store_page)
        source = 'web'

        # the XPath has been copied from the browser inspection mode
        # susceptible to failure even if a small change is made in page layout
        try:
            output = {
                'app_id': app_id,
                'app_name': tree.xpath('//*[@id="body-content"]/div/div/div[1]/div[1]/div/div[1]/div[2]/div[1]/div/text()')[0],
                'dev_name': tree.xpath('//*[@id="body-content"]/div/div/div[1]/div[3]/div/div[2]/div[8]/div[2]/text()')[0],
                'dev_email': tree.xpath('//*[@id="body-content"]/div/div/div[1]/div[3]/div/div[2]/div[9]/div[2]/a[2]/@href')[0],
                'icon_url': tree.xpath('//*[@id="body-content"]/div/div/div[1]/div[1]/div/div[1]/div[1]/img/@src')[0],
            }

            # and cache it in db
            PlayApp(app_id=output['app_id'],
                    app_name=output['app_name'],
                    dev_name=output['dev_name'],
                    dev_email=output['dev_email'],
                    icon_url=output['icon_url']).save()

        except IndexError:
            # exception when the app does not exist on play store
            output = {
                'app_id': app_id,
                'app_name': 'Not found',
                'dev_name': 'Not found',
                'dev_email': '',
                'icon_url': '',
            }

    return HttpResponse( template.render( context={'app': output,
                                                   'source': source,
                                                   'request': request} ) )

