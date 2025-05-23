
from django.http import HttpResponse

# @api_view(["GET"])
def root(request):
    return HttpResponse("<small>CMS Api Response System</small>")

