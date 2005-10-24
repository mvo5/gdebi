#!/usr/bin/python2.4

import sys, time, thread, os, fcntl, string
import apt, apt_pkg
import subprocess

from DebPackage import DebPackage, MyCache


class GDebiCli(object):

    def __init__(self):
        # fixme, do graphic cache check
        tp = apt.progress.OpTextProgress()
        self._cache = MyCache(tp)
        
    def open(self, file):
        self._deb = DebPackage(self._cache, file)
        print self._deb.pkgName
        try:
            print self._deb["Description"]
        except KeyError:
            print "No description found in the package"

        # check the deps
        if not self._deb.checkDeb():
            print "This package can't be installed"
            print self._deb._failureString
            return False

        # show what changes
        (install, remove) = self._deb.requiredChanges
        if len(remove) > 0:
            print "Need to REMOVE the following pkgs: " 
            for pkgname in install:
                print pkgname + " ",
        print
        if len(install) > 0:
            print "Need to install the following pkgs: " 
            for pkgname in install:
                print pkgname + " ",
        print
        return True

    def install(self):
        # install the dependecnies
        (install,remove) = self._deb.requiredChanges
        if len(install) > 0 or len(remove) > 0:
            # lock for install
            apt_pkg.PkgSystemLock()
            fprogress = apt.progress.TextFetchProgress()
            iprogress = apt.progress.InstallProgress()
            res = self._cache.commit(fprogress,iprogress)

        # install the package itself
        subprocess.call(["dpkg", "-i", "%s"%self._deb.file])
        

if __name__ == "__main__":
    app = GDebiCli()
    if not app.open(sys.argv[1]):
        sys.exit(1)
    print "Do you want to install it [yN]:",
    sys.stdout.flush()
    res = sys.stdin.readline()
    if res.startswith("y") or res.startswith("Y"):
        app.install()
