import tweepy
#override tweepy.StreamListener to add logic to on_status

consumer_key='25PeAiNHtlhhJos5geyPlWRTK'
consumer_secret='W9jwJZls4USmXjWD0KreCEMG7QWkPYdFAlT6jqwrzj4b1zctyj'
access_token = '2383095896-YhxBDJD2jpgEuKvaFF9SN5z34A0AA3wrdy1jwtk'
access_token_secret='2OOPD0gB5LYIK8an5gqtU2wwLzF8UYQ7n4rEUyz7yhAZe'
callback_uri='oob'

class MaxListener(tweepy.Stream):

    def on_status(self, status):
        print(status.text)

    def process_data(self, raw_data):
        print(raw_data)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False
class MaxSream():
    def __init__(self, auth, listener):
        self.stream=tweepy.Stream(auth = auth, listener=listener())

    def start(self, keyword_list):
        self.stream.filter(track=keyword_list)


if __name__=='__main__':
    listener=MaxListener()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_uri)
    auth.set_access_token(access_token, access_token_secret)
    stream=MaxStream(auth, listener)
    stream.start(['python'])