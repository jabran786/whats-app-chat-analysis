

import re
import pandas as pd
# import pandas as pd
"""
Created on Tue Apr 25 19:40:13 2023

@author: STAR PC11
"""

def proprocess(data):
    #             {date,                ,time          , }
    pattren = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s\w{2}\s-'
#pattern = r'\d{1,2}\/\d{1,2}\/\d{1,2}, \d{1,2}:\d{2} (AM|PM) - \s.*'
    messages = re.split(pattren, data)[1:]
    dates = re.findall(pattren,data)
    df = pd.DataFrame({'user_message':messages,'message_date':dates})
#conver message date type 
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p -')
#df.rename(columns={'message_date': 'date'}, inplace=True)
#df['date'] = df['date'].dt.strftime('%d-%m-%y %I:%M:%S %p')
#again conver date to date time format currently in string
    # Separate users and messages
    users = []
    messages=[]
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s',message)
        if entry[1:]:#User name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
            
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['only_date'] = df['message_date'].dt.date
    df['year'] = df['message_date'].dt.year
    df['month_num'] = df['message_date'].dt.month
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    #for activity map
    df['day_name']  = df['message_date'].dt.day_name()
    #
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute

    # column to create heat map

    period = []
    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 00:
            period.append(str('00') + "-" + str(hour))
        else:
            period.append(str(hour) + "-" + str(hour+1))
    df['period'] = period
    
    return df