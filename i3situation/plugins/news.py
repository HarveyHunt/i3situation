import webbrowser
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
            self.news = self.getNews()
        self.article = self.getRandomArticle(self.news)
        if self.getNumberofArticles() == 1:
            self.news = self.getNews()
        outputText = self.options['format'].replace('time', self.getAge(self.article['published']))
        longOutput = outputText.replace('news', self.article['description'])
        shortOutput = outputText.replace('news', self.article['title'])
        return self.output(longOutput, shortOutput)

    def onClick(self, event):
        webbrowser.open(self.article['link'])

    def getAge(self, publishedTime):
        """
        Converts the published time (relevant to the epoch) into a human readable
        format.
        """
        minutes = math.floor((time.time() - publishedTime) / 60)
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

    def getNews(self):
        """
        Connects to the BBC API, removes unnecessary data and returns a dictionary
        with topic for a key and stories for the values.
        """
        news = {}
        for topic in self.options['topics']:
            try:
                response = urlopen('http://api.bbcnews.appengine.co.uk/stories/{0}'.format(topic))
                jsonObj = json.loads(response.read().decode())
                # Remove audio and video stories.
                jsonObj['stories'] = [x for x in jsonObj['stories'] if not 'VIDEO'
                                    in x['title'] and not 'AUDIO' in x['title']]
                # Remove thumbnails
                jsonObj['stories'] = [dict({(k, v) for (k, v) in x.items() if k
                    not in 'thumbnail'}) for x in jsonObj['stories']]
                # Rearrange the dictionary to allow multiple topics to coexist.
                news[jsonObj['topic']['title']] = jsonObj['stories']
            except URLError as e:
                logging.exception(e)
        return news

    def getNumberofArticles(self):
        """
        A helper function to check how many articles are left,
        in order to request new articles.
        """
        count = 0
        for topic in list(self.news):
            count += len(self.news[topic])
        return count

    def getRandomArticle(self, news):
        """
        Selects a random article from a random topic and removes it from the news
        dictionary.
        """
        topic = random.choice(list(self.news))
        article = random.choice(self.news[topic])
        del self.news[topic][self.news[topic].index(article)]
        return article
