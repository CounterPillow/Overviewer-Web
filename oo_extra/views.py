from models import Package, PackageModelForm, Build

from django.http import HttpResponse, Http404
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
import os

@csrf_exempt
def package_hook(request):
    if request.method == 'POST' and 'key' in request.GET and request.GET['key'] == settings.PACKAGE_HOOK_KEY:
        f = PackageModelForm(request.POST)
        f.save()
        return HttpResponse('<pre>Package Posted.</pre>\n')
    
    raise Http404

@csrf_exempt
def update(request):
    if request.method == 'POST' and 'payload' in request.POST and 'key' in request.GET and request.GET['key'] == settings.UPDATE_HOOK_KEY:
        data = request.POST['payload']
        data = json.loads(data)
        ref = data['ref']
        os.system("%s %s" % (settings.UPDATE_HOOK_COMMAND, ref))
        return HttpResponse('<pre>Hook Started</pre>\n')
        
    raise Http404

def build(request, bid, path):
    b = get_object_or_404(Build, pk=bid)
    b.downloads += 1
    b.save()
    
    response = HttpResponse()
    url = settings.ACCEL_BUILD_URL_PREFIX + b.path
    response['Content-Type'] = ""
    response['X-Accel-Redirect'] = url
    
    return response
