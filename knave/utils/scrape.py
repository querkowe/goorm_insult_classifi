from googleapiclient.discovery import build
from oauth2client.tools import argparser
from django.conf import settings
import pandas as pd
from datetime import datetime

from . import analysis

# 유튜브의 ISO 8601 형식의 날짜 문자열 면#
def date_parse(src):
    dt = datetime.fromisoformat(src[:-1])
    return dt.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")

def get_comments(video):

    # print(video)

    #사용자 계정 api_key
    api_key = settings.API_KEY

    # 비디오 주소 맨 뒤쪽에 있음
    video_id = video

    # 영상 하나당 최대 댓글 갯수 -> 시간 관계상 제
    limit = 100

    comments = list()
    api_obj = settings.YOUTUBE_OBJ
    good_count = 0
    bad_count = 0
    response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, maxResults=100).execute()

    if response and len(comments) < limit:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']

            comments.append([comment['textDisplay'], date_parse(comment['publishedAt']), comment['likeCount']])

            result = analysis.predict_sent(comments[-1][0])

            if result == 0:
                result = " 악성 👿"
                bad_count += 1
            elif result == 1:
                result = " 정상 😀"
                good_count += 1

            comments[-1].append(result)

    return good_count, bad_count, pd.DataFrame(comments, columns=['댓글 내용', '게시일', '좋아요', '판별 결과']).to_html(classes='table table-dark', index=False).strip()


# 키워드를 통한 영상 목록 검색
def search_text(text):
    query_text = text
    max_results = 10
    youtube = settings.YOUTUBE_OBJ

    search_response = youtube.search().list(
        q=query_text,
        order="relevance",
        part="snippet",
        type='video',
        maxResults=max_results,
        # videoEmbeddable=true,
        regionCode="kr",
        relevanceLanguage="ko"
    ).execute()

    videos = []

    for i in range(len(search_response['items'])):

        videos.append(
            [
                search_response['items'][i]['id']['videoId'].strip(),
                search_response['items'][i]['snippet']['title'].strip(),
                search_response['items'][i]['snippet']['description'].strip(),
                search_response['items'][i]['snippet']['thumbnails']['high']['url'].strip(),
                search_response['items'][i]['snippet']['channelId'].strip(),
                search_response['items'][i]['snippet']['channelTitle'].strip(),
                date_parse(search_response['items'][i]['snippet']['publishedAt'].strip()),
                # search_response['items'][i]['snippet']['publishedAt'].strip(),
            ]
        )

    return videos

# 키워드를 통한 채널 리스트 검색
def channel_list(text):
    query_text = text
    max_results = 10
    youtube = settings.YOUTUBE_OBJ

    search_response = youtube.search().list(
        q=query_text,
        order="relevance",
        part="snippet",
        type='channel',
        maxResults=max_results,
        # videoEmbeddable=true,
        regionCode="kr",
        relevanceLanguage="ko"
    ).execute()

    channels = []

    for i in range(len(search_response['items'])):

        channels.append(
            [
                search_response['items'][i]['snippet']['title'].strip(),
                search_response['items'][i]['snippet']['description'].strip(),
                search_response['items'][i]['snippet']['thumbnails']['high']['url'].strip(),
                search_response['items'][i]['snippet']['channelId'].strip(),
                # search_response['items'][i]['snippet']['channelTitle'],
                date_parse(search_response['items'][i]['snippet']['publishedAt'].strip()),
                # search_response['items'][i]['snippet']['publishedAt'].strip(),
            ]
        )

    return channels

# 영상 id 리스트를 통한 영상 정보 검색 및 분석
def search_video_list(vids):
    max_results = 10
    youtube = settings.YOUTUBE_OBJ

    videos = []
    sum_good= 0
    sum_bad = 0

    for vid in vids:
        search_response = youtube.videos().list(
            id=vid,
            part="id,snippet,statistics",
            maxResults=max_results,
            # videoEmbeddable=true,
            # regionCode="kr",
            # relevanceLanguage="ko"
        ).execute()

        good_count, bad_count, comments_df = get_comments(search_response['items'][0]['id'])

        sum_good += good_count
        sum_bad += bad_count

        videos.append(
            [
                search_response['items'][0]['id'].strip(),
                search_response['items'][0]['snippet']['title'].strip(),
                search_response['items'][0]['snippet']['description'].strip(),
                search_response['items'][0]['snippet']['thumbnails']['high']['url'].strip(),
                search_response['items'][0]['snippet']['channelId'].strip(),
                search_response['items'][0]['snippet']['channelTitle'].strip(),
                date_parse(search_response['items'][0]['snippet']['publishedAt'].strip()),
                # search_response['items'][0]['snippet']['publishedAt'].strip(),
                search_response['items'][0]['statistics']['viewCount'].strip(),
                search_response['items'][0]['statistics']['likeCount'].strip(),
                search_response['items'][0]['statistics']['favoriteCount'].strip(),
                search_response['items'][0]['statistics']['commentCount'].strip(),
                good_count,
                bad_count,
                comments_df
            ]
        )

    return videos, sum_good, sum_bad

