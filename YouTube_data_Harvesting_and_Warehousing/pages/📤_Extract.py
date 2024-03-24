import pymysql
import pandas as pd
from googleapiclient.discovery import build
import streamlit as st
from datetime import datetime
from googleapiclient.errors import HttpError

# Function to connect to YouTube API
def api_connect():
    try:
        api_key = "AIzaSyC3yAjUEmfHnqBGC3RX5aheo2hVsBj_gds"  # API key
        api_service_name = "youtube"
        api_version = "v3"
        youtube = build(api_service_name, api_version, developerKey=api_key)
        return youtube
    except Exception as e:
        print("Error connecting to the YouTube API:", e)
        return None

# Function to get channel information from YouTube API
def get_channel_info(youtube, channel_id):
    try:
        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id=channel_id
        )
        response = request.execute()
        if 'items' in response and response['items']:
            item = response['items'][0]
            data = {
                'Channel_Name': item["snippet"]["title"],
                'Channel_Id': item["id"],
                'Subscription_Count': int(item["statistics"]["subscriberCount"]),
                'Views': int(item['statistics']['viewCount']),
                'Total_Videos': int(item["statistics"]["videoCount"]),
                'Channel_Description': item["snippet"]["description"],
                'Playlist_id': item['contentDetails']['relatedPlaylists']['uploads']
            }
            return data
        else:
            print("No channel information found.")
            return None
    except Exception as e:
        print("Error fetching channel information:", e)
        return None
    
# Getting videos ids
def get_videos_ids(youtube, channel_id):
    video_ids = []
    response = youtube.channels().list(id=channel_id, part='contentDetails').execute()

    playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    next_page_token = None

    while True:
        response1 = youtube.playlistItems().list(part='snippet',
                                                playlistId=playlist_id,
                                                maxResults=50,
                                                pageToken=next_page_token).execute()
        for i in range(len(response1['items'])):
            video_ids.append(response1['items'][i]['snippet']['resourceId']['videoId'])
        next_page_token = response1.get('nextPageToken')

        if next_page_token is None:
            break
    return video_ids
def convert_duration(Duration):
    Duration = Duration[2:]  # Remove the leading 'PT' indicating duration
    hours = minutes = seconds = 0

    if 'H' in Duration:
        hours = int(Duration.split('H')[0])
        Duration = Duration.split('H')[1]

    if 'M' in Duration:
        minutes = int(Duration.split('M')[0])
        Duration = Duration.split('M')[1]

    if 'S' in Duration:
        seconds = int(Duration.split('S')[0])

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
#geting videos info
def get_video_info(youtube, video_ids):
    video_data = []
    for video_id in video_ids:
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()

        for item in response["items"]:
            data = dict(Channel_Name=item['snippet']['channelTitle'],
                        Channel_Id=item['snippet']['channelId'],
                        Video_Id=item['id'],
                        Title=item['snippet']['title'],
                        Thumbnail=item['snippet']['thumbnails']['default']['url'],
                        Description=item['snippet'].get('description'),
                        Published_Date=item['snippet']['publishedAt'],
                        Duration=item['contentDetails']['duration'],
                        Views=item['statistics'].get('viewCount'),
                        Likes=item['statistics'].get('likeCount'),
                        Dislikes=item['statistics'].get('dislikeCount'),
                        Comments=item['statistics'].get('commentCount'),
                        Favorite_Count=item['statistics'].get('favoriteCount'),
                        Definition=item['contentDetails']['definition'],
                        Caption_status=item['contentDetails'].get('caption')
                        )
            video_data.append(data)
    return video_data

