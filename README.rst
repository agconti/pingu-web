pingu-web
==============================

Ping Pong like never before...

Dummy Account:

* Username: dummy
* Password: correct horse battery staple

http://xkcd.com/936/

LICENSE: BSD

Settings
------------

cookiecutter-django relies extensively on environment settings which **will not work with Apache/mod_wsgi setups**. It has been deployed successfully with both Gunicorn/Nginx and even uWSGI/Nginx.

For configuration purposes, the following table maps the cookiecutter-django environment variables to their Django setting:

======================================= =========================== ============================================== ===========================================
Environment Variable                    Django Setting              Development Default                            Production Default
======================================= =========================== ============================================== ===========================================
DJANGO_AWS_ACCESS_KEY_ID                AWS_ACCESS_KEY_ID           n/a                                            raises error
DJANGO_AWS_SECRET_ACCESS_KEY            AWS_SECRET_ACCESS_KEY       n/a                                            raises error
DJANGO_AWS_STORAGE_BUCKET_NAME          AWS_STORAGE_BUCKET_NAME     n/a                                            raises error
DJANGO_CACHES                           CACHES                      locmem                                         memcached
DJANGO_DATABASES                        DATABASES                   See code                                       See code
DJANGO_DEBUG                            DEBUG                       True                                           False
DJANGO_EMAIL_BACKEND                    EMAIL_BACKEND               django.core.mail.backends.console.EmailBackend django.core.mail.backends.smtp.EmailBackend
DJANGO_SECRET_KEY                       SECRET_KEY                  CHANGEME!!!                                    raises error
DJANGO_SECURE_BROWSER_XSS_FILTER        SECURE_BROWSER_XSS_FILTER   n/a                                            True
DJANGO_SECURE_SSL_REDIRECT              SECURE_SSL_REDIRECT         n/a                                            True
DJANGO_SECURE_CONTENT_TYPE_NOSNIFF      SECURE_CONTENT_TYPE_NOSNIFF n/a                                            True
DJANGO_SECURE_FRAME_DENY                SECURE_FRAME_DENY           n/a                                            True
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS   HSTS_INCLUDE_SUBDOMAINS     n/a                                            True
DJANGO_SESSION_COOKIE_HTTPONLY          SESSION_COOKIE_HTTPONLY     n/a                                            True
DJANGO_SESSION_COOKIE_SECURE            SESSION_COOKIE_SECURE       n/a                                            False
======================================= =========================== ============================================== ===========================================

* TODO: Add vendor-added settings in another table

Developer Installation
-----------------------

For getting this running on your local machine:

1. Set up a virtualenv.
2. Install all the supporting libraries into your virtualenv::

    pip install -r requirements/local.txt

3. Install Grunt Dependencies.

    npm install

4. Run development server. (For browser auto-reload, use Livereload_ plugins.)

    grunt serve

.. _livereload: https://github.com/gruntjs/grunt-contrib-watch#using-live-reload-with-the-browser-extension


Deployment
------------

Run these commands to deploy the project to Heroku:

.. code-block:: bash

    heroku create --buildpack https://github.com/heroku/heroku-buildpack-python
    git remote rename heroku staging
    heroku addons:add heroku-postgresql:dev --remote staging
    heroku addons:add pgbackups --remote staging
    heroku addons:add sendgrid:starter --remote staging
    heroku addons:add memcachier:dev --remote staging
    heroku pg:promote HEROKU_POSTGRESQL_COLOR --remote staging
    heroku config:set DJANGO_CONFIGURATION=Production --remote staging
    heroku config:set DJANGO_SECRET_KEY="314i*8v^8t8m4pv*jpiy425_++(@b_&df^+uj5vs#+=_j" --remote staging
    heroku config:set DJANGO_AWS_ACCESS_KEY_ID=AKIAIDJBPN5KDPRBFFRQ --remote staging
    heroku config:set DJANGO_AWS_SECRET_ACCESS_KEY=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 --remote staging
    heroku config:set DJANGO_AWS_STORAGE_BUCKET_NAME=pingu-staging --remote staging
    git push staging master
    heroku run python pingu/manage.py syncdb --noinput --settings=config.settings --remote staging
    heroku run python pingu/manage.py migrate --settings=config.settings  --remote staging
    heroku run python pingu/manage.py collectstatic --settings=config.settings --remote staging
