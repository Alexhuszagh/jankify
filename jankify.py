'''
    jankify
    -------

    Trolling AsianJunkie, as a service.
'''

import abc
import json
import re
import os
import time

import markovify
import requests
import six
import tweepy
from bs4 import BeautifulSoup

# HELPERS
# -------

HOME = os.path.dirname(os.path.realpath(__file__))

def get_soup(session, url):
    '''Get BeautifulSoup from URL'''

    response = session.get(url)
    return BeautifulSoup(response.text, 'html.parser')


# OBJECTS
# -------

# GENERIC MODELS


@six.add_metaclass(abc.ABCMeta)
class Model:
    '''Generalized model'''

    def __init__(self):
        self.posts = []
        self.model = None

    @abc.abstractproperty
    def path(self):
        '''Abstract path for data storage.'''

    def train(self):
        '''Train Markov models based on input text'''

        if self.model is not None:
            return

        models = []
        for post in self.posts:
            try:
                model = markovify.Text(post)
                models.append(model)
            except KeyError:
                print(len(models))

        self.model = markovify.combine(models)

    def to_json(self):
        '''Export data to JSON.'''

        d = {'posts': self.posts}
        if self.model is not None:
            d['model'] = self.model.to_dict()

        with open(self.path, 'w') as f:
            json.dump(d, f)

    def load_json(self):
        '''Load data from JSON.'''

        with open(self.path, 'r') as f:
            d = json.load(f)

        self.posts = d['posts']
        if 'model' in d:
            self.model = markovify.Text.from_dict(d['model'])

    @classmethod
    def from_json(cls):
        '''Create class from JSON data'''

        inst = cls()
        inst.load_json()
        return inst

    def make_tweet(self):
        '''Make 140 character Tweet.'''

        if self.model is None:
            self.train()

        return self.model.make_short_sentence(140)

    def make_sentence(self):
        '''Make generic sentence.'''

        if self.model is None:
            self.train()

        return self.model.make_sentence()


class Blog(Model):
    '''Model for blog material.'''

    def __init__(self):
        self.session = requests.Session()
        super(Blog, self).__init__()

    @abc.abstractproperty
    def host(self):
        '''Get the host name for the service.'''

    @abc.abstractproperty
    def timeout(self):
        '''Optional timeout to avoid rate limiting.'''

    @abc.abstractmethod
    def get_last_post(self):
        '''Get last post from blog.'''

    @abc.abstractmethod
    def get_previous_post(self, soup):
        '''Extract previous post from BeautifulSoup'''

    @abc.abstractmethod
    def extract_text(self, soup):
        '''Extract blog text from BeautifulSoup'''

    def scrape_from(self, url):
        '''Scrape from existing URL'''

        try:
            while (url):
                print(url)
                soup = get_soup(self.session, url)
                self.posts.append(self.extract_text(soup))
                url = self.get_previous_post(soup)
                time.sleep(self.timeout)
        except:
            print("Error occurred, current place is: {}".format(url))

    def scrape(self):
        '''Scrape all posts on blog.'''

        url = self.get_last_post()
        self.scrape_from(url)


class Twitter(Model):
    '''Model for Twitter material.'''

    def __init__(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_key, self.access_secret)
        self.api = tweepy.API(auth)
        super(Twitter, self).__init__()

    @abc.abstractproperty
    def screen_name(self):
        '''Get the screen_name to download Tweets from.'''

    @property
    def auth(self):
        if not hasattr(self, '_auth'):
            with open(os.path.join(HOME, 'data', 'tweepy.json')) as f:
                self._auth = json.load(f)
        return self._auth

    @property
    def consumer_key(self):
        return self.auth['consumerKey']

    @property
    def consumer_secret(self):
        return self.auth['consumerSecret']

    @property
    def access_key(self):
        return self.auth['accessKey']

    @property
    def access_secret(self):
        return self.auth['accessSecret']

    def fetch(self, oldest=None):
        '''Fetch 200 most recent Tweets from oldest Tweet.'''

        kwds = {
            'screen_name': self.screen_name,
            'count': 200
        }
        if oldest is not None:
            kwds['max_id'] = oldest
        return self.api.user_timeline(**kwds)

    def download_from(self, oldest):
        '''Download Tweets from existing ID'''

        while True:
            print(oldest)
            tweets = self.fetch(oldest)
            if not tweets:
                return
            oldest = tweets[-1].id - 1
            text = [re.sub(r"(?:http\S+)|(?:@\S+)", "", i.text) for i in tweets]
            self.posts += text

    def download(self):
        '''Download all Tweets from user.'''

        self.download_from(None)


# SPECIALIZED MODELS


class AsianJunkieCom(Blog):
    '''Blog model for "asianjunkie.com"'''

    @property
    def host(self):
        return "http://asianjunkie.com"

    @property
    def timeout(self):
        return 0

    @property
    def path(self):
        return os.path.join(HOME, 'data', 'asianjunkie_com.json')

    def get_last_post(self):
        soup = get_soup(self.session, self.host)
        post = soup.find(class_='post-box-title')
        return post.a['href']

    def get_previous_post(self, soup):
        post = soup.find(class_='post-previous')
        if post is None or getattr(post, 'a', None) is None:
            return
        return post.a['href']

    def extract_text(self, soup):
        entry = soup.find(class_='entry')
        paragraphs = entry.find_all('p')
        text = [i.get_text() for i in paragraphs]
        return '\n'.join([i for i in text if i])


class KpopalypseCom(Blog):
    '''Blog model for "kpopalypse.com"'''

    @property
    def host(self):
        return "https://kpopalypse.com"

    @property
    def timeout(self):
        return 0.1

    @property
    def path(self):
        return os.path.join(HOME, 'data', 'kpopalypse_com.json')

    def get_last_post(self):
        soup = get_soup(self.session, self.host)
        post = soup.find(class_='entry-title')
        return post.a['href']

    def get_previous_post(self, soup):
        post = soup.find(class_='previous')
        if post is None or getattr(post, 'a', None) is None:
            return
        return post.a['href']

    def extract_text(self, soup):
        entry = soup.find(class_='entry-content')
        paragraphs = entry.find_all('p')
        text = [i.get_text() for i in paragraphs]
        return '\n'.join([i for i in text if i])


class AsianJunkieTweet(Twitter):
    '''Twitter model for AsianJunkie'''

    @property
    def screen_name(self):
        return 'asianjunkiecom'

    @property
    def path(self):
        return os.path.join(HOME, 'data', 'asianjunkie_twitter.json')


class KpopalypseTweet(Twitter):
    '''Twitter model for Kpopalypse'''

    @property
    def screen_name(self):
        return 'kpopalypse'

    @property
    def path(self):
        return os.path.join(HOME, 'data', 'kpopalypse_twitter.json')
