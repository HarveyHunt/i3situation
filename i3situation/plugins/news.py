import webbrowser
import logging
import time
import json
import math
import random
from urllib.request import urlopen
from urllib.error import URLError
from i3situation.plugins._plugin import Plugin

__all__ = 'NewsPlugin'


class NewsPlugin(Plugin):
    """
    A plugin that displays information from BBC news on the status bar.
    Serves as a basis for more advanced web plugins.
    """

    def __init__(self, config):
        self.options = {'topics': ['uk', 'technology'], 'interval': 30, 'format': 'news time '}
        super().__init__(config)

    def main(self):
        """
        Actually fetch and process the data and then return it to the
        Status object.
        """
        if not hasattr(self, 'news'):
            self.news = self.get_news()
        self.article = self.get_random_article(self.news)
        if self.get_numberof_articles() == 1:
            self.news = self.get_news()
        output_text = self.options['format'].replace('time', self.get_age(self.article['published']))
        long_output = output_text.replace('news', self.article['description'])
        short_output = output_text.replace('news', self.article['title'])
        return self.output(long_output, short_output)

    def on_click(self, event):
        webbrowser.open(self.article['link'])

    def get_age(self, published_time):
        """
        Converts the published time (relevant to the epoch) into a human readable
        format.

        published_time: An integer representing the time that the article was
        published at. The time is relevant to the epoch.
        """
        minutes = math.floor((time.time() - published_time) / 60)
        if minutes > 1439:
            days = math.floor(minutes / 1440)
            if days > 1:
                return "{0} days ago".format(days)
            else:
                return "{0} day ago".format(days)
        if minutes > 59:
            hours = minutes / 60
            if hours >= 2:
                return "{0} hours ago".format(math.floor(hours))
            else:
                return "{0} hour ago".format(math.floor(hours))
        elif minutes < 1:
            return "Moments ago"
        else:
            return "{0} minutes ago".format(minutes)

    def get_news(self):
        """
        Connects to the BBC API, removes unnecessary data and returns a dictionary
        with topic for a key and stories for the values.
        """
        news = {}
        for topic in self.options['topics']:
            try:
                response = urlopen('http://api.bbcnews.appengine.co.uk/stories/{0}'.format(topic))
                json_obj = json.loads(response.read().decode())
                # Remove audio and video stories.
                json_obj['stories'] = [x for x in json_obj['stories'] if not 'VIDEO'
                                    in x['title'] and not 'AUDIO' in x['title']]
                # Remove thumbnails
                json_obj['stories'] = [dict({(k, v) for (k, v) in x.items() if k
                    not in 'thumbnail'}) for x in json_obj['stories']]
                # Rearrange the dictionary to allow multiple topics to coexist.
                news[json_obj['topic']['title']] = json_obj['stories']
            except URLError as e:
                logging.exception(e)
        return news

    def get_numberof_articles(self):
        """
        A helper function to check how many articles are left,
        in order to request new articles.
        """
        count = 0
        for topic in list(self.news):
            count += len(self.news[topic])
        return count

    def get_random_article(self, news):
        """
        Selects a random article from a random topic and removes it from the news
        dictionary.

        news: A dictionary of lists that contain articles (In the form of a
        dictationary).
        """
        topic = random.choice(list(self.news))
        article = random.choice(self.news[topic])
        del self.news[topic][self.news[topic].index(article)]
        return article
