import tweepy
import pandas as pd
import config
import webbrowser

consumer_key=config.consumer_key
consumer_secret=config.consumer_secret
access_token = config.access_token
access_token_secret=config.access_token_secret
callback_uri='oob'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_uri)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
my_timeline = api.home_timeline()


def extract_timeline_as_df(timeline_list):
    columns=set()
    allowed_types=[int,str]
    tweets_data=[]
    for status in my_timeline:
        status_dict=dict(vars(status))
        keys=status_dict.keys()
        single_tweet_data={'user':status.user.screen_name,'author':status.author.screen_name}

        for k in keys:
            try:
                v_type=type(status_dict[k])
            except:
                v_type=None
            if v_type != None:
                if v_type in allowed_types:
                    single_tweet_data[k]=status_dict[k]
                    columns.add(k)
        tweets_data.append(single_tweet_data)
    header_cols=list(columns)
    header_cols.append('user')
    header_cols.append('author')

    df=pd.DataFrame(tweets_data, columns=header_cols)
    return(df)

user= api.get_user(screen_name='ShardiB2')
user_timeline=api.user_timeline(page=1)
df3=extract_timeline_as_df(user_timeline)

count=0
df1=pd.DataFrame()
list_of_tweets=[]
for pages in tweepy.Cursor(api.user_timeline, screen_name='ShardiB2').items(50):
    #a=extract_timeline_as_df(pages)
    # df1.append(a, ignore_index=True)
    count=count+1
    list_of_tweets.append(pages)
    print(count, pages)
df=pd.DataFrame(list_of_tweets)
df.to_excel("test.xlsx")