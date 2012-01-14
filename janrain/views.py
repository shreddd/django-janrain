from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from janrain.backends import JanrainBackend

import urllib, urllib2, json
from urllib import unquote

@csrf_exempt
def login(request):
    try:
        token = request.POST['token']
    except KeyError:
        # TODO: set ERROR to something
        return HttpResponseRedirect('/')

    api_params = {
        'token': token,
        'apiKey': settings.JANRAIN_RPX_API_KEY,
        'format': 'json',
    }

    janrain_domain = settings.JANRAIN_DOMAIN
    janrain_response = urllib2.urlopen(
            "https://rpxnow.com/api/v2/auth_info",
            urllib.urlencode(api_params))
    resp_json = janrain_response.read()
    auth_info = json.loads(resp_json)
    u = None
    if auth_info['stat'] == 'ok':
        profile = auth_info['profile']
        u = auth.authenticate(profile=profile)

    if u is not None:
        request.user = u
        auth.login(request, u)
    else:
        # Auth failure
        jb=JanrainBackend()
        errmsg=''
        if jb.get_email(profile)=='':
            errmesg="Your identity did not include email information. Please make sure your email is registered with your ID provider."
        elif jb.get_provider(profile)=='':
            errmesg="You did not use a valid identity provider. Please try again with a different provider."
        else:
            errmesg="Miscellaneous Failure."            
        msg='Authentication Failure: %s'%errmesg
        messages.add_message(request, messages.ERROR, msg)
        
    try:
        return HttpResponseRedirect(request.GET['redirect_to'])
    except KeyError:
        return HttpResponseRedirect('/')

def logout(request):
    auth.logout(request)
    try:
        return HttpResponseRedirect(request.GET['redirect_to'])
    except KeyError:
        return HttpResponseRedirect('/')

def loginpage(request):
    next=unquote(request.GET.get('next', '/'))
    next='/registration?next='+next
    
    hostname=request.META.get('HTTP_HOST', None)
    
    return render_to_response(
        'janrain/templates/loginpage.html',
        locals(),
        context_instance=RequestContext(request)
    )
    
