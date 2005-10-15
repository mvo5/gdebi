#!/usr/bin/env python

from distutils.core import setup
import glob
import os

GETTEXT_NAME="gdebi"
I18NFILES = []
#for filepath in glob.glob("po/mo/*/LC_MESSAGES/*.mo"):
#    lang = filepath[len("po/mo/"):]
#    targetpath = os.path.dirname(os.path.join("share/locale",lang))
#    I18NFILES.append((targetpath, [filepath]))

# HACK: make sure that the mo files are generated and up-to-date
#os.system("cd po; make update-po")
    
setup(name='gdebi', version='0.1',
      packages=['GDebi'],
      scripts=['gdebi'],
      data_files=[('share/gdebi/',
                   ["data/gdebi.glade"]),
                  ('share/applications',
                   ["data/gdebi.desktop"]),
                  ('share/application-registry',
		   ["data/gdebi.applications"]),
                  ('share/pixmaps',
                   ["data/gdebi.png"])]+I18NFILES,
      )


