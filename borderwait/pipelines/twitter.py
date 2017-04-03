import tweepy, os, requests, random

# Tweet about the new item
class TwitterPipeline(object):
    def __init__(self, tw_consumer_key, tw_consumer_secret, tw_access_token, tw_access_token_secret, tw_gifs, path_to_gifs):
        self.tw_consumer_key = tw_consumer_key
        self.tw_consumer_secret = tw_consumer_secret
        self.tw_access_token = tw_access_token
        self.tw_access_token_secret = tw_access_token_secret
        self.tw_gifs = tw_gifs
        self.path_to_gifs = path_to_gifs
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            tw_consumer_key=crawler.settings.get('TWITTER_CONSUMER_KEY'),
            tw_consumer_secret=crawler.settings.get('TWITTER_CONSUMER_SECRET'),
            tw_access_token=crawler.settings.get('TWITTER_ACCESS_TOKEN'),
            tw_access_token_secret=crawler.settings.get('TWITTER_ACCESS_TOKEN_SECRET'),
            tw_gifs=crawler.settings.get('WAIT_TIME_GIF_URLS'),
            path_to_gifs=crawler.settings.get('GIFS_DIRECTORY')
        )

    def open_spider(self, spider):
        tw_auth = tweepy.OAuthHandler(self.tw_consumer_key, self.tw_consumer_secret)
        tw_auth.set_access_token(self.tw_access_token, self.tw_access_token_secret)
        self.tweepy_api = tweepy.API(tw_auth)

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        border = item['border']
        entry_min = item['entry']['min']
        entry_max = item['entry']['max']
        exit_min = item['exit']['min']
        exit_max = item['exit']['max']

        def get_feeling(max_min):
            feeling = ['great','ok','bad','horrible']
            feeling_great=range(0,6)
            feeling_ok=(6,11)
            feeling_bad=(11,46)
            if max_min in feeling_great:
                return feeling[0]
            elif max_min in feeling_ok:
                return feeling[1]
            elif max_min in feeling_bad:
                return feeling[2]
            else:
                return feeling[3]

        def get_random_feeling_path(feeling):
            filelist = [ f for f in os.listdir('%s/%s/'%(self.path_to_gifs, feeling)) if f.endswith(".gif") ]
            path = random.choice(filelist)
            return '%s/%s/%s'%(self.path_to_gifs, feeling, path)

        def tweet_gif(path, message):
            self.tweepy_api.update_with_media(path, status=message)

        entry_feeling = get_feeling(entry_max)
        exit_feeling = get_feeling(exit_max)

        if entry_feeling is exit_feeling:
            # Generate 1 tweet message for both entry and exit.
            gif_path = get_random_feeling_path(entry_feeling)
            tw_message = 'Kufiri #%s: pritja 'u'\xeb''sht'u'\xeb'' %s deri %s minuta p'u'\xeb''r t'u'\xeb'' hyr'u'\xeb'' n'u'\xeb'' #Kosov'u'\xeb'' dhe %s deri %s minuta p'u'\xeb''r t'u'\xeb'' dalur.\n #Mir'u'\xeb''sevini #Rrug'u'\xeb''T'u'\xeb''Mbar'u'\xeb''' % (border,str(entry_min), str(entry_max), str(exit_min), str(exit_max))
            # tweet
            tweet_gif(gif_path, tw_message)
        else:
            # Generate 2 tweet messages: one for entry and one for exit.
            gif_path_entry = get_random_feeling_path(entry_feeling)
            gif_path_exit = get_random_feeling_path(exit_feeling)

            tw_message_entry = 'Kufiri #%s: pritja 'u'\xeb''sht'u'\xeb'' %s deri %s minuta p'u'\xeb''r t'u'\xeb'' hyr'u'\xeb'' n'u'\xeb'' #Kosov'u'\xeb''. #Mir'u'\xeb''sevini' % (border,str(entry_min), str(entry_max))
            tw_message_exit = 'Kufiri #%s: pritja 'u'\xeb''sht'u'\xeb'' %s deri %s minuta p'u'\xeb''r t'u'\xeb''dal'u'\xeb'' nga #Kosova. #Rrug'u'\xeb''T'u'\xeb''Mbar'u'\xeb''' % (border, str(exit_min), str(exit_max))

            # tweet
            tweet_gif(gif_path_entry, tw_message_entry)
            tweet_gif(gif_path_exit, tw_message_exit)
        return item
