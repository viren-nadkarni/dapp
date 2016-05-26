import sys
import requests
import lxml.html

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist

from .models import PlayApp

APP_SEARCH_URL = 'https://play.google.com/store/search?c=apps&q={}'
APP_DETAILS_URL = 'https://play.google.com/store/apps/details?id={}'


def get_app_details(app_id):
    """This function will check the db cache if the details about an app with given id exists.
    Otherwise, it will be fetched from playstore, and cached
    
    args:
        app_id -- java convention style id of the app
        
    returns:
        dict of app details
    """
    try:
        # check if the said app details are available in db
        # get it as a dict object
        output = PlayApp.objects.get(app_id__iexact=app_id).__dict__

        # the source field will indicate where the details have been pulled from
        output['source'] = 'cache'

    except ObjectDoesNotExist:
        # app details are not cached
        # so we scrape app info
        store_page = requests.get( APP_DETAILS_URL.format( app_id ) ).text
        tree = lxml.html.fromstring(store_page)

        # XPath might be susceptible to failure even if a change is made in page layout
        try:
            # create a dict object representing the app
            output = {
                'app_id': app_id,
                'app_name': tree.xpath('//div[@class="id-app-title"]/text()')[0],
                'dev_name': tree.xpath('//div[div[@class="title"] = "Offered By"]/div[@class="content"]/text()')[0],
                'icon_url': tree.xpath('//img[@class="cover-image"]/@src')[0],
                'source': 'web',
            }

            # some apps have details like Privacy Policy, Mailing address, some don't. Handle it here
            # no particular order is followed, 
            dev_email_value = tree.xpath('//a[@class="dev-link"]/@href')
            output['dev_email'] = [email for email in dev_email_value if 'mailto:' in email][0][7:]

            # and cache it in db
            PlayApp(app_id=output['app_id'],
                    app_name=output['app_name'],
                    dev_name=output['dev_name'],
                    dev_email=output['dev_email'],
                    icon_url=output['icon_url']).save()

        except IndexError:
            # exception when the app does not exist on play store
            print sys.exc_info()
            output = {
                'app_id': app_id,
                'app_name': 'Not found',
                'dev_name': 'Not found',
                'dev_email': '',
                'icon_url': '',
                'source': 'web',
            }

    return output



def search(request): 
    template = loader.get_template('search.html')
    return HttpResponse(template.render(template))


def results(request): 
    template = loader.get_template('results.html')
    search_term = request.GET.get('search_term')

    output = list()
    if search_term:
        # search results will always be fetched from play store
        # however, for app details, db cache will be checked first
        store_results_raw = requests.get( APP_SEARCH_URL.format(search_term) ).text
        tree = lxml.html.fromstring(store_results_raw)
        results = tree.xpath('//div[@class="card-content id-track-click id-track-impression"]/@data-docid')

        for app_id in results[:10]:
            output.append( get_app_details(app_id) )

    return HttpResponse( template.render( context={'search_results': output} ) )


def app(request, app_id): 
    template = loader.get_template('app.html')

    output = get_app_details(app_id)

    return HttpResponse( template.render( context={'app': output,
                                                   'request': request} ) )

