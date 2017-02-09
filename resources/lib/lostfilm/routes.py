# -*- coding: utf-8 -*-

import logging

from common.plugin import plugin
from lostfilm.authenticator import Authenticator
from lostfilm.scrappers.lostfilm_library_series import LostfilmLibrarySeries
from lostfilm.scrappers.lostfilm_library_episodes import LostfilmLibraryEpisodes

@plugin.route('/')
def index():
  Authenticator().enshure_authorize()

  plugin.set_content('tvshows')
  series = LostfilmLibrarySeries().list()
  plugin.add_items(series)
  plugin.finish()

@plugin.route('/serie_episodes/<serie_id>/<serie_code>')
def serie_episodes(serie_id, serie_code):
  Authenticator().enshure_authorize()

  plugin.set_content('episodes')
  episodes = LostfilmLibraryEpisodes(serie_id, serie_code).list()
  plugin.add_items(episodes)
  plugin.finish()

@plugin.route('/play_episode/<serie_id>/<season_number>/<episode_number>')
def play_episode(serie_id, season_number, episode_number):
  return
