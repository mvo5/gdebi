#!/usr/bin/python2.4

import sys, time, thread, os, fcntl, string
import apt, apt_pkg
import subprocess

from DebPackage import DebPackage


class GDebiCli(object):

    def __init__(self):
        # fixme, do graphic cache check
        tp = apt.progress.OpTextProgress()
        self._cache = apt.Cache(tp)
        
    def open(self, file):
        self._deb = DebPackage(self._cache, file)
        print self._deb.pkgName
        try:
            print self._deb["Description"]
        except KeyError:
            print "No description found in the package"

        # check the deps
        if not self._deb.checkDepends():
            print self._deb._failureString
        else:
            print "Need to install the following %s packages from the archive:" % len(self._deb.missingDeps)
            for pkgname in self._deb.missingDeps:
                print pkgname
        return True

    def install(self):
        # install the dependecnies
        pkgs = self._deb.missingDeps
        print pkgs
        if len(pkgs) > 0:
            # lock for install
            apt_pkg.PkgSystemLock()
            for pkg in pkgs:
                self._cache[pkg].markInstall()
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
