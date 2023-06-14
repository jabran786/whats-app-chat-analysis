# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 19:18:34 2023

@author: STAR PC11
"""
# from tkinter import VERTICAL
# from turtle import color
import streamlit as st 
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns 

st.sidebar.title('What\'s App Chat Analyzer   (version 1.0 )')

# Upload a chat.txt file 
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.proprocess(data)
    # show all messages in a df
    # st.dataframe(df)

    # Fetch unique users and create list    
    users_list = df['user'].unique().tolist()

    users_list.remove('group_notification')
    users_list.sort()
    users_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show Analyses w.r.t ",users_list)

    # menu create button to show analysis   (----------------------section------------------------)
    if st.sidebar.button("Show Analysis"):
        num_messages, words, media, total_links = helper.fetch_stats(selected_user,df)
        st.title("Overall Chat Summary ")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media")
            st.title(media)
        with col4:
            st.header("Total  Links")
            st.title(total_links)    

        
        # Monthly Timeline generation  (----------------------section------------------------)
        st.title("Monthly chat Analysis Graph")
        timeline = helper.monthly_timeline(selected_user,df)
        fig, ax =plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color ='green')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # Daily Timeline generation  (----------------------section------------------------)
        st.title("Daily chat Analysis Graph")
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig, ax =plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color ='black')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # Activity Map  (----------------------section------------------------)

        st.title('Activity Map')
        col1,col2 = st.columns(2)

        # Day Wise chat counts
        with col1:
            st.header("Most busy day of week")    
            busy_day  = helper.week_activity_chart(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='orange')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
        # month Wise chat counts
        with col2:
            st.header("Most busy Month")    
            busy_month  = helper.month_activity_chart(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='brown')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
        st.title("Weekly Activity Map")
        # Heat Map
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)



        # menu Creat Most busy user graph   (----------------------section------------------------)
        if selected_user == 'Overall':
            st.title("Top 5 Busy Users")
            x, new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.header("Message Percentage")
                st.dataframe(new_df)

        # Create Word cloud (----------------------section------------------------)
        st.markdown("<h1 style='text-align: left; font-size: 36px; color: green;'>Word Cloud ( Your Personality In One Picture)</h1>", unsafe_allow_html=True)
        df_wc = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Most Common Words
        most_common_df = helper.most_common_words(selected_user,df)
        
        # Print Data Frame
        # st.dataframe(most_common_df)

        fig, ax = plt.subplots()
        
        ax.barh(most_common_df[0],most_common_df[1], color='green')
        #make bar heading vertical
        plt.xticks(rotation='vertical')

        # Add labels to the end of each bar
        for i, v in enumerate(most_common_df[1]):
            ax.text(v, i, str(v), color='blue', fontweight='bold')

        st.title("Most common Words ")
        st.pyplot(fig)

        # Emoji analysis (----------------------section------------------------)
        st.title("Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user,df)
        

        col1, col2 = st.columns(2)

        with col1:#printing data table of emojis
            st.dataframe(emoji_df)

        with col2:# printing piechat of emojis
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)
