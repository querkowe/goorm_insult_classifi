from django.shortcuts import render
from django.http import Http404

import re
import pandas as pd

from .utils import scrape

# Create your views here.
def index(request):
    title = 'knaves'
    res = 'index page'
    return render(request, 'knave/index.html', {'title':title, 'content': res})

def test(request):

    return render(request, 'knave/test.html')

def search(request):
    # try:
    #     url = request.POST['url']
    #     print(url)
    #
    #     url_pattern = r'[^\/\=]+'
    #
    #     title = 'search'
    #     video = re.findall(url_pattern, url)[-1]
    #
    #     comments = scrape.get_comments(video)
    #     content = analysis.prepare_model(comments)
    #
    #     return render(request, 'knave/result.html', {'title': title, 'content': content})
    # except:
    #     return render(request, 'knave/result.html', {'title': 'Error', 'content': 'something goes wrong...'})
    text = request.POST.get('text')
    category = int(request.POST.get('category'))
    print(text)
    print(category)
    res = ""

    if category == 1:
        res = keyword(request, text)
    elif category == 2:
        res = channels(request, text)
    elif category == 3:
        url_pattern = r'[^\/\=]+'
        text = re.findall(url_pattern, text)[-1]
        res = video(request, text)

    return res

def channel(request, id):

    title = "channel"

    print(id)

    content = scrape.search_channel(id)

    return render(request, 'knave/channel.html', {'title': title, 'content': content})


def channels(request, query):

    title = "channels"

    print(query)

    content = scrape.channel_list(query)

    return render(request, 'knave/list.html', {'title': title, 'content': content})


def keyword(request, query):

    title = "keyword"

    print(query)

    content = scrape.search_text(query)

    return render(request, 'knave/keyword.html', {'title': title, 'content': content})


def video(request, id):

    title = "video"

    video = id

    print(video)

    content = scrape.preview_video(video)

    return render(request, 'knave/check.html', {'title': title, 'content': content})


def one_analysis(request, id):

    title = "videos"

    print(id)

    content = scrape.search_video(id)

    return render(request, 'knave/video.html', {'title': title, 'content': content})


def list_analysis(request):

    vids = request.POST.getlist('vid')

    title = "videos"

    print(vids)

    content = scrape.search_video_list(vids)

    return render(request, 'knave/result.html', {'title': title, 'content': content})
