from django.shortcuts import render
import markdown2

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

