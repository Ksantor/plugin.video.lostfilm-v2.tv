# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'lib'))

from common.plugin import plugin
from common.localized_error import LocalizedError

import lostfilm.routes

def launch():
  try:
    plugin.run()
  except LocalizedError as e:
    from kodiswift import xbmcgui
    e.log()
    if e.kwargs.get('dialog'):
        xbmcgui.Dialog().ok(
          plugin.get_string(30000),
          *e.localized.split("|")
        )
    else:
      plugin.notify(e.localized,
        plugin.get_string(30000),
        10000,
        plugin.addon.getAddonInfo('icon'))
    if e.kwargs.get('check_settings'):
        plugin.open_settings()

if __name__ == '__main__':
  launch()
