import json

def youtube_api_key():
    value = ''
    with open('secret_value.json', 'r') as f:
        value = json.load(f)['youtube_api_key']
    return value

def django_secret_key():
    value = ''
    with open('secret_value.json', 'r') as f:
        value = json.load(f)['django_secret_key']
    return value
