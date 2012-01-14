##############
django-janrain
##############

Janrain integration into Django using built-in django.contrib.auth package. It
creates a django user using django.contrib.auth.models.User on first login and
retrieves that User object on future logins.

This is a fork of the very useful django-janrain app (https://github.com/spuriousdata/django-janrain), 
but I decided to add built-in templates and models so that it works out of the box.

In practice, you should consider tweaking it to meet your specific user registration needs.

============
Installation
============

Place the ``janrain`` directory in your project directory

Add a url entry in ``urls.py``::

	urlpatterns += patterns('',
		(r'^janrain/', include('janrain.urls')),
	)

Add ``janrain`` to your ``INSTALLED_APPS``::

	INSTALLED_APPS = (
		'django.contrib.admin',
		'django.contrib.auth',
		'django.contrib.contenttypes',
		'django.contrib.sessions',
		'janrain',
	)

Add ``janrain.backends.JanrainBackend`` to ``AUTHENTICATION_BACKENDS``::

	# put janrain.backends.JanrainBackend first
	AUTHENTICATION_BACKENDS = (
		'janrain.backends.JanrainBackend',
		'django.contrib.auth.backends.ModelBackend',
	)

Add your janrain api key to ``settings``::

	JANRAIN_RPX_API_KEY = "0123456789abcdef0123456789abcdef0123456789abcdef"
	
Add your janrain domain to ``settings``::

    JANRAIN_DOMAIN = "yoursite.rpxnow.com"



=====
Usage
=====

Visit the login page at ``/janrain/login/`` to login

Visit ``/janrain/logout/`` to log out.

You will probably need to tweak the code to meet your needs, but this should get you started.
