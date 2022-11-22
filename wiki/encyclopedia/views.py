from django.shortcuts import render
import markdown2
from django import forms

from . import util

def convertMd(title):
    md = util.get_entry(title)
    if md == None:
        return None
    info = markdown2.markdown(md)
    return info

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    info = convertMd(title)
    if info == None:
        return render(request, "encyclopedia/error.html")

    return render(request, "encyclopedia/entry.html", {
        "info": info,
        "title": title
    })

def search(request):
    if request.method == "POST":
        search = request.POST['q']
        entry = convertMd(search)
        if entry is not None:
            return render(request, "encyclopedia/entry.html", {
                "info": entry,
                "title": search
            })
        else:
            listOfEntries = util.list_entries()
            listOfSimilars = []
            for data in listOfEntries:
                if search.upper() in data.upper():
                    listOfSimilars.append(data)
            return render(request, "encyclopedia/search.html", {
                "similars":listOfSimilars
            })