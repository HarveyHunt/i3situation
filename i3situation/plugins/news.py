from i3situation.plugins._plugin import Plugin
import time
import json
import math
import random
from urllib.request import urlopen
from urllib.error import URLError

__all__ = 'NewsPlugin'


class NewsPlugin(Plugin):
    """
    A plugin that displays information from BBC news on the status bar.
    Serves as a basis for more advanced web plugins.
    """

    def __init__(self, config):
        self.options = {'topics': ['uk', 'technology'], 'interval': 2}
        super().__init__(config, self.options)

    def main(self):
        """
        Actually fetch and process the data and then return it to the
        Status object.
        """
        if not hasattr(self, 'news'):
            self.news = self.getNews()
        self.article = self.getRandomArticle(self.news)
        if round(time.time()) % 1 == 0:
            self.article = self.getRandomArticle(self.news)
        if self.getNumberofArticles() == 1:
            self.news = self.getNews()
        return self.output(self.article['description'] + '   ' + self.getAge(
            self.article['published']), self.article['title'] + '   ' +
            self.getAge(self.article['published']))

    def getAge(self, pubTime):
        """
        Converts the published time (relevant to the epoch) into a human readable
        format.
        """
        minutes = math.floor((time.time() - pubTime) / 60)
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
                # Remove thumbnail information, audio and video stories.
                jsonObj['stories'] = [x for x in jsonObj['stories'] if not 'VIDEO'
                                    in x['title'] and not 'AUDIO' in x['title']]
                for index, story in enumerate(jsonObj['stories']):
                    del jsonObj['stories'][index]['thumbnail']
                    del jsonObj['stories'][index]['link']
                # Rearrange the dictionary to allow multiple topics to coexist.
                news[jsonObj['topic']['title']] = jsonObj['stories']
            except URLError as e:
                print('Broken: {0}'.format(e))
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
