# Django GitHub OAuth

GitHub OAuth Server in Django

https://developer.github.com/enterprise/2.8/v3/oauth/

#### Python 3

This project was built using Python 3.

#### Python 2

Notes for running under Python 2:

- Add `configparser` to the `requirements.txt`.
    - Or run `pip install configparser` manually.
- Use `virtualenv` instead of `venv`.

## Quick Deployment

1. `cd` into deploy directory
2. `git clone https://git.cssnr.com/shane/github-oauth.git .`
3. `pyvenv venv`
4. `source venv/bin/activate`
5. `pip install -r requirements.txt`
6. `cp settings.ini.example settings.ini`
7. Edit the settings to your preference.
8. `python manage.py runserver 0.0.0.0:8000`
