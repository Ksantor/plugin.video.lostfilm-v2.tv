# -*- coding: utf-8 -*-

import os
import logging
import requests

from requests import Timeout, RequestException
from common.plugin import plugin
from common.localized_error import LocalizedError

class NetworkRequest(object):
  USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
  BASE_URL = 'https://www.lostfilm.tv'
  POST_URL = 'https://www.lostfilm.tv/ajaxik.php'

  def __init__(self):
    self.session = requests.Session()
    self.session.headers['User-Agent'] = self.USER_AGENT

  @property
  def base_url(self):
    return self.BASE_URL

  @property
  def post_url(self):
    return self.POST_URL

  def get(self, url, params=None):
    try:
      response = self.session.get(url, params=params, cookies=self.stored_cookies)

      return response
    except Timeout as e:
      raise self.timeout_error(e, url)
    except RequestException as e:
      raise self.exception_error(e, url)

  def post(self, url, data=None):
    try:
      response = self.session.post(url, data=data, cookies=self.stored_cookies)

      return response
    except Timeout as e:
      raise self.timeout_error(e, url)
    except RequestException as e:
      raise self.exception_error(e, url)

  def timeout_error(self, e, url):
    LocalizedError(32000, "Timeout while fetching URL: %s (%%s)" % url,
      plugin.get_string(30000), cause=e)

  def exception_error(self, e, url):
    LocalizedError(32001, "Can't fetch URL: %s (%%s)" % url,
      plugin.get_string(30000), cause=e)

  def clear_cookies(self):
    if self.session.cookies.get('lf_session'):
      self.session.cookies.clear('.lostfilm.tv')

  def save_cookies(self, cookie_jar):
    self.cookie_store['cookie_jar'] = cookie_jar

  @property
  def stored_cookies(self):
    return self.cookie_store.get('cookie_jar')

  @property
  def cookie_store(self):
    return plugin.get_storage('lostfilm', ttl=60)
