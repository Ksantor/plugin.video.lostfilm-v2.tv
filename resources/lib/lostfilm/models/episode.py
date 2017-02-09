# -*- coding: utf-8 -*-

import datetime
import time

from collections import namedtuple
from common.plugin import plugin
from common.helpers import poster, fanart_image
from common.helpers import color

class Episode(namedtuple('Episode', ['serie_id', 'serie_code', 'season_number',
  'episode_number', 'title_en', 'title_ru', 'date', 'rating', 'watched'])):
  def item(self):
    return {
      'label': self.list_title,
      'path': self.episode_url,
      'is_playable': True,
      'thumbnail': poster(self.serie_id, self.season_number),
      'icon': None,
      'properties': {
          'fanart_image': fanart_image(self.serie_id),
      },
      'info': {
          'title': self.title,
          'originaltitle': self.title_en,
          'premiered': self.episode_date,
          'plot': None,
          'rating': self.rating,
          'studio': None,
          'castandrole': [],
          'writer': None,
          'director': None,
          'genre': None,
          'tvshowtitle': None,
          'year': None,
      }
    }

  @property
  def episode_url(self):
    return plugin.url_for('play_episode',
      serie_id = self.serie_id,
      season_number = self.season_number,
      episode_number = self.episode_number,
      select_quality = True
    )

  @property
  def episode_date(self):
    date = datetime.date(*(time.strptime(self.date, '%d.%m.%Y')[0:3]))
    return date.strftime('%Y-%m-%d')

    # str_to_date(release_date, '%d.%m.%Y %H:%M')
    # date_to_str(e.release_date, '%Y-%m-%d')

  # @property
  # def poster(self):
  #   return 'http://static.lostfilm.tv/Images/%s/Posters/shmoster_s%s.jpg' \
  #     % (self.serie_id, self.season_number)

  # @property
  # def fanart_image(self):
  #   return 'http://static.lostfilm.tv/Images/%s/Posters/poster.jpg' \
  #     % self.serie_id

  @property
  def list_title(self):
    if self.watched:
      return self.title
    else:
      return color(self.title, 'lime')

  @property
  def title(self):
    if plugin.get_setting('show-original-title', bool):
      return self.episode_number + '  -  ' + self.title_en
    else:
      return self.episode_number + '  -  ' + self.title_ru
