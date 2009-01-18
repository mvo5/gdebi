#!/usr/bin/env python

from distutils.core import setup
import glob
import os
import re

# look/set what version we have
changelog = "debian/changelog"
if os.path.exists(changelog):
    head=open(changelog).readline()
    match = re.compile(".*\((.*)\).*").match(head)
    if match:
        version = match.group(1)
        f=open("GDebi/Version.py","w")
        f.write("VERSION=\"%s\"\n" % version)
        f.close()


GETTEXT_NAME="gdebi"
I18NFILES = []
for filepath in glob.glob("po/mo/*/LC_MESSAGES/*.mo"):
    lang = filepath[len("po/mo/"):]
    targetpath = os.path.dirname(os.path.join("share/locale",lang))
    I18NFILES.append((targetpath, [filepath]))

# we should probably only run those os.system() stuff when "build" is
# the cmndline argument
os.system("intltool-merge -x po data/gdebi.xml.in"\
                       " build/gdebi.xml")
os.system("intltool-merge -d po data/gdebi.desktop.in"\
                       " build/gdebi.desktop")
os.system("intltool-merge -d po data/gdebi-kde.desktop.in"\
                       " build/gdebi-kde.desktop")

# HACK: make sure that the mo files are generated and up-to-date
os.system("cd po; make update-po")
    
setup(name='gdebi',
      version=version,
      packages=['GDebi'],
      scripts=['gdebi','gdebi-gtk','gdebi-kde'],
      data_files=[('share/gdebi/',
                   ["data/gdebi.glade", "data/GDebiKDEDialog.ui", "data/GDebiKDEInstallDialog.ui"]),
                  ('share/applications',
                   ["build/gdebi.desktop"]),
		  ('share/applications/kde4',
		   ["build/gdebi-kde.desktop"]),
                  ('share/application-registry',
		   ["data/gdebi.applications"]),
                  ('share/mime/packages/',
                   ["build/gdebi.xml"]),
                  ('share/gdebi/',
                   ["data/gdebi.png"])]+I18NFILES,
      )
