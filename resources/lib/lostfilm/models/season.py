# -*- coding: utf-8 -*-

from collections import namedtuple
from common.plugin import plugin
from common.helpers import poster, fanart_image

class Season(namedtuple('Season', ['serie_id', 'serie_code', 'season_number'])):
  def item(self):
    return {
      'label': self.season_title,
      'path': self.season_url,
      'is_playable': False,
      'thumbnail': poster(self.serie_id, self.season_number),
      'properties': {
          'fanart_image': fanart_image(self.serie_id),
      }
    }

  @property
  def season_title(self):
    if plugin.get_setting('show-original-title', bool):
      return 'Season %d' % self.season_number
    else:
      return '%d сезон' % self.season_number

  @property
  def season_url(self):
    return plugin.url_for('serie_episodes', serie_id = self.serie_id, serie_code = self.serie_code)