#geting playlist data
def get_playlist_details(youtube, channel_id):

    next_page_token = None
    All_data = []

    while True:
        request = youtube.playlists().list(
            part='snippet,contentDetails',
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            data = dict(playlist_Id=item['id'],
                        Title=item['snippet']['title'],
                        Channel_Id=item['snippet']['channelId'],
                        Channel_Name=item['snippet']['channelTitle'],
                        PublishedAt=item['snippet']['publishedAt'],
                        Video_Count=item['contentDetails']['itemCount'])
            All_data.append(data)

        next_page_token = response.get('nextPageToken')
        if next_page_token is None:
            break
    return All_data

#comments data fetching
def get_comment_info(youtube, video_ids):
    Comment_data = []
    try:
        for video_id in video_ids:
            next_page_token = None
            while True:
                request = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    maxResults=50,  # Set max results per page
                    pageToken=next_page_token
                )
                response = request.execute()

                if 'items' in response:
                    for item in response['items']:
                        data = dict(Comment_Id=item['snippet']['topLevelComment']['id'],
                                    Video_id=item['snippet']['topLevelComment']['snippet']['videoId'],
                                    Comment_Text=item['snippet']['topLevelComment']['snippet']['textDisplay'],
                                    Comment_Author=item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                                    Comment_Published=item['snippet']['topLevelComment']['snippet']['publishedAt'])
                        Comment_data.append(data)

                    # Check if there are more pages
                    if 'nextPageToken' in response:
                        next_page_token = response['nextPageToken']
                    else:
                        break
                else:
                    print(f"No comments found for video with ID {video_id}")
                    break

    except HttpError as e:
        # Handle HttpError 403 (commentsDisabled) specifically
        if e.resp.status == 403:
            print(f"Comments are disabled for video with ID {video_id}. Skipping...")
        else:
            # Re-raise other HttpErrors
            raise
    except Exception as e:
        print(f"Error encountered: {e}")

    return Comment_data

#creating table
def create_tables():
    try:
        my_connection = pymysql.connect(host='127.0.0.1', user='root', passwd='8680974712@Sql', database="youtube_harvest")
        cursor = my_connection.cursor()
        # Creating channel_data table
        cursor.execute("CREATE TABLE IF NOT EXISTS channel_data ("
                       "id INT AUTO_INCREMENT PRIMARY KEY,"
                       "Channel_Name VARCHAR(255),"
                       "Channel_Id VARCHAR(255),"
                       "Subscription_Count INT,"
                       "Views INT,"
                       "Total_Videos INT,"
                       "Channel_Description TEXT,"
                       "Playlist_id VARCHAR(255)"
                       ")")
        my_connection.commit()

        # Creating videos table
        cursor.execute('''CREATE TABLE IF NOT EXISTS videos(
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       Channel_Name VARCHAR(255),
                       Channel_Id VARCHAR(255),
                       Video_Id VARCHAR(255),
                       Title VARCHAR(255),
                       Thumbnail VARCHAR(255),
                       Description TEXT,
                       Published_Date DATETIME,
                       Duration TIME,
                       Views INT,
                       Likes INT,
                       Dislikes INT,
                       Comments INT,
                       Favorite_Count INT,
                       Definition VARCHAR(20),
                       Caption_status VARCHAR(255)
                       )''')
        my_connection.commit()

        # Creating playlist table
        cursor.execute('''CREATE TABLE IF NOT EXISTS playlist(
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       playlist_Id VARCHAR(100),
                       Title VARCHAR(255),
                       Channel_Id VARCHAR(255),
                       Channel_Name VARCHAR(255),
                       PublishedAt TIMESTAMP,
                       Video_Count INT
                       )''')
        my_connection.commit()

        # Creating comments table
        cursor.execute('''CREATE TABLE IF NOT EXISTS comments(
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       Comment_Id VARCHAR(100),
                       Video_id VARCHAR(255),
                       Comment_Text TEXT,
                       Comment_Author VARCHAR(255),
                       Comment_Published TIMESTAMP
                       )''')
        my_connection.commit()

    except pymysql.Error as e:
        print("Error creating tables:", e)

