from googleapiclient.discovery import build
from oauth2client.tools import argparser
from django.conf import settings
import pandas as pd

from . import analysis

def get_comments(video):

    # print(video)

    #사용자 계정 api_key
    api_key = settings.API_KEY

    # 비디오 주소 맨 뒤쪽에 있음
    video_id = video

    limit = 100

    comments = list()
    api_obj = settings.YOUTUBE_OBJ
    good_count = 0
    bad_count = 0
    response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, maxResults=100).execute()

    if response and len(comments) < limit:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']

            # comments.append([comment['textDisplay'], comment['authorDisplayName'], comment['publishedAt'], comment['likeCount']])
            comments.append([comment['textDisplay'], comment['publishedAt'], comment['likeCount']])

            result = analysis.predict_sent(comments[-1][0])

            if result == 0:
                result = " 악성 👿"
                bad_count += 1
            elif result == 1:
                result = " 정상 😀"
                good_count += 1

            comments[-1].append(result)


    # print(len(comments))

    # return good_count, bad_count, pd.DataFrame(comments, columns=['comment', 'author', 'date', 'num_likes', 'is_bad']).to_html().strip()
    return good_count, bad_count, pd.DataFrame(comments, columns=['댓글 내용', '게시일', '좋아요', '판별 결과']).to_html(classes='table', index=False).strip()

# def search_text(text):
#     query_text = text
#     max_results = 10
#     youtube = settings.YOUTUBE_OBJ
#
#     search_response = youtube.search().list(
#         q=query_text,
#         order="relevance",
#         part="snippet",
#         type='video',
#         maxResults=max_results,
#         # videoEmbeddable=true,
#         regionCode="kr",
#         relevanceLanguage="ko"
#     ).execute()
#
#     videos = []
#
#     for i in range(len(search_response['items'])):
#
#         good_count, bad_count, comments_df = get_comments(search_response['items'][i]['id']['videoId'])
#
#         videos.append(
#             [
#                 search_response['items'][i]['id']['videoId'].strip(),
#                 search_response['items'][i]['snippet']['title'].strip(),
#                 search_response['items'][i]['snippet']['description'].strip(),
#                 search_response['items'][i]['snippet']['thumbnails']['high']['url'].strip(),
#                 search_response['items'][i]['snippet']['channelId'].strip(),
#                 search_response['items'][i]['snippet']['channelTitle'].strip(),
#                 search_response['items'][i]['snippet']['publishedAt'].strip(),
#                 good_count,
#                 bad_count,
#                 comments_df
#             ]
#         )
#
#     return videos

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
                search_response['items'][i]['snippet']['publishedAt'].strip(),
            ]
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
            [
                search_response['items'][i]['snippet']['title'].strip(),
                search_response['items'][i]['snippet']['description'].strip(),
                search_response['items'][i]['snippet']['thumbnails']['high']['url'].strip(),
                search_response['items'][i]['snippet']['channelId'].strip(),
                # search_response['items'][i]['snippet']['channelTitle'],
                search_response['items'][i]['snippet']['publishedAt'].strip(),
            ]
        )

    return channels

def search_video_list(vids):
    max_results = 10
    youtube = settings.YOUTUBE_OBJ

    videos = []

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

        videos.append(
            [
                search_response['items'][0]['id'].strip(),
                search_response['items'][0]['snippet']['title'].strip(),
                search_response['items'][0]['snippet']['description'].strip(),
                search_response['items'][0]['snippet']['thumbnails']['high']['url'].strip(),
                search_response['items'][0]['snippet']['channelId'].strip(),
                search_response['items'][0]['snippet']['channelTitle'].strip(),
                search_response['items'][0]['snippet']['publishedAt'].strip(),
                search_response['items'][0]['statistics']['viewCount'].strip(),
                search_response['items'][0]['statistics']['likeCount'].strip(),
                search_response['items'][0]['statistics']['favoriteCount'].strip(),
                search_response['items'][0]['statistics']['commentCount'].strip(),
                good_count,
                bad_count,
                comments_df
            ]
        )

    return videos

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
                search_response['items'][i]['snippet']['publishedAt'].strip()
            ]
        )

    return videos

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
                search_response['items'][i]['snippet']['publishedAt'].strip(),
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
                search_response['items'][i]['snippet']['publishedAt'].strip(),
                search_response['items'][i]['statistics']['viewCount'].strip(),
                search_response['items'][i]['statistics']['likeCount'].strip(),
                search_response['items'][i]['statistics']['favoriteCount'].strip(),
                search_response['items'][i]['statistics']['commentCount'].strip(),
            ]
        )

    return videos
