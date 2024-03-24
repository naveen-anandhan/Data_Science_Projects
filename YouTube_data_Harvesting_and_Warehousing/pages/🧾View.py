import streamlit as st
import pymysql
import pandas as pd
import matplotlib.pyplot as plt

def fetch_data(question):
    try:
        # Connect to MySQL
        my_connection = pymysql.connect(host='127.0.0.1', user='root', passwd='8680974712@Sql', database="youtube_harvest")
        cursor = my_connection.cursor()

        if question == "1.What are the names of all the videos and their corresponding channels?":  
                cursor.execute("SELECT DISTINCT Title, Channel_Name FROM videos")
                data = cursor.fetchall()
                na = pd.DataFrame(data, columns=['Video Name', 'Channel Name'])
                df = None

                # Group by channel name and count the number of videos per channel
                videos_per_channel = na.groupby('Channel Name').size().reset_index(name='Total Videos')
            
                st.write("Table of Videos and Corresponding Channels:")
                st.dataframe(na)
                
                st.write("Bar Chart of Total Videos per Channel:")
                st.bar_chart(videos_per_channel.set_index('Channel Name'))

        elif question == "2.Which channels have the most number of videos, and how many videos do they have?":
                # Execute SQL query to fetch channel names and video counts
                cursor.execute("SELECT DISTINCT Channel_Name, Total_Videos FROM channel_data ORDER BY Total_Videos DESC")
                data = cursor.fetchall()
                na = pd.DataFrame(data, columns=['Channel Name', 'Video Count'])
                df = None

                # Display the DataFrame
                st.write("Table of Channels with Most Videos:")
                st.dataframe(na)

                # Sort the DataFrame by 'Total Videos' in descending order
                na_sorted = na.sort_values(by='Video Count', ascending=False)

                # Create and display the horizontal bar chart
                plt.figure(figsize=(10, 6))
                plt.barh(na_sorted['Channel Name'], na_sorted['Video Count'])  # Swap x and y arguments
                plt.xlabel('Channel Name')
                plt.ylabel('Video Count')
                plt.title('Channels with Most Videos')
                plt.grid(axis='x')  # Show gridlines along the x-axis
                plt.tight_layout()  # Adjust layout to prevent clipping of labels
                st.pyplot(plt)

        elif question == "3.What are the top 10 most viewed videos and their respective channels?":
            # Execute SQL query to fetch top 10 most viewed videos and their respective channels
            cursor.execute("SELECT Title, Channel_Name, Views FROM videos ORDER BY Views DESC LIMIT 10 ")
            data = cursor.fetchall()
            na = pd.DataFrame(data, columns=['Video Name', 'Channel Name', 'View Count'])
            df = None
            st.write("Top 10 Most Viewed Videos:")
            st.dataframe(na)

            plt.figure(figsize=(12, 8))
            for index, row in na.iterrows():
                plt.barh(index, row['View Count'], color='skyblue')
                plt.text(row['View Count'], index, f'{row["Video Name"]}', ha='left', va='center', fontsize=12, color='red')
            plt.yticks(range(len(na)), na['Channel Name'])
            plt.xlabel('View Count')
            plt.ylabel('Channel Name')
            plt.title('Top 10 Most Viewed Videos and Their Respective Channels')
            plt.gca().invert_yaxis()  # Invert the y-axis to display the highest view count at the top
            plt.tight_layout()  # Adjust layout to prevent clipping of labels
            st.pyplot(plt)

        elif question == "4.How many comments were made on each video, and what are their corresponding video names?":
            # Execute SQL query to fetch video names, number of comments, and channel names
            cursor.execute("SELECT Title, Comments, Channel_Name FROM videos ORDER BY Comments DESC LIMIT 20")
            data = cursor.fetchall()
            na = pd.DataFrame(data, columns=['Video Name', 'Comments', 'Channel Name'])
            df = None

            st.write("No of comments data:")
            st.dataframe(na)
            # Group by channel name and sum up the number of comments for each channel
            comments_per_channel = na.groupby('Channel Name')['Comments'].sum().reset_index()
            
            # Create a pie chart
            st.write("Pie Chart of Total Comments per Channel:")
            fig, ax = plt.subplots()
            ax.pie(comments_per_channel['Comments'], labels=comments_per_channel['Channel Name'], autopct='%1.1f%%')
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig)

        elif question == "5.Which videos have the highest number of likes, and what are their corresponding channel names?":
                # Execute SQL query to fetch videos with the highest number of likes for each channel   
                cursor.execute("SELECT Title, Likes, Channel_Name FROM videos ORDER BY Likes DESC LIMIT 20")
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=['Video Name', 'Highest Likes', 'Channel Name'])

        elif question == "6.What is the total number of likes and dislikes for each video, and what are their corresponding video names?":
                # Execute SQL query to fetch total number of likes and dislikes for each video
                cursor.execute("SELECT Title, Likes, Dislikes, Channel_Name FROM videos ORDER BY Likes DESC LIMIT 20")
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=['Video Name', 'No of Likes', 'No of Dislikes', 'Channel Name'])

        elif question == "7.What is the total number of views for each channel, and what are their corresponding channel names?":
                # Execute SQL query to fetch total number of views for each channel
                cursor.execute("SELECT Views, Channel_Name FROM videos ORDER BY Views DESC LIMIT 20")
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=['Total No of Views', 'Channel Name'])    

        elif question == "8.What are the names of all the channels that have published videos in the year 2022?":
                cursor.execute("SELECT DISTINCT Channel_Name, DATE(Published_Date) AS Published_Date FROM videos WHERE YEAR(Published_Date) = 2022")
                data = cursor.fetchall()
                na = pd.DataFrame(data, columns=['Channel Name', 'Videos published in 2022'])
                df=None
                # Group by channel name and count the number of videos published in 2022 for each channel
                videos_per_channel = na.groupby('Channel Name').size().reset_index(name='Videos Published in 2022')
                
                st.write("Videos Published in 2022")
                st.dataframe(na)
                # Create and display the bar chart
                st.write("Bar Chart of Videos Published in 2022 per Channel:")
                st.bar_chart(videos_per_channel.set_index('Channel Name'))

        elif question == "9.What is the average duration of all videos in each channel, and what are their corresponding channel names?":
                cursor.execute("SELECT Channel_Name, TIME_FORMAT(SEC_TO_TIME(AVG(TIME_TO_SEC(Duration))), '%H:%i:%s') AS Average_Duration FROM videos GROUP BY Channel_Name")
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=['Channel Name', 'Average Duration of all videos'])

        elif question == "10.Which videos have the highest number of comments, and what are their corresponding channel names?":
            try:
                cursor.execute("SELECT Title, Comments, Channel_Name FROM videos ORDER BY Comments DESC LIMIT 20")
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=['Video Name', 'Highest number of comments', 'Channel Name'])
            except Exception as e:
                st.error(f"Error occurred: {e}")

        my_connection.close()

        return df
    except Exception as e:
        # Handle exceptions and return None
        st.error(f"Error occurred: {e}")
        return None

# Streamlit app
st.title("Select any question to get insights")
question = st.selectbox(label="Questions", options=[
    '1.What are the names of all the videos and their corresponding channels?',
    '2.Which channels have the most number of videos, and how many videos do they have?',
    '3.What are the top 10 most viewed videos and their respective channels?',
    '4.How many comments were made on each video, and what are their corresponding video names?',
    '5.Which videos have the highest number of likes, and what are their corresponding channel names?',
    '6.What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
    '7.What is the total number of views for each channel, and what are their corresponding channel names?',
    '8.What are the names of all the channels that have published videos in the year 2022?',
    '9.What is the average duration of all videos in each channel, and what are their corresponding channel names?',
    '10.Which videos have the highest number of comments, and what are their corresponding channel names?'
])

if st.button("Show Insights"):
    # Fetch data
    df = fetch_data(question)

    if df is not None:
        # Display table
        st.write("Table:")
        st.dataframe(df)
