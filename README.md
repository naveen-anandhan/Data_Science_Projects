YouTube Data Extractor:

This project consists of two main parts:

YouTube Data Extractor: A Streamlit application that allows users to extract data from a YouTube channel using the YouTube Data API. The extracted data includes channel information, video details, playlist information, and comments. This data is then stored in a MySQL database for further analysis.

YouTube Data Analyzer: Another Streamlit application that provides various insights and analytics based on the data stored in the MySQL database. Users can select from a list of predefined questions to get insights such as most viewed videos, channels with the most videos, total likes and dislikes for each video, and more.

Features:
1.Channel Information Extraction: The application allows users to input a YouTube channel ID. Upon clicking the "Extract" button, the application retrieves various details about the channel, such as its name, subscription count, views, total videos, and description.

2.Video Details Extraction: Using the YouTube API, the application fetches information about all the videos uploaded to the channel. This includes details like video title, thumbnail URL, description, published date, duration, views, likes, dislikes, comments, favorite count, video definition, and caption status.

3.Playlist Information Extraction: The application also fetches details about playlists associated with the channel, including the playlist title, ID, channel ID, channel name, published date, and the number of videos in each playlist.

4.Comments Data Extraction: Comments from all videos uploaded to the channel are extracted, including the comment ID, video ID, comment text, commenter name, and comment published date.

5.Data Upload to SQL Database: After extraction, the data is uploaded to a MySQL database for storage and further analysis. The application creates separate tables for storing channel data, video details, playlist information, and comments.

Usage:

1.Input Channel ID: Provide the YouTube channel ID in the input field and click the "Extract" button to fetch the channel's data.

2.Data Extraction: After entering the channel ID, the application retrieves various details about the channel, videos, playlists, and comments associated with it.

3.Upload to SQL: Once the data is extracted, users can click the "Upload to SQL" button to store the data in a MySQL database.

Dependencies:
Python 3.x
Streamlit
Pandas
Matplotlib
PyMySQL
google-api-python-client

Obtain a YouTube Data API key from the Google Cloud Console and replace the api_key variable in the api_connect function with your API key.

Ensure that you have a MySQL database set up with the appropriate tables as defined in the create_tables function.

Modify the MySQL connection details (host, username, password, database) in both the data extraction and analysis scripts to match your database configuration.

Run the YouTube Data Analyzer script (youtube_data_analyzer.py). Select a question from the dropdown list and click the "Show Insights" button to get analytics based on the stored data.

Notes:
The Streamlit applications provide a user-friendly interface for interacting with the data extraction and analysis functionalities.
The provided SQL queries and Python functions handle data extraction, storage, and retrieval efficiently.
Make sure to handle API quotas and limits while using the YouTube Data API to avoid rate limiting issues.


Thankyou:
Naveen Anandhan
