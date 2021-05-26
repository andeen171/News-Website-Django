from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.conf import settings
from django.http.response import HttpResponseNotFound
from .forms import CreateNewsForm, SearchNewsForm
import datetime
import random
import json


# get the raw file; just to not rewrite it everytime
def GetRawFile():
    with open(settings.NEWS_JSON_PATH, 'r') as jason:
        return json.load(jason)


# Sort News by it created date
def SortNews(file):
    newsDict = {}
    for item in file:
        item['created'] = item['created'].split()[0]
    sorted_news = sorted(file, key=lambda i: i['created'], reverse=True)
    for item in sorted_news:
        if item['created'] not in newsDict:
            newsDict[item['created']] = [item]
        else:
            newsDict[item['created']].append(item)
    return newsDict


class MenuView(View):
    @staticmethod
    def get(request):
        form = SearchNewsForm(request.GET)
        rawFile = GetRawFile()
        if form.is_valid():
            processedFile = []
            q = form.cleaned_data['q']
            for i in rawFile:
                if q.lower() in i['title'].lower():
                    processedFile.append(i)
            newsDict = SortNews(processedFile)
            return render(request, 'menu.html', context={'news': newsDict, 'form': SearchNewsForm})
        else:
            newsDict = SortNews(rawFile)
            return render(request, 'menu.html', context={'news': newsDict, 'form': SearchNewsForm})


class NewsView(View):
    @staticmethod
    def get(request, **kwargs):
        index = int(kwargs['link'])
        data = GetRawFile()
        article = list(filter(lambda x: x['link'] == index, data))
        if not article:
            return HttpResponseNotFound('<h1>Page not found</h1>')
        return render(request, 'news.html', context={'article': article[0]})


class NoneView(View):
    @staticmethod
    def get(request):
        return HttpResponse("<h2> Coming soon </h2>")


class CreateView(View):
    @staticmethod
    def get(request):
        return render(request, 'create.html', context={'form': CreateNewsForm})

    @staticmethod
    def post(request):
        form = CreateNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            link = random.randint(3, 99999)
            obj = {'created': date, 'text': text, 'title': title, 'link': link}
            all = GetRawFile()
            with open(settings.NEWS_JSON_PATH, 'w') as jason:
                all.append(obj)
                json.dump(all, jason)
            return redirect('/news/')
        else:
            return redirect('/news/create/')
