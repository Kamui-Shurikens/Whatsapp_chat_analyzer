from urlextract import URLExtract
extract = URLExtract()

from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

def get_stats(selected_user,df):

    if(selected_user == 'Overall'):

        words = 0;
        for msg in df['message']:
            words += len(msg.split(' '))

        media = df[df['message'] == '<Media omitted>\n'].shape[0]
        links = []
        for msg in df['message']:
            links.extend(extract.find_urls(msg))

        return df.shape[0],words,media,len(links)

    else:

        words = 0;
        for msg in df[df['user'] == selected_user ]['message']:
            words += len(msg.split(' '))
        tf = df[df['user'] == selected_user]
        media = tf[tf['message'] == '<Media omitted>\n'].shape[0]
        links = []
        for msg in tf['message']:
            links.extend(extract.find_urls(msg))
        return tf.shape[0],words,media,len(links)


def most_active(df):
    x = df['user'].value_counts()
    return x

def get_most20(selected_user,df):

    if(selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    f = open('hinglish_stop_words.txt')
    stop_words = f.read()
    stop_words = stop_words.split()
    f.close()

    df = df[df['user'] != 'group_notification']
    df = df[df['message'] != '<Media omitted>\n']

    words = []

    for msg in df['message']:
        for word in msg.split():
            if word not in stop_words:
                words.append(word)

    rf = pd.DataFrame(Counter(words).most_common(20))

    return rf

def get_emoji_df(selected_user,df):

    if(selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    emojis = []

    for msg in df['message']:
        emojis.extend([ch for ch in msg if ch in emoji.distinct_emoji_list(msg)])

    x = pd.DataFrame(Counter(emojis).most_common(10))
    return x

def get_monthly_stats(selected_user,df):
    if(selected_user != 'Overall'):
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline

def get_daily_stats(selected_user,df):
    if(selected_user != 'Overall'):
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['just_date']).count()['message'].reset_index()

    return timeline

def get_weekly_activity(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    x = df['day_name'].value_counts()
    return x

def get_monthly_activity(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    x = df['month'].value_counts()
    return x
