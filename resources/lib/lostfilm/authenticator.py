# -*- coding: utf-8 -*-

import os
import logging

from common.plugin import plugin
from common.network_request import NetworkRequest
from common.localized_error import LocalizedError

class Authenticator(NetworkRequest):
  def authorize(self):
    self.clear_cookies()

    response = self.post(url = self.POST_URL, data = self.login_data)
    json_response = response.json()

    if 'name' in json_response and json_response['success']:
      self.save_cookies(response.cookies)
    else:
      raise LocalizedError(32003, "Authorization failed", check_settings=True)

  @property
  def login_data(self):
    return {
      'act': 'users',
      'type': 'login',
      'rem': '1',
      'mail': plugin.get_setting('login', unicode),
      'pass': plugin.get_setting('password', unicode)
    }

  def enshure_authorize(self):
    if self.stored_cookies == None:
      self.authorize()
