from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from . import search_engine
import time

def home(request):
    context = {
            'links' : list()
        }
    
    if request.method == "POST":
        x = time.time()
        query = request.POST.get("search-query")   

        # query = "College of Pharmacy"

        links = search_engine.return_links(query)
        num_links = len(links)
        y = time.time()
        time_taken = y-x
        context = {
            'links' : links,
            'num_links' : num_links,
            'time_taken': round(time_taken,3),
            'query':query
        }
    return render(request, "webcrawler/home.html", context)

def contact(request):

    return render(request, "webcrawler/contact.html")