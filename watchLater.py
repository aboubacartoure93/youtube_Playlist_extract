


#------------------------------------------------------------------------
    
  # -*- coding: utf-8 -*-

# Sample Python code for youtube.playlistItems.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from datetime import timedelta
import isodate
import pandas as pd

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]




# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = r"C:/Users/aboub/Downloads/youtube_playlist/YOUR_CLIENT_SECRET_FILE.json"

# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)
'''
request = youtube.playlistItems().list(
    part="contentDetails",
    maxResults=25,
    #playlistId="PLqVVAK0h-QnC_Ui2kpCtL-M9kj2HkLnO1" #watch later 2
    #playlistId ="PLqVVAK0h-QnCXSirQUJf0jcYUZLKSvqtC" #delete playlist
    )

response = request.execute()

print(response)

'''

def get_playlist_videos(playlist_id):
    videos = []
    next_page_token = None
   
    while True:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        
        video_ids = [item['contentDetails']['videoId'] for item in response['items']]
        videos.extend(get_video_details(video_ids))
        
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    
    return videos

def get_video_details(video_ids):
    video_details = []
    
    request = youtube.videos().list(
        part="contentDetails,snippet",
        id=",".join(video_ids)
    )
    response = request.execute()
    
    for item in response['items']:
        video_id = item['id']
        title = item['snippet']['title']
        duration = isodate.parse_duration(item['contentDetails']['duration'])
        channel_title = item['snippet']['channelTitle']
        video_details.append((title, duration, channel_title, video_id))
        print(video_id)
        
    return video_details

def main():
    #playlistId ="PLqVVAK0h-QnC_Ui2kpCtL-M9kj2HkLnO1" #watch later 2
    playlistId ='PLqVVAK0h-QnB12dhma4ahehfGlmI36sxs' #watch later copy2
    
    videos = get_playlist_videos(playlistId)
    videos_sorted = sorted(videos, key=lambda x: x[2])  # Sort by duration
    
    # Prepare data for Excel
    data = {
        "Title": [video[0] for video in videos_sorted],
        "Duration": [str(video[1]) for video in videos_sorted],
        "URL": [f"https://www.youtube.com/watch?v={video[3]}" for video in videos_sorted],
        "Channel Name": [video[2] for video in videos_sorted],
        "Video ID": [video[3] for video in videos_sorted]
        }
    df = pd.DataFrame(data)
        
    # Save to Excel file
    output_file = "youtube_videos_sorted.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Excel file '{output_file}' created successfully.")


if __name__ == "__main__":
    main()

