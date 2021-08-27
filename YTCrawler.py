import requests
from datetime import datetime

YTAPI = 'AIzaSyCJXA1a4BKp5va4QjJ1BCZYCHPQYfgLRE4'

def main():
    ChannelIDs = {
        'LLSeries':'UCTkyJbRhal4voLZxmdRSssQ',
        'MuseTW':'UCgdwtyqBunlRb-i-7PnCssQ'
    }
    Crawler = YTCrawler(YTAPI)
    uploads_id = Crawler.get_uploads_id(ChannelIDs['LLSeries'])
    #print(uploads_id)
    playlist = Crawler.get_playlist(uploads_id)
    #print(playlist)
    video_info = Crawler.get_video(playlist[0])
    print(video_info)

class YTCrawler():
    def __init__(self, key):
        self.base_url = 'https://www.googleapis.com/youtube/v3/'
        self.key = key

    def html_to_json(self, path):
        url = f'{self.base_url}{path}&key={self.key}'
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            data = r.json()
        else:
            data = None
        return data

    def get_uploads_id(self, channel_id, part='contentDetails'):
        path = f'channels?part={part}&id={channel_id}'
        data = self.html_to_json(path)
        try:
            uploads_id = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        except KeyError:
            uploads_id = None
        return uploads_id

    def get_playlist(self, playlist_id, part='contentDetails', max_results=5):
        path = f'playlistItems?part={part}&playlistId={playlist_id}&maxResults={max_results}'
        data = self.html_to_json(path)
        if not data:
            return []
        video_ids = []
        for item in data['items']:
            video_ids.append(item['contentDetails']['videoId'])
        return video_ids

    def get_video(self, video_id, part='snippet,statistics'):
        path = f'videos?part={part}&id={video_id}'
        data = self.html_to_json(path)
        if not data:
            return {}
        data_item = data['items'][0]
        url_ = f"https://www.youtube.com/watch?v={data_item['id']}"

        info = {
            'id': data_item['id'],
            'channel': data_item['snippet']['channelTitle'],
            'time': data_item['snippet']['publishedAt'],
            'url': url_,
            'title': data_item['snippet']['title'],
            'description': data_item['snippet']['description'],
            'likes': data_item['statistics']['likeCount'],
            'dislikes': data_item['statistics']['dislikeCount'],
            'commentCount': data_item['statistics']['commentCount'],
            'views': data_item['statistics']['viewCount']
        }
        return info
        
"""
從網站回傳的資料格式：
{
    'kind': 'youtube#video', 
    'etag': 'O8dYZboHRUpUtILcansZCTS4eho', 
    'id': 'cROw7-Yrt3w', 
    'snippet': {
        'publishedAt': '2021-08-21T06:37:39Z', 
        'channelId': 'UCgdwtyqBunlRb-i-7PnCssQ', 
        'title': '東京復仇者', 
        'description': '《東京復仇者》', 
        'thumbnails': {
            default': {
                'url': 'https://i.ytimg.com/vi/cROw7-Yrt3w/default.jpg', 
                'width': 120, 
                'height': 90
            }, 
            'medium': {
                'url': 'https://i.ytimg.com/vi/cROw7-Yrt3w/mqdefault.jpg', 
                'width': 320, 
                'height': 180
            }, 
            'high': {
                'url': 'https://i.ytimg.com/vi/cROw7-Yrt3w/hqdefault.jpg', 
                'width': 480, 
                'height': 360
            }, 
            'standard': {
                'url': 'https://i.ytimg.com/vi/cROw7-Yrt3w/sddefault.jpg', 
                'width': 640, 
                'height': 480
            }, 
            'maxres': {
                'url': 'https://i.ytimg.com/vi/cROw7-Yrt3w/maxresdefault.jpg', 
                'width': 1280, 
                'height': 720
            }
        }, 
        'channelTitle': 'Muse木棉花-TW', 
        'tags': ['新番', 'Muse木棉花', '東京復仇者'], 
        'categoryId': '1', 
        'liveBroadcastContent': 'upcoming', 
        'localized': {
            'title': '東京復仇者', 
            'description': '《東京復仇者》'
        }, 
        'defaultAudioLanguage': 'ja'
    }, 
    'statistics': {
        'viewCount': '0', 
        'likeCount': '21', 
        'dislikeCount': '0', 
        'favoriteCount': '0', 
        'commentCount': '3'
    }
}
"""