import sys, time, thread, os, fcntl, string
import apt, apt_pkg
from gettext import gettext as _

from DebPackage import DebPackage, MyCache
from DscSrcPackage import DscSrcPackage

class GDebiCli(object):

    def __init__(self):
        # fixme, do graphic cache check
        tp = apt.progress.OpTextProgress()
        self._cache = MyCache(tp)
        
    def open(self, file):
        try:
            if file.endswith(".deb"):
                self._deb = DebPackage(self._cache, file)
            elif file.endswith(".dsc"):
                self._deb = DscSrcPackage(self._cache, file)
            else:
                raise Exception
        except (IOError,SystemError),e:
            print _("Failed to open the software package"),
            print _("The package might be corrupted or you are not "
                    "allowed to open the file. Check the permissions "
                    "of the file.")
            sys.exit(1)
        print self._deb.pkgName
        try:
            print self._deb["Description"]
        except KeyError:
            print _("No description is available")

        # check the deps
        if not self._deb.checkDeb():
            print _("This package is uninstallable")
            print self._deb._failureString
            return False

        # show what changes
        (install, remove, unauthenticated) = self._deb.requiredChanges
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
        return True

    def install(self):
        # install the dependecnies
        (install,remove,unauthenticated) = self._deb.requiredChanges
        if len(install) > 0 or len(remove) > 0:
            fprogress = apt.progress.TextFetchProgress()
            iprogress = apt.progress.InstallProgress()
            res = self._cache.commit(fprogress,iprogress)

        # install the package itself
        os.system("dpkg -i %s"%self._deb.file)
        

if __name__ == "__main__":
    app = GDebiCli()
    if not app.open(sys.argv[1]):
        sys.exit(1)
    print _("Do you want to install the software package? [y/N]:"),
    sys.stdout.flush()
    res = sys.stdin.readline()
    if res.startswith("y") or res.startswith("Y"):
        app.install()
