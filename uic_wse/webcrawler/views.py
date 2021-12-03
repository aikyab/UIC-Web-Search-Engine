from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from . import search_engine

def home(request):
    context = {
            'links' : list()
        }

    if request.method == "POST":
        query = request.POST.get("search-query")    
        # query = "College of Pharmacy"

        links = search_engine.return_links(query)

        context = {
            'links' : links
        }
    return render(request, "webcrawler/home.html", context)

def contact(request):

    return render(request, "webcrawler/contact.html")