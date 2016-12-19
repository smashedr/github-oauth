from django.shortcuts import render
import logging
import requests
from urllib.parse import parse_qs
from github_oauth.settings import config

logger = logging.getLogger(__name__)


def home(request):
    # View: /
    pgdata = {'client_id': config.get('GitHub', 'client_id')}
    return render(request, 'home.html', {
        'pgdata': pgdata,
    })


def callback(request):
    # View: /callback/
    pgdata = {'success': False}
    if 'code' in request.GET:
        code = request.GET['code']
        try:
            results = github_token(code)
            if 'access_token' in results:
                pgdata['gh'] = {
                    'token': results['access_token'],
                    'scope': results['scope'],
                }
                pgdata['success'] = True
            elif 'error_description' in results:
                pgdata['error'] = results['error_description']
            else:
                pgdata['error'] = 'Unable to parse GitHub response data.'
        except Exception as error:
            logger.exception(error)
            pgdata['error'] = error
    else:
        pgdata['error'] = 'Unable to parse code from query string.'

    return render(request, 'callback.html', {
        'pgdata': pgdata,
    })


def github_token(code):
    """
    Post OAuth code to GitHub and parse response data
    """
    uri = 'https://github.com/login/oauth/access_token'
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
