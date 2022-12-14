from django.shortcuts import render
import markdown2
import random

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
        return render(request, "encyclopedia/error.html", {
            'message': "This entry doesn't exist"
        })

    return render(request, "encyclopedia/entry.html", {
        "info": info,
        "title": title,
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

def new_entry(request):
    if request.method == "POST":
        title = request.POST['title']
        entry = convertMd(title)
        desc = request.POST['info']

        if title is "":
            return render(request, 'encyclopedia/error.html', {
                'message': "The Title is empty",
            })

        if desc is "":
            return render(request, 'encyclopedia/error.html', {
                'message': "The Content is empty",
            })


        if entry is not None:
            return render(request, 'encyclopedia/error.html', {
                'message': "The Title already exists",
            })
        else:
            util.save_entry(title, desc)
            entry = convertMd(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "info": entry,
            })

    return render(request, "encyclopedia/new_entry.html", {})

def edit_entry(request):
    if request.method == "POST":
        title = request.POST['title']
        edit = request.POST['edit']
        desc = request.POST['info']
        md = util.get_entry(title)
        if edit == "si":
            return render(request, 'encyclopedia/edit_entry.html', {
                "title": title,
                "info": md,
            })
             
        if title is "":
            return render(request, 'encyclopedia/error.html', {
                'message': "The Title is empty",
            })

        if desc is "":
            return render(request, 'encyclopedia/error.html', {
                'message': "The Content is empty",
            })

        util.save_entry(title, desc)
        info = convertMd(title)
        return render(request, "encyclopedia/entry.html", {
            "info": info,
            "title": title,
        })

def rand(request):
    entries = util.list_entries()
    title = random.choice(entries)
    info = convertMd(title)
    return render(request, "encyclopedia/entry.html", {
            "info": info,
            "title": title,
        })
