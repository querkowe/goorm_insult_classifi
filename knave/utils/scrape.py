from googleapiclient.discovery import build
from oauth2client.tools import argparser
from django.conf import settings
import pandas as pd

def get_comments(video):

    # print(video)

    #사용자 계정 api_key
    api_key = settings.API_KEY

    # 비디오 주소 맨 뒤쪽에 있음
    video_id = video

    limit = 100

    comments = list()
    api_obj = settings.YOUTUBE_OBJ
    response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, maxResults=100).execute()

    while response and len(comments) < limit:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append([comment['textDisplay'], comment['authorDisplayName'], comment['publishedAt'], comment['likeCount']])

            if item['snippet']['totalReplyCount'] > 0:
                for reply_item in item['replies']['comments']:
                    reply = reply_item['snippet']
                    comments.append([reply['textDisplay'], reply['authorDisplayName'], reply['publishedAt'], reply['likeCount']])

        if 'nextPageToken' in response:
            response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, pageToken=response['nextPageToken'], maxResults=100).execute()
        else:
            break

    # print(len(comments))

    return pd.DataFrame(comments, columns=['comment', 'author', 'date', 'num_likes']).to_html()

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
            (
                search_response['items'][i]['id']['videoId'],
                search_response['items'][i]['snippet']['title'],
                search_response['items'][i]['snippet']['description'],
                search_response['items'][i]['snippet']['thumbnails']['high']['url'],
                search_response['items'][i]['snippet']['channelId'],
                search_response['items'][i]['snippet']['channelTitle'],
                search_response['items'][i]['snippet']['publishedAt'],
                get_comments(search_response['items'][i]['id']['videoId'])
            )
        )

    return videos

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
            (
                search_response['items'][i]['snippet']['title'],
                search_response['items'][i]['snippet']['description'],
                search_response['items'][i]['snippet']['thumbnails']['high']['url'],
                search_response['items'][i]['snippet']['channelId'],
                # search_response['items'][i]['snippet']['channelTitle'],
                search_response['items'][i]['snippet']['publishedAt'],
            )
        )

    return channels

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
            (
                search_response['items'][i]['id']['videoId'],
                search_response['items'][i]['snippet']['title'],
                search_response['items'][i]['snippet']['description'],
                search_response['items'][i]['snippet']['thumbnails']['high']['url'],
                search_response['items'][i]['snippet']['channelId'],
                search_response['items'][i]['snippet']['channelTitle'],
                search_response['items'][i]['snippet']['publishedAt'],
                get_comments(search_response['items'][i]['id']['videoId'])
            )
        )

    return videos
