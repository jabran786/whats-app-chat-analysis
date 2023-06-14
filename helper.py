import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji #pip install emoji~=1.5.0 for python 3,7

extract = URLExtract()
def fetch_stats(selected_user,df):
    if selected_user != "Overall":
       df= df[df['user'] == selected_user]

# def check_user(selected_user,df):
#      if selected_user != "Overall":
#        df= df[df['user'] == selected_user]
#      return df

    # 1.Calculate Total Messages

    num_messages = df.shape[0]

    # 2. Calculate Total Words
    
    words = []
    for message in df['message']:
        words.extend(message.split())
        total_words=len(words)
    # 3. Calculate Total Media files
   
    media = df[df['message'] =='<Media omitted>\n'].shape[0]
    
    # 4. calculate Total Links Shared

    links =[]
    for link in df['message']:
        links.extend(extract.find_urls(link))
        total_links = len(links)
    return num_messages, total_words ,media, total_links 

# Function to calculate most busy users and their percentages contribution

def most_busy_user(df):# (group level)
    # caculate total messages per user and then return top 5 
    x = df['user'].value_counts().head()

    # calculate message percentage and convert into data frame
    df = round((df['user'].value_counts()/ df.shape[0]) * 100, 2)
    df = df.reset_index().rename(columns = {'index':'name', 'user':'percentage ( % )'}) 
    df['percentage'] = (df['percentage ( % )']).astype(str) + ' % '
    
    #to drop duplicate column
    df.drop(columns=['percentage ( % )'], inplace=True)
    return x,df

def create_wordcloud(selected_user,df):
    if selected_user != "Overall":
       df= df[df['user'] == selected_user]
   
   # removing stop words etc reusing code
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    
    def remove_stop_words(message):
        w = []
        f = open('stop_hinglish.txt','r')
        stop_words = f.read()
        for word in message.lower().split():
            if word not in stop_words:
                w.append(word)
        return " ".join(w)

   
    # configure word cloud
    wc= WordCloud(width=500, height=500, min_font_size=14, background_color='white')

    # removing stop words etc reusing code
    temp['message'] = temp['message'].apply(remove_stop_words)

    # # remove media omitted values
    # df = df[~df['message'].str.contains("<Media omitted>")]

    #generate image 
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc

def most_common_words(selected_user,df):

    # open stop word file

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    # checking selected user
    if selected_user != "Overall":
       df= df[df['user'] == selected_user]
    
    #Remove group notifications and media omitted
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words =[]

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    # convering clean messages into a data frame
    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != "Overall":
       df= df[df['user'] == selected_user]
    emojis =[]
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


def monthly_timeline(selected_user,df):
    if selected_user != "Overall":
        df= df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range (timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != "Overall":
        df= df[df['user'] == selected_user]
    daily_timeline = df.groupby(['only_date']).count()['message'].reset_index()

    return daily_timeline

def week_activity_chart(selected_user,df):
    if selected_user != "Overall":
        df= df[df['user'] == selected_user]    

    return df['day_name'].value_counts()

def month_activity_chart(selected_user,df):
    if selected_user != "Overall":
        df= df[df['user'] == selected_user]    

    return df['month'].value_counts()    

def activity_heatmap(selected_user,df):
    if selected_user != "Overall":
        df= df[df['user'] == selected_user] 
    
    user_headmap  = df.pivot_table(index='day_name', columns = 'period', values = 'message', aggfunc= 'count').fillna(0)

    return user_headmap


















    # # 2. Calculate Total Words
    # words = []
    # for message in df['message']:
    #     words.extend(message.split())
    # return num_messages,len(words)
    # else:
    #     new_df = df[df['user'] == selected_user]
    #     num_messages = new_df.shape[0]
    #     words = []
    #     for message in new_df['message']:
    #         words.extend(message.split())
    #     return num_messages,len(words)
    #     ### also checkhow much a user active (messages ) and percentage
