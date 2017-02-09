# -*- coding: utf-8 -*-

from collections import namedtuple
from common.plugin import plugin
from common.helpers import poster, fanart_image
from common.helpers import color

class Serie(namedtuple('Serie', ['id', 'code', 'title_en', 'title_ru', 'total_episodes', 'watched_episodes'])):
  def item(self):
    return {
      'label': self.title,
      'path': self.serie_url,
      'is_playable': False,
      'thumbnail': poster(self.id),
      'properties': {
          'fanart_image': fanart_image(self.id),
      },
      'info': {
          'title': self.title,
          'episode': None,
          'original_title': self.title_en,
          'plot': None,
          'rating': None,
          'studio': None,
          'castandrole': [],
          'writer': None,
          'director': None,
          'genre': None,
          'tvshowtitle': None,
          'year': None,
      },
      'context_menu': self.context_menu
    }

  @property
  def context_menu(self):
    return [self.info_menu]

  @property
  def info_menu(self):
    return (plugin.get_string(40306), "Action(Info)")

  @property
  def serie_url(self):
    return plugin.url_for('serie_episodes', serie_id = self.id, serie_code = self.code)

  @property
  def title(self):
    if plugin.get_setting('show-original-title', bool):
      return '%s %s' % (self.title_en, self.unwatched_episode_count)
    else:
      return '%s %s' % (self.title_ru, self.unwatched_episode_count)

  @property
  def unwatched_episode_count(self):
    if int(self.total_episodes) == int(self.watched_episodes):
      return ''
    if int(self.total_episodes) == 0:
      return ''

    return ' (%s)' % color(int(self.total_episodes) - int(self.watched_episodes), 'lime')

