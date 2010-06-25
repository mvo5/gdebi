# Copyright (c) 2005-2009 Canonical Ltd
#
# AUTHOR:
# Michael Vogt <mvo@ubuntu.com>
#
# This file is part of GDebi
#
# GDebi is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# GDebi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GDebi; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#


import apt
import apt_pkg
import fcntl
import os
import string
import sys
import time
import thread

from gettext import gettext as _

from apt.cache import Cache
from apt.debfile import DebPackage, DebSrcPackage

from subprocess import PIPE, Popen, call

class GDebiCli(object):

    def __init__(self, options):
        # fixme, do graphic cache check
        self.options = options
        if options.quiet:
            tp = apt.progress.base.OpProgress()
        else:
            tp = apt.progress.text.OpProgress()
        # set architecture to architecture in root-dir
        if options.rootdir and os.path.exists(options.rootdir+"/usr/bin/dpkg"):
            arch = Popen([options.rootdir+"/usr/bin/dpkg",
                          "--print-architecture"], stdout=PIPE).communicate()[0]
            if arch:
                apt_pkg.config.set("APT::Architecture",arch.strip())
        if options.apt_opts:
            for o in options.apt_opts:
                if o.find('=') < 0:
                    sys.stderr.write(_("Configuration items must be specified with a =<value>\n"))
                    sys.exit(1)
                (name, value) = o.split('=', 1)
                try:
                    apt_pkg.config.set(name, value)
                except:
                    sys.stderr.write(_("Couldn't set APT option %s to %s\n") % (name, value))
                    sys.exit(1)
        self._cache = Cache(tp, rootdir=options.rootdir)

    def open(self, file):
        try:
            if (file.endswith(".deb") or 
                "Debian binary package" in Popen(["file", file], stdout=PIPE).communicate()[0]):
                self._deb = DebPackage(file, self._cache)
            elif (file.endswith(".dsc") or
                  os.path.basename(file) == "control"):
                self._deb = DscSrcPackage(file, self._cache)
            else:
                sys.stderr.write(_("Unknown package type '%s', exiting\n") % file)
                sys.exit(1)
        except (IOError,SystemError),e:
            sys.stderr.write(_("Failed to open the software package\n"))
            sys.stderr.write(_("The package might be corrupted or you are not "
                           "allowed to open the file. Check the permissions "
                           "of the file.\n"))
            sys.exit(1)
        # check the deps
        if not self._deb.check():
            sys.stderr.write(_("This package is uninstallable\n"))
            sys.stderr.write(self._deb._failure_string + "\n")
            return False
        return True
            
    def show_description(self):
        try:
            print self._deb["Description"]
        except KeyError:
            print _("No description is available")

    def show_dependencies(self):
        # show what changes
        (install, remove, unauthenticated) = self._deb.required_changes
        if len(unauthenticated) > 0:
            print _("The following packages are UNAUTHENTICATED: ")
            for pkgname in unauthenticated:
                print pkgname + " ",
        if len(remove) > 0:
            print _("Requires the REMOVAL of the following packages: ")
            for pkgname in remove:
                print pkgname + " ",
        print
        if len(install) > 0:
            print _("Requires the installation of the following packages: ") 
            for pkgname in install:
                print pkgname + " ",
        print

    def install(self):
        # install the dependecnies
        (install,remove,unauthenticated) = self._deb.required_changes
        if len(install) > 0 or len(remove) > 0:
            fprogress = apt.progress.text.AcquireProgress()
            iprogress = apt.progress.base.InstallProgress()
            try:
                res = self._cache.commit(fprogress,iprogress)
            except SystemError, e:
                sys.stderr.write(_("Error during install: '%s'") % e)
                return False

        # install the package itself
        if self._deb.file.endswith(".dsc"): 
            # FIXME: add option to only install build-dependencies
            #        (or build+install the deb) and then enable
            #        this code
            #dir = self._deb.pkgname + "-" + apt_pkg.UpstreamVersion(self._deb["Version"])
            #os.system("dpkg-source -x %s" % self._deb.file)
            #os.system("cd %s && dpkg-buildpackage -b -uc" % dir)
            #for i in self._deb.binaries:
            #    os.system("gdebi %s_%s_*.deb" % (i,self._deb["Version"]))
            pass
        else:
            ret = call(["dpkg","--auto-deconfigure", "-i",self._deb.file])
            if (ret != 0):
                return False
        return True
        

if __name__ == "__main__":
    app = GDebiCli()
    if not app.open(sys.argv[1]):
        sys.exit(1)
    msg =  _("Do you want to install the software package? [y/N]:")
    print msg,
    sys.stdout.flush()
    res = sys.stdin.readline()
    if res.lower().startswith(msg[-5]):
        app.install()
