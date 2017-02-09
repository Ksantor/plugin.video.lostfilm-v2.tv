# -*- coding: utf-8 -*-

def color(title, color_val):
  return "[COLOR %s]%s[/COLOR]" % (color_val, title)

def poster(serie_id, season_number = 1):
  return 'http://static.lostfilm.tv/Images/%s/Posters/shmoster_s%d.jpg' % \
    (serie_id, season_number)

def fanart_image(serie_id):
  return 'http://static.lostfilm.tv/Images/%s/Posters/poster.jpg' % serie_id
