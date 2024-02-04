import re
import pandas as pd

def preprocess(data):
    pattern = '\[\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}:\d{2} [A-Za-z]*]'
    messages = re.split(pattern, data)[1:]
    units = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'dates': units})
    df['dates'] = pd.to_datetime(df['dates'], format='[%d/%m/%y, %I:%M:%S %p]')
    users = []
    message = []
    for messages in df['user_message']:
        entry = re.split('([\w\W]+?):\s', messages)
        if entry[1:]:
            users.append(entry[1])
            message.append(entry[2])
        else:
            users.append('group_notification')
            message.append(entry[0])

    df['users'] = users
    df['message'] = message
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['dates'].dt.year
    df['month'] = df['dates'].dt.month
    df['day'] = df['dates'].dt.day
    df['hour'] = df['dates'].dt.hour
    df['minutes'] = df['dates'].dt.minute
    df['seconds'] = df['dates'].dt.second
    df['month_name'] = df['dates'].dt.month_name()

    return df