def insert_data(youtube, data, video_df, playlist_df, comments_df):
    try:
        my_connection = pymysql.connect(host='127.0.0.1', user='root', passwd='8680974712@Sql', database="youtube_harvest")
        cursor = my_connection.cursor()

        # Inserting data into the channel_data table
        cursor.execute("INSERT INTO channel_data (Channel_Name, Channel_Id, Subscription_Count, Views, Total_Videos, Channel_Description, Playlist_id) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (data['Channel_Name'], data['Channel_Id'], data['Subscription_Count'],
                        data['Views'], data['Total_Videos'], data['Channel_Description'],
                        data['Playlist_id']))
        print("Channel data inserted successfully.")

        # Inserting data into the videos table
        for row in video_df.itertuples():
            insert_query = '''INSERT INTO videos (Channel_Name, Channel_Id, Video_Id, Title, Thumbnail, Description, Published_Date, Duration ,Views ,Likes ,Dislikes ,Comments, Favorite_Count, Definition , Caption_status)
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            values = (row.Channel_Name, row.Channel_Id, row.Video_Id, row.Title, row.Thumbnail, row.Description, row.Published_Date, row.Duration, row.Views, row.Likes, row.Dislikes, row.Comments, row.Favorite_Count, row.Definition, row.Caption_status)
            cursor.execute(insert_query, values)
            update_query = "UPDATE videos SET dislikes = 0 WHERE dislikes IS NULL"
            cursor.execute(update_query)
        print("Video data inserted successfully.")

        # Inserting data into the playlist table
        for row in playlist_df.itertuples():
            insert_query = '''INSERT INTO playlist (playlist_Id, Title, Channel_Id, Channel_Name, PublishedAt, Video_Count)
                              VALUES (%s, %s, %s, %s, %s, %s)'''
            values = (row.playlist_Id, row.Title, row.Channel_Id, row.Channel_Name, row.PublishedAt, row.Video_Count)
            cursor.execute(insert_query, values)
        print("Playlist data inserted successfully.")

        # Inserting data into the comments table
        for row in comments_df.itertuples():
            insert_query = '''INSERT INTO comments (Comment_Id, Video_id, Comment_Text, Comment_Author, Comment_Published)
                              VALUES (%s, %s, %s, %s, %s)'''
            values = (row.Comment_Id, row.Video_id, row.Comment_Text, row.Comment_Author, row.Comment_Published)
            cursor.execute(insert_query, values)
        print("Comments data inserted successfully.")

        my_connection.commit()
    except pymysql.Error as e:
        print("Error inserting data:", e)
    finally:
        my_connection.close()


# Streamlit application
def main():
    st.title("YouTube Data Extractor Form")

    st.header("Enter YouTube Channel ID below:")
    channel_id = st.text_input("Hint: Go to channel's home page > Right click > View page source > Find Channel_id")

    if st.button("Extract"):
        if channel_id:
            st.info("Extracting data...")
            youtube = api_connect()
            data = get_channel_info(youtube, channel_id)
            video_ids = get_videos_ids(youtube, channel_id)
            video_details = get_video_info(youtube, video_ids)
            playlist_details = get_playlist_details(youtube, channel_id)
            comments_details = get_comment_info(youtube, video_ids)

            video_df = pd.DataFrame(video_details)
            video_df['Duration'] = video_df['Duration'].apply(convert_duration)
            video_df['Published_Date'] = pd.to_datetime(video_df['Published_Date'], format='%Y-%m-%dT%H:%M:%SZ')
          

            playlist_df = pd.DataFrame(playlist_details)
            playlist_df['PublishedAt'] = pd.to_datetime(playlist_df['PublishedAt'])

            comments_df = pd.DataFrame(comments_details)
            comments_df['Comment_Published'] = pd.to_datetime(comments_df['Comment_Published'])
            st.success("Data extracted successfully.")


            st.subheader("Channel Information")
            st.write("Channel Name:", data['Channel_Name'])
            st.write("Channel ID:", data['Channel_Id'])
            st.write("Subscription Count:", data['Subscription_Count'])
            st.write("Views:", data['Views'])
            st.write("Total Videos:", data['Total_Videos'])
            st.write("Channel Description:", data['Channel_Description'])
        else:
            st.warning("Please enter a YouTube channel ID.")   

    if st.button("Upload to SQL"):
        if channel_id:
            st.info("Uploading data to SQL...")
            youtube = api_connect()
            data = get_channel_info(youtube, channel_id)
            video_ids = get_videos_ids(youtube, channel_id)
            video_details = get_video_info(youtube, video_ids)
            playlist_details = get_playlist_details(youtube, channel_id)
            comments_details = get_comment_info(youtube, video_ids)

            video_df = pd.DataFrame(video_details)
            video_df['Duration'] = video_df['Duration'].apply(convert_duration)
            video_df['Published_Date'] = pd.to_datetime(video_df['Published_Date'], format='%Y-%m-%dT%H:%M:%SZ')
           

            playlist_df = pd.DataFrame(playlist_details)
            playlist_df['PublishedAt'] = pd.to_datetime(playlist_df['PublishedAt'])

            comments_df = pd.DataFrame(comments_details)
            comments_df['Comment_Published'] = pd.to_datetime(comments_df['Comment_Published'])
            # Call functions to create table and insert data into SQL
            create_tables()
            insert_data(youtube, data, video_df, playlist_df, comments_df)
            st.success("Data uploaded to SQL successfully.")
        else:
            st.warning("Please enter a YouTube channel ID.")

if __name__ == "__main__":
    main()

                      
