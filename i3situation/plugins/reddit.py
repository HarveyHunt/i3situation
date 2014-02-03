import html.parser
import webbrowser
import requests
from i3situation.plugins._plugin import Plugin

__all__ = 'RedditPlugin'


class RedditPlugin(Plugin):
    """
    A plugin to display data from Reddit. The submissions on the front page can
    be displayed as well as the submissions on selected subreddits. The format
    options can contain the following keywords that will be replace at run time:

    link_flair_css_class
    approved_by
    num_reports
    num_comments
    author_flair_css_class
    link_flair_text
    ups
    author_flair_text
    permalink
    selftext
    domain
    subreddit_id
    over_18
    secure_media
    name
    media
    clicked
    score
    is_self
    stickied
    distinguished
    media_embed
    subreddit
    edited
    selftext_html
    banned_by
    likes
    created_utc
    hidden
    url
    id
    downs
    thumbnail
    author
    secure_media_embed
    title
    saved
    """

    def __init__(self, config):
        self.options = {'mode': 'front', 'color': '#FFFFFF', 'interval': 30,
                        'subreddits': ['vim', 'python'], 'username': None,
                        'password': None, 'limit': 25, 'format': '[subreddit] title ↑ups',
                        'sort': 'hot'}
        super().__init__(config)
        if isinstance(self.options['subreddits'], str):
            self.options['subreddits'] = [self.options['subreddits']]
        self.h = html.parser.HTMLParser()
        self.client = requests.session()
        self.client.headers.update({'user-agent': 'i3situation reddit plugin'})

    def main(self):
        """
        Generates an output string by replacing the keywords in the format
        string with the corresponding values from a submission dictionary.
        """
        self.manage_submissions()
        out_string = self.options['format']
        self.selected_submission = self.submissions.pop()
        for k, v in self.selected_submission.items():
            out_string = out_string.replace(k, str(v))
        return self.output(out_string, out_string)

    def on_click(self, event):
        # FIXME: The webbrowser module decides to allow firefox to dump
        # everything to STDOUT/ERR and this messes with i3bar.
        webbrowser.open(self.selected_submission['url'])

    def login(self):
        """
        Logs into Reddit in order to display a personalised front page.
        """
        data = {'user': self.options['username'], 'passwd':
                self.options['password'], 'api_type': 'json'}
        response = self.client.post('http://www.reddit.com/api/login', data=data)
        self.client.modhash = response.json()['json']['data']['modhash']

    def manage_submissions(self):
        """
        If there are no or only one submissions left, get new submissions.
        This function manages URL creation and the specifics for front page
        or subreddit mode.
        """
        if not hasattr(self, 'submissions') or len(self.submissions) == 1:
            self.submissions = []
            if self.options['mode'] == 'front':
                # If there are no login details, the standard front
                # page will be displayed.
                if self.options['password'] and self.options['username']:
                    self.login()
                url = 'http://reddit.com/.json?sort={0}'.format(self.options['sort'])
                self.submissions = self.get_submissions(url)
            elif self.options['mode'] == 'subreddit':
                for subreddit in self.options['subreddits']:
                    url = 'http://reddit.com/r/{0}/.json?sort={1}'.format(
                        subreddit, self.options['limit'])
                    self.submissions += self.get_submissions(url)
        else:
            return

    def get_submissions(self, url):
        """
        Connects to Reddit and gets a JSON representation of submissions.
        This JSON data is then processed and returned.

        url: A url that requests for submissions should be sent to.
        """
        response = self.client.get(url, params={'limit': self.options['limit']})
        submissions = [x['data'] for x in response.json()['data']['children']]
        return submissions
