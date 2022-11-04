from django.shortcuts import render
from django.http import Http404

import re

from .utils import analysis, scrape

# Create your views here.
def index(request):
    title = 'knaves'
    res = 'index page'
    return render(request, 'knave/index.html', {'title':title, 'content': res})

def search(request):
    try:
        url = request.POST['url']
        print(url)

        url_pattern = r'[^\/\=]+'

        title = 'search'
        video = re.findall(url_pattern, url)[-1]

        comments = scrape.get_comments(video)
        content = analysis.prepare_model(comments)

        return render(request, 'knave/result.html', {'title': title, 'content': content})
    except:
        return render(request, 'knave/result.html', {'title': 'Error', 'content': 'something goes wrong...'})
    # url = request.POST['url']
    # print(url)
    #
    # url_pattern = r'[^\/\=]+'
    #
    # title = 'search'
    # video = re.findall(url_pattern, url)[-1]
    #
    # comments = scrape.get_comments(video)
    # content = analysis.prepare_model(comments)
    #
    # return render(request, 'knave/result.html', {'title': title, 'content': content})
