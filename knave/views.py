from django.shortcuts import render, redirect
from django.http import Http404

import re
import pandas as pd

from .utils import scrape

# Create your views here.

# 함수는 기본적으로 페이지 제목(title)과 내용(content)을 반환, 기능에 따라 다른 값 추가

# 메인 페이지
def index(request):
    title = 'knaves'
    res = 'index page'
    return render(request, 'knave/index.html', {'title':title, 'content': res})

# 프론트엔드 테스트
def test(request):

    return render(request, 'knave/test.html')

# 에러 페이지 렌더링
def error(request, exception='검색 결과가 없습니다'):
    return render(request, 'knave/error.html', {'title': 'Error', 'content': exception})

# 카테고리와 키워드를 받아 해당하는 결과 반환
# category 1 키워드 관련 영상 정보
# category 2 키워드 관련 채녈 목록
# category 3 영상 주소 또는 id 를 통한 영상 분석
def search(request):
    res = ""
    try:
        text = request.POST.get('text')
        if len(text) == 0:
            return redirect('/error/')
        category = int(request.POST.get('category'))
        print(text)
        print(category)

        if category == 1:
            res = keyword(request, text)
        elif category == 2:
            res = channels(request, text)
        elif category == 3:
            url_pattern = r'[^\/\=]+'
            text = re.findall(url_pattern, text)[-1]

            title = "videos"

            content = scrape.search_video(text)

            if len(content) == 0:
                return redirect('/error/')

            res = render(request, 'knave/video.html', {'title': title, 'content': content})
    except:
        return redirect('/error/')

    return res

# 키워드를 받아 채널 정보의 목록 반환
def channel(request, id):

    title = "channel"

    print(id)

    content = scrape.search_channel(id)

    if len(content) == 0:
        return redirect('/error/')

    input_text = content[0][5]

    return render(request, 'knave/channel.html', {'title': title, 'content': content, 'input_text': input_text})

# 채널 id를 받아 영상 id의 목록 반환
def channels(request, query):

    title = "channels"

    print(query)

    content = scrape.channel_list(query)

    if len(content) == 0:
        return redirect('/error/')

    return render(request, 'knave/list.html', {'title': title, 'content': content, 'input_text': query})

# 키워드를 받아 영상 id의 목록 반환
def keyword(request, query):

    title = "keyword"

    print(query)

    content = scrape.search_text(query)

    if len(content) == 0:
        return redirect('/error/')

    return render(request, 'knave/keyword.html', {'title': title, 'content': content, 'input_text': query})

# 영상 id를 받아 영상정보 반환
def video(request, id):

    title = "video"

    video = id

    print(video)

    content = scrape.preview_video(video)

    if len(content) == 0:
        return redirect('/error/')

    return render(request, 'knave/check.html', {'title': title, 'content': content})

# 영상 id의 목록을 받아 영상정보와 분석결과 반환
def list_analysis(request):

    input_text = request.POST.get('input_text')

    vids = request.POST.getlist('vid')

    title = "videos"

    print(vids)

    content, sum_good, sum_bad = scrape.search_video_list(vids)

    if len(content) == 0:
        return redirect('/error/')

    return render(request, 'knave/result.html', {'title': title, 'content': content, 'input_text': input_text, 'sum_good': sum_good, 'sum_bad': sum_bad})
