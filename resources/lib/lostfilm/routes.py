# -*- coding: utf-8 -*-

import logging

from common.plugin import plugin
from lostfilm.authenticator import Authenticator
from lostfilm.scrappers.lostfilm_series import LostfilmSeries

@plugin.route('/')
def index():
  Authenticator().enshure_authorize()

  plugin.set_content('tvshows')
  series = LostfilmSeries().list()
  plugin.add_items(series)
  plugin.finish()
