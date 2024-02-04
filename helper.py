from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
extract = URLExtract()
def fetch_analyze(selected_user,df):

     if selected_user != 'overall':
         df = df[df['users'] == selected_user]

     number_msg = df.shape[0]
     audio_omitted_text = df[df['message'].str.contains('audio omitted', case=False, na=False)]
     video_omitted_text= df[df['message'].str.contains('video omitted', case=False, na=False)]
     image_omitted_text= df[df['message'].str.contains('image omitted', case=False, na=False)]
     words = []
     for message in df['message']:
        words.extend(message.split())


     link = []
     for message in df['message']:
         link.extend(extract.find_urls(message))


     return number_msg, len(words),audio_omitted_text.shape[0],video_omitted_text.shape[0],image_omitted_text.shape[0],len(link)


def most_active_users(df):

    x= df['users'].value_counts().head()
    df =round((df['users'].value_counts()/ df.shape[0]) * 100, 2).reset_index().rename(
        columns={'count': 'Percent', 'users': 'Names'})
    return x,df

def create_wordcloud(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'overall':
        df = df[df['users'] == selected_user]

    temp = df[~df['message'].str.contains('audio omitted\n', case=False, na=False)]
    temp = temp[~temp['message'].str.contains('video omitted\n', case=False, na=False)]
    temp = temp[~temp['message'].str.contains('image omitted\n', case=False, na=False)]
    temp = temp[~temp['message'].str.contains('sticker omitted\n', case=False, na=False)]
    temp = temp[~temp['message'].str.contains('This message was deleted.\n', case=False, na=False)]


    def remove_stop_word(message):
        y= []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)


    wc = WordCloud(width=500,height=500, min_font_size=10 , background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_word)
    df_wc= wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc



def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()


    if selected_user != 'overall':
        df = df[df['users'] == selected_user]

    temp = df[~df['message'].str.contains('audio omitted\n', case=False, na=False)]
    temp = temp[~temp['message'].str.contains('video omitted\n', case=False, na=False)]
    temp = temp[~temp['message'].str.contains('image omitted\n', case=False, na=False)]
    temp = temp[~temp['message'].str.contains('sticker omitted\n', case=False, na=False)]
    temp = temp[~temp['message'].str.contains('This message was deleted.\n', case=False, na=False)]

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    common_words = pd.DataFrame(Counter(words).most_common(20))
    return common_words


def emoji_helper(selected_user,df):


    if selected_user != 'overall':
        df = df[df['users'] == selected_user]

    emojis = []
    for message in df['message']:
            emojis.extend(c for c in message if c in emoji.EMOJI_DATA)

    all_emoji = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return all_emoji

def group_timeline(selected_user,df):
    if selected_user != 'overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year', 'month', 'month_name']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month_name'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline
def date_timeline(selected_user,df):
    df['date_only'] = df['dates'].dt.date
    if selected_user != 'overall':
        df = df[df['users'] == selected_user]

    timeline_daily = df.groupby(['date_only']).count()['message'].reset_index()
    return timeline_daily
def activity_day(selected_user,df):
    df['day_name'] = df['dates'].dt.day_name()
    if selected_user != 'overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts()


def activity_month(selected_user,df):
    if selected_user != 'overall':
        df = df[df['users'] == selected_user]

    return df['month_name'].value_counts()


def activity_heatmap(selected_user,df):
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period
    if selected_user != 'overall':
        df = df[df['users'] == selected_user]

    heat_table = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return heat_table

