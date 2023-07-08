from googleapiclient.discovery import build
import pandas as pd
import logging

class Scraping:
    @staticmethod
    def channel_playlist_id(token, idd):
        try:
            youtube = build('youtube', 'v3', developerKey=token)
            request = youtube.channels().list(
                part='snippet,contentDetails,statistics',
                id=idd
            )
            response = request.execute()
            playlist_id  = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            Channel_name = response['items'][0]['snippet']['title']
            
            request = youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId=playlist_id,
                    maxResults=50)
            
            response = request.execute()

            video_ids = [] # getting all videos ids

            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])

            next_page_token = response.get('nextPageToken')
            more_pages = True

            while more_pages:
                if next_page_token is None:
                    more_pages = False
                else:
                    request = youtube.playlistItems().list(
                                part='contentDetails',
                                playlistId=playlist_id,
                                maxResults=50,
                                pageToken=next_page_token)
                    response = request.execute()

                    for i in range(len(response['items'])):
                        video_ids.append(response['items'][i]['contentDetails']['videoId'])

                    next_page_token = response.get('nextPageToken')
            
            all_video_stats = [] # al videos data is available

            for i in range(0, len(video_ids), 50):
                request = youtube.videos().list(
                            part='snippet,statistics',
                            id=','.join(video_ids[i:i+50]))
                response = request.execute()
            
            # Extract video URL, URL Thumbnails, Titles, Views, Time of posting
                for video in response['items']:
                    video_stats = dict(Video_URL="https://www.youtube.com/watch?v="+str(video["id"]),
                                    Thumbnails_URL=video["snippet"]["thumbnails"]["high"]["url"],
                                    Title=video['snippet']['title'],
                                    Views=video['statistics']['viewCount'],
                                    Published_date=video['snippet']['publishedAt']
                                    )
                    all_video_stats.append(video_stats)
            
            video_data = pd.DataFrame(all_video_stats) # Convert all data to a DataFrame
            video_data['Views'] = pd.to_numeric(video_data['Views'])
            video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date
            
            return video_data
        
        except Exception as e:
            logging.error(f"Scraping Error: {str(e)}")
            return pd.DataFrame()

