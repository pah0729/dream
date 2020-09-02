from django.contrib.sites.models import Site
'''
all tempaltes return property
'''

def config(request):
    return {
        "site": Site.objects.get_current()
    }
