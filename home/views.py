from django.shortcuts import render
import logging
import requests
from github_oauth.settings import config

logger = logging.getLogger(__name__)

PGDATA = {
    'github': {
        'base_url': config.get('GitHub', 'base_url'),
        'client_id': config.get('GitHub', 'client_id'),
    }
}


def home(request):
    # View: /
    return render(request, 'home.html', {
        'pgdata': PGDATA,
    })


def callback(request):
    # View: /callback/
    PGDATA['success'] = False
    if 'code' in request.GET:
        code = request.GET['code']
        try:
            results = github_token(code)
            if 'access_token' in results:
                PGDATA['gh_resp'] = {
                    'token': results['access_token'],
                    'scope': results['scope'],
                }
                PGDATA['success'] = True
            elif 'error_description' in results:
                PGDATA['error'] = results['error_description']
            else:
                PGDATA['error'] = 'Unable to parse GitHub response data.'
        except Exception as error:
            logger.exception(error)
            PGDATA['error'] = error
    else:
        PGDATA['error'] = 'Unable to parse code from query string.'

    return render(request, 'callback.html', {
        'pgdata': PGDATA,
    })


def github_token(code):
    """
    Post OAuth code to GitHub and parse response data
    """
    uri = '%s/login/oauth/access_token' % config.get('GitHub', 'base_url')
    data = {
        'client_id': config.get('GitHub', 'client_id'),
        'client_secret': config.get('GitHub', 'client_secret'),
        'code': code,
    }
    headers = {'Accept': 'application/json'}
    r = requests.post(uri, data=data, headers=headers)
    results = r.json()
    logger.info(results)
    return results
