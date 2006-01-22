import sys, time, thread, os, fcntl, string
import apt, apt_pkg

from DebPackage import DebPackage, MyCache


class GDebiCli(object):

    def __init__(self):
        # fixme, do graphic cache check
        tp = apt.progress.OpTextProgress()
        self._cache = MyCache(tp)
        
    def open(self, file):
        try:
            self._deb = DebPackage(self._cache, file)
        except (IOError,SystemError),e:
            print _("Failed to open the deb package"),
            print _("The package can't be opened, it may have "
                    "improper permissions, is invalid or corrupted.")
            sys.exit(1)
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
        (install, remove, unauthenticated) = self._deb.requiredChanges
        if len(unauthenticated) > 0:
            print "The following packages are UNAUTHENTICATED: "
            for pkgname in unauthenticated:
                print pkgname + " ",
        if len(remove) > 0:
            print "Need to REMOVE the following pkgs: " 
            for pkgname in remove:
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
    print "Do you want to install it [yN]:",
    sys.stdout.flush()
    res = sys.stdin.readline()
    if res.startswith("y") or res.startswith("Y"):
        app.install()
