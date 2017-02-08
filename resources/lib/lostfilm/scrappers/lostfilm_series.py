# -*- coding: utf-8 -*-

import logging
import re
import CommonFunctions

from common.network_request import NetworkRequest
from lostfilm.models.serie import Serie

class LostfilmSeries(object):
  def __init__(self):
    self.network_request = NetworkRequest()
    self.parsedom = CommonFunctions

  def list(self):
    response = self.network_request.get(self.network_request.base_url + '/my/type_1')
    rows = self.serial_rows(response.text)
    series_list_items = []

    for row in rows:
      title_en, title_ru = self.serie_titles(row)
      total_episodes_count, watched_episodes_count = self.series_episode_count(row)

      series_data = [
        self.serie_id(row),
        self.serie_code(row),
        title_en,
        title_ru,
        total_episodes_count,
        watched_episodes_count
      ]

      series_list_items.append(Serie(*series_data).item())

    return series_list_items

  def serial_rows(self, dom):
    serials_list_box = self.parsedom.parseDOM(dom,
      'div', attrs = { 'class': 'serials-list-box' })
    rows = self.parsedom.parseDOM(serials_list_box,
      'div', attrs = { 'class': 'serial-box' })
    return rows

  def serie_id(self, dom):
    id_attr = self.parsedom.parseDOM(dom,
      'div', attrs = { 'class': 'subscribe-box' }, ret = 'id')

    if not id_attr:
      id_attr = self.parsedom.parseDOM(dom,
        'div', attrs = { 'class': 'subscribe-box active' }, ret = 'id')

    series_id = re.search('(\d+)', id_attr[0]) if id_attr[0] else ''
    return series_id.group(1) if series_id else 000

  def serie_code(self, dom):
    href_attr = self.parsedom.parseDOM(dom,
      'a', attrs = { 'href': '/series/.+?', 'class': 'body' }, ret = 'href')
    series_code = re.search('([^/]+$)', href_attr[0]) if href_attr[0] else ''

    return series_code.group(1) if series_code else ''

  def serie_titles(self, dom):
    link = self.parsedom.parseDOM(dom,
      'a', attrs = { 'href': '/series/.+?', 'class': 'body' })
    title_en = self.parsedom.parseDOM(link,
      'div', attrs = { 'class': 'title-en' })
    title_ru = self.parsedom.parseDOM(link,
      'div', attrs = { 'class': 'title-ru' })

    return title_en[0].encode('utf-8'), title_ru[0].encode('utf-8')

  def series_episode_count(self, dom):
    episode_bar_pane = self.parsedom.parseDOM(dom,
      'div', attrs = { 'class': 'bar-pane' })

    total_episodes_bar = self.parsedom.parseDOM(episode_bar_pane,
      'div', attrs = { 'class': 'bar' })
    total_episodes_count = self.parsedom.parseDOM(total_episodes_bar,
      'div', attrs = { 'class': 'value' })
    if total_episodes_count[0] == '':
      total_episodes_count[0] = 0

    watched_episodes_bar = self.parsedom.parseDOM(episode_bar_pane,
      'div', attrs = { 'class': 'bar-active' })
    watched_episodes_count = self.parsedom.parseDOM(watched_episodes_bar,
      'div', attrs = { 'class': 'value' })
    if watched_episodes_count[0] == '':
      watched_episodes_count[0] = 0

    return total_episodes_count[0], watched_episodes_count[0]
