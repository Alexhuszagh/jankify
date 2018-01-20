# Jankify

A simple, easy-to-use script to generate text in the form of your favorite K-Pop blogger or Tweeter.

Includes:

- AsianJunkie
- Kpopalypse

## Getting Started

Run out-of-the-box using pre-scraped data from various blogs or Tweets. 

```python
>>> import jankify
>>>
>>> # load model from existing data
>>> asianjunkie_model = jankify.AsianJunkieCom.from_json()
>>>
>>> # make tweets
>>> asianjunkie_model.make_tweet()
"I told you I’m gonna kill you!"
>>> asianjunkie_model.make_sentence()
"What is news, however, is that relevant to this shit from me."
```

## Scraping Blogs

To fetch raw text from blogs, you may use `jankify.Blog.scrape` for an implementation from a blog.

The following classes support scraping:

- AsianJunkieCom
- KpopalypseCom

For example, to scrap all posts from `asianjunkie.com`, you would use:

```python
asianjunkie_model = jankify.AsianJunkieCom()
asianjunkie_model.scrape()
```

## Fetching Tweets

**Warning** In order to fetch Tweets, you must register a client application with Twitter from `https://developer.twitter.com/`. You must place these items in [tweepy.json](/data/tweepy.json).

```python
asianjunkie_model = jankify.AsianJunkieTweet()
asianjunkie_model.download()
```

## Training Models

Once data has been scraped, you may train the model using the `train()` member function. For example, using our `asianjunkie_model` above, you may use:

```python
asianjunkie_model.train()
```

## Generating Text

Jankify supports generating both custom Tweets (140 characters) and sentences. To generate a Tweet, call `make_tweet` after running the model. To generate a sentence, call `make_sentence`.

```python
>>> asianjunkie_model = jankify.AsianJunkieTweet()
>>> asianjunkie_model.download()
>>> asianjunkie_model.train()
>>> asianjunkie_model.make_tweet()
"I told you I’m gonna kill you!"
>>> asianjunkie_model.make_sentence()
"What is news, however, is that relevant to this shit from me."
```

## Saving/Loading Models

Models may be loaded or saved to JSON, a simple object notation similar to Python dictionaries. To load a model from JSON, call the classmethod `from_json`. To save a model to JSON, call the member function `to_json`.

```python
asianjunkie_model = jankify.AsianJunkieTweet()
asianjunkie_model.download()
asianjunkie_model.train()
asianjunkie_model.to_json()
copy = jankify.AsianJunkieTweet.from_json()
```

## License

Publid Domain
