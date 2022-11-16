from django.shortcuts import render, redirect
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

def error(request):
    return render(request, 'knave/error.html', {'title': 'Error', 'content': '검색결과가 없습니다'})

def search(request):
    text = request.POST.get('text')
    if len(text) == 0:
        return redirect('/error/')
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

    if len(content) == 0:
        return redirect('/error/')

    input_text = content[0][5]

    return render(request, 'knave/channel.html', {'title': title, 'content': content, 'input_text': input_text})


def channels(request, query):

    title = "channels"

    print(query)

    content = scrape.channel_list(query)

    if len(content) == 0:
        return redirect('/error/')

    return render(request, 'knave/list.html', {'title': title, 'content': content, 'input_text': query})


def keyword(request, query):

    title = "keyword"

    print(query)

    content = scrape.search_text(query)

    if len(content) == 0:
        return redirect('/error/')

    return render(request, 'knave/keyword.html', {'title': title, 'content': content, 'input_text': query})


def video(request, id):

    title = "video"

    video = id

    print(video)

    content = scrape.preview_video(video)

    if len(content) == 0:
        return redirect('/error/')

    return render(request, 'knave/check.html', {'title': title, 'content': content})


def one_analysis(request, id):

    title = "videos"

    print(id)

    content = scrape.search_video(id)

    if len(content) == 0:
        return redirect('/error/')

    return render(request, 'knave/video.html', {'title': title, 'content': content})


def list_analysis(request):

    input_text = request.POST.get('input_text')

    vids = request.POST.getlist('vid')

    title = "videos"

    print(vids)

    content, sum_good, sum_bad = scrape.search_video_list(vids)

    if len(content) == 0:
        return redirect('/error/')

    return render(request, 'knave/result.html', {'title': title, 'content': content, 'input_text': input_text, 'sum_good': sum_good, 'sum_bad': sum_bad})
