# -*- coding: utf-8 -*-

import logging
import re
import CommonFunctions

from common.plugin import plugin
from common.network_request import NetworkRequest
from lostfilm.models.season import Season
from lostfilm.models.episode import Episode

class LostfilmLibraryEpisodes(object):
  def __init__(self, serie_id, serie_code):
    self.network_request = NetworkRequest()
    self.parsedom = CommonFunctions
    self.serie_id = serie_id
    self.serie_code = serie_code
    self.episode_list_items = []
    self.season_numbers = []

  def list(self):
    url = self.network_request.base_url + '/series/%s/seasons' % self.serie_code
    response = self.network_request.get(url)

    seasons = self.seasons(response.text)
    for season in seasons:
      season_number = self.season_number(season)
      if not season_number:
        continue
      self.append_season_header(season_number)

      season_episodes = self.season_episodes(season)
      watched_episodes = self.watched_episodes()

      for episode in season_episodes:
        self.append_season_episode(episode, season_number, watched_episodes)

    return self.episode_list_items


  # Seasons
  def seasons(self, dom):
    return self.parsedom.parseDOM(dom,
      'div', attrs = { 'class': 'serie-block' })

  def season_number(self, dom):
    season_title = self.parsedom.parseDOM(dom, 'h2')
    season_title = season_title[0].encode('utf-8')
    match = re.search('(\d+) сезон', season_title)

    if not match:
      return None
    else:
      return int(match.group(1))

  def append_season_header(self, season_number):
    self.season_numbers.append(season_number)
    season_data = [self.serie_id, self.serie_code, season_number]
    self.episode_list_items.append(Season(*season_data).item())


  # Episodes
  def season_episodes(self, dom):
    table = self.parsedom.parseDOM(dom,
      'table', attrs = { 'class': 'movie-parts-list' })

    return self.parsedom.parseDOM(table, 'tr')

  def append_season_episode(self, episode, season_number, watched_episodes):
    episode_number = self.episode_number(episode)
    title_en, title_ru = self.episode_titles(episode)
    date = self.episode_date(episode)
    rating = self.episode_rating(episode)

    episode_watched = False
    if len(watched_episodes) > 0:
      episode_watched = self.episode_watched(
        season_number,
        episode_number,
        watched_episodes['data']
      )

    episode_data = [
      self.serie_id,
      self.serie_code,
      season_number,
      episode_number,
      title_en,
      title_ru,
      date,
      rating,
      episode_watched
    ]
    logging.warning(episode_data)

    self.episode_list_items.append(Episode(*episode_data).item())

  def episode_number(self, dom):
    td = self.parsedom.parseDOM(dom, 'td', attrs = { 'class': 'beta' })
    number = re.search('(\d+) серия', td[0].encode('utf-8'))
    if number:
      return number.group(1)
    else:
      return 999

  def episode_titles(self, dom):
    td = self.parsedom.parseDOM(dom, 'td', attrs = { 'class': 'gamma' })
    title_en = self.parsedom.parseDOM(td[0], 'span')[0]
    title_ru = re.search('([^>])(.*)(?=\<br)', td[0].encode('utf-8')).group(2).lstrip()

    return title_en, title_ru

  def episode_date(self, dom):
    td = self.parsedom.parseDOM(dom, 'td', attrs = { 'class': 'delta' })
    return re.search('(Ru:\ )(\d{2}.\d{2}.\d{4})', td[0]).group(2)

  def episode_rating(self, dom):
    return self.parsedom.parseDOM(dom, 'div', attrs = { 'class': 'mark-green-box' })[0]

  def watched_episodes(self):
    data = {
      'act': 'serial',
      'type': 'getmarks',
      'id': self.serie_id
    }
    url = self.network_request.post_url
    response = self.network_request.post(url, data = data)

    return response.json()

  def episode_watched(self, season_number, episode_number, watched_episodes):
    separator = '-'
    serie_episode_id = separator.join((
      str(self.serie_id),
      str(season_number),
      str(episode_number)
    ))

    if serie_episode_id in watched_episodes:
      return True
    else:
      return False