# 키워드를 통한 채널 검색
def search_channel(channel):
    query_text = channel
    max_results = 10
    youtube = settings.YOUTUBE_OBJ

    search_response = youtube.search().list(
        channelId=channel,
        order="relevance",
        part="snippet",
        type='video',
        maxResults=max_results,
        # videoEmbeddable=true,
        regionCode="kr",
        relevanceLanguage="ko"
    ).execute()

    videos = []

    for i in range(len(search_response['items'])):

        videos.append(
            [
                search_response['items'][i]['id']['videoId'].strip(),
                search_response['items'][i]['snippet']['title'].strip(),
                search_response['items'][i]['snippet']['description'].strip(),
                search_response['items'][i]['snippet']['thumbnails']['high']['url'].strip(),
                search_response['items'][i]['snippet']['channelId'].strip(),
                search_response['items'][i]['snippet']['channelTitle'].strip(),
                date_parse(search_response['items'][i]['snippet']['publishedAt'].strip())
                # search_response['items'][i]['snippet']['publishedAt'].strip()
            ]
        )

    return videos

# 단일 영상 정보 검색 및 분석
def search_video(id):
    query_text = id
    youtube = settings.YOUTUBE_OBJ

    search_response = youtube.videos().list(
        id=query_text,
        part="id,snippet,statistics",
        # videoEmbeddable=true,
        # regionCode="kr",
        # relevanceLanguage="ko"
    ).execute()

    videos = []

    for i in range(len(search_response['items'])):

        good_count, bad_count, comments_df = get_comments(search_response['items'][i]['id'])

        videos.append(
            [
                search_response['items'][i]['id'],
                search_response['items'][i]['snippet']['title'].strip(),
                search_response['items'][i]['snippet']['description'].strip(),
                search_response['items'][i]['snippet']['thumbnails']['high']['url'].strip(),
                search_response['items'][i]['snippet']['channelId'].strip(),
                search_response['items'][i]['snippet']['channelTitle'].strip(),
                date_parse(search_response['items'][i]['snippet']['publishedAt'].strip()),
                # search_response['items'][i]['snippet']['publishedAt'].strip(),
                search_response['items'][i]['statistics']['viewCount'].strip(),
                search_response['items'][i]['statistics']['likeCount'].strip(),
                search_response['items'][i]['statistics']['favoriteCount'].strip(),
                search_response['items'][i]['statistics']['commentCount'].strip(),
                good_count,
                bad_count,
                comments_df
            ]
        )

    return videos

# 영상 정보 검색
def preview_video(id):
    query_text = id
    youtube = settings.YOUTUBE_OBJ

    search_response = youtube.videos().list(
        id=query_text,
        part="id,snippet,statistics",
        # videoEmbeddable=true,
        # regionCode="kr",
        # relevanceLanguage="ko"
    ).execute()

    videos = []

    for i in range(len(search_response['items'])):

        videos.append(
            [
                search_response['items'][i]['id'],
                search_response['items'][i]['snippet']['title'].strip(),
                search_response['items'][i]['snippet']['description'].strip(),
                search_response['items'][i]['snippet']['thumbnails']['high']['url'].strip(),
                search_response['items'][i]['snippet']['channelId'].strip(),
                search_response['items'][i]['snippet']['channelTitle'].strip(),
                date_parse(search_response['items'][i]['snippet']['publishedAt'].strip()),
                # search_response['items'][i]['snippet']['publishedAt'].strip(),
                search_response['items'][i]['statistics']['viewCount'].strip(),
                search_response['items'][i]['statistics']['likeCount'].strip(),
                search_response['items'][i]['statistics']['favoriteCount'].strip(),
                search_response['items'][i]['statistics']['commentCount'].strip(),
            ]
        )

    return videos
