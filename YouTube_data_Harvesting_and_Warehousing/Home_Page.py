import streamlit as st
import altair as alt
import pandas as pd
import matplotlib.pyplot as plt



st.set_page_config(
    page_title="YouTube Data Harvesting and Warehousing",
    layout="wide"
)

# Title
st.title("YouTube Data Harvesting and Warehousing")

st.subheader("Project Description")

col1, col2, col3, _ = st.columns([4, 40, 5, 2]) 
with col1:
    st.image("C:\\Users\\mrnav\\OneDrive\\Desktop\\Python\\Practise\\YouTube_data_Harvesting_and_Warehousing\\youtube_logo.jpg",
             width=150)
with col2:
    st.markdown("<p style='font-size: 30px;'>This project is aimed at extracting data from a YouTube channel, including channel information, video details, playlist information, and comments. The extracted data is then stored in a MySQL database for further analysis or use.</p>", unsafe_allow_html=True)

# Dependencies
with col3:
    st.markdown("<h2 style='text-align: right; margin-top: -70px;'>Dependencies:</h2>", unsafe_allow_html=True)
    st.markdown("<ul style='text-align: right; font-size: 16px; list-style-type: none; margin-top: 0;'>"
                "<li>Python 3.x</li>"
                "<li>Streamlit</li>"
                "<li>Pandas</li>"
                "<li>pymysql</li>"
                "<li>google-api-python-client</li>"
                "</ul>", unsafe_allow_html=True)
    
st.subheader("Features:")

st.write("""1.Channel Information Extraction: The application allows users to input a YouTube channel ID. Upon clicking the "Extract" button, the application retrieves various details about the channel, such as its name, subscription count, views, total videos, and description.

2.Video Details Extraction: Using the YouTube API, the application fetches information about all the videos uploaded to the channel. This includes details like video title, thumbnail URL, description, published date, duration, views, likes, dislikes, comments, favorite count, video definition, and caption status.

3.Playlist Information Extraction: The application also fetches details about playlists associated with the channel, including the playlist title, ID, channel ID, channel name, published date, and the number of videos in each playlist.

4.Comments Data Extraction: Comments from all videos uploaded to the channel are extracted, including the comment ID, video ID, comment text, commenter name, and comment published date.

5.Data Upload to SQL Database: After extraction, the data is uploaded to a MySQL database for storage and further analysis. The application creates separate tables for storing channel data, video details, playlist information, and comments.""")

st.subheader("Usage:")

st.write("""1.Input Channel ID: Provide the YouTube channel ID in the input field and click the "Extract" button to fetch the channel's data.

2.Data Extraction: After entering the channel ID, the application retrieves various details about the channel, videos, playlists, and comments associated with it.

3.Upload to SQL: Once the data is extracted, users can click the "Upload to SQL" button to store the data in a MySQL database.""")

st.subheader("Setup Instructions:")

st.write("""1.Install the required dependencies using pip install -r requirements.txt.
         
2.Obtain a Google API key and enable the YouTube Data API v3.
         
3.Ensure that MySQL is installed and running on your system.
         
4.Update the MySQL database connection details in the code.
         
5.Run the application using streamlit run <filename.py>.""")


st.subheader("Contributors:")
st.write("Naveen Anandhan", unsafe_allow_html=True)




