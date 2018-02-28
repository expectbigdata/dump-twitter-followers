import os
from configparser import ConfigParser

"""
Slightly modified from TweetRc class found in python-twitter's examples
(https://github.com/bear/python-twitter/blob/master/examples/tweet.py)
"""
class TweetRc(object):
	def __init__(self, rcPath):
		self._config = None
		if rcPath:
			self._loadConfigFrom(rcPath)

	def getConsumerKey(self):
		return self._getOption('consumer_key')

	def getConsumerSecret(self):
		return self._getOption('consumer_secret')

	def getAccessToken(self):
		return self._getOption('access_token')

	def getAccessSecret(self):
		return self._getOption('access_secret')

	def _getOption(self, option):
		try:
			return self._getConfig().get('Tweet', option)
		except:
			return None

	def _getConfig(self):
		if not self._config:
			self._loadConfigFrom('~/.tweetrc')
		return self._config
	
	def _loadConfigFrom(self, rcPath):
		self._config = ConfigParser()
		self._config.read(os.path.expanduser(rcPath))

