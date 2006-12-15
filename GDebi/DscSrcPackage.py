
import apt_inst, apt_pkg
import apt
import sys
import os 
from gettext import gettext as _
from DebPackage import DebPackage
from Cache import Cache

class DscSrcPackage(DebPackage):
    def __init__(self, cache, file=None):
        DebPackage.__init__(self, cache)
        self.depends = []
        self.conflicts = []
        if file != None:
            self.open(file)
    def getConflicts(self):
        return self.conflicts
    def getDepends(self):
        return self.depends
    def open(self, file):
        depends_tags = ["Build-Depends", "Build-Depends-Indep"]
        conflicts_tags = ["Build-Conflicts", "Build-Conflicts-Indep"]
        for line in open(file):
            for tag in depends_tags:
                if line.startswith(tag):
                    key = line.split(":")[1].strip()
                    self.depends.extend(apt_pkg.ParseDepends(key))
            for tag in conflicts_tags:
                if line.startswith(tag):
                    key = line.split(":")[1].strip()
                    self.conflicts.extend(apt_pkg.ParseDepends(key))
            if line.startswith("Source"):
                self.pkgName = line.split(":")[1].strip()
    def checkDeb(self):
        if not self.checkConflicts():
            for pkgname in self._installedConflicts:
                if self._cache[pkgname]._pkg.Essential:
                    raise Exception, _("A essential package would be removed")
                self._cache[pkgname].markDelete()
        # FIXME: a additional run of the checkConflicts()
        #        after _satisfyDepends() should probably be done
        return self._satisfyDepends(self.depends)

if __name__ == "__main__":

    cache = Cache()
    s = DscSrcPackage(cache, "../tests/3ddesktop_0.2.9-6.dsc")
    s.checkDep()
    print "Missing deps: ",s.missingDeps
    print "Print required changes: ", s.requiredChanges
