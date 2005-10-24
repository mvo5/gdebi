import apt_inst, apt_pkg
import apt
import sys, os, subprocess

class DebPackage:
    debug = 0
    
    def __init__(self, cache, file):
        cache.clear()
        self._cache = cache
        self.file = file
        self._needPkgs = None
        # read the deb
        control = apt_inst.debExtractControl(open(file))
        self._sections = apt_pkg.ParseSection(control)
        self.pkgName = self._sections["Package"]


    def _isOrGroupSatisfied(self, or_group):
        """ this function gets a "or_group" and analyzes if
            at least one dependency of this group is already satisfied """
        self._dbg(2,"_checkOrGroup(): %s " % (or_group))

        for dep in or_group:
            depname = dep[0]
            ver = dep[1]
            oper = dep[2]

            # check for virtual pkgs
            if not self._cache.has_key(depname):
                if self._cache.isVirtualPkg(depname):
                    #print "%s is virtual" % depname
                    for pkg in self._cache.getProvidersForVirtual(depname):
                        if pkg.isInstalled:
                            return True
                continue

            inst = self._cache[depname]
            instver = inst.installedVersion
            if instver != None and apt_pkg.CheckDep(instver,oper,ver) == True:
                return True

        return False
            

    def _satisfyOrGroup(self, or_group):
        """ try to satisfy the or_group """

        or_found = False
        virtual_pkg = None

        for dep in or_group:
            depname = dep[0]
            ver = dep[1]
            oper = dep[2]

            if not self._cache.has_key(depname):
                if self._cache.isVirtualPkg(depname):
                    virtual_pkg = depname
                continue
                
            # now check if we can satisfy the deps with the candidate(s)
            # in the cache
            cand = self._cache[depname]
            candver = self._cache._depcache.GetCandidateVer(cand._pkg)
            if not apt_pkg.CheckDep(candver.VerStr,oper,ver):
                continue

            # check if we need to install it
            self._dbg(2,"Need to get: %s" % depname)
            self._needPkgs.append(depname)
            return True

        # check if this or group was ok
        or_str = ""
        for dep in or_group:
            or_str += dep[0]
            if dep != or_group[len(or_group)-1]:
                or_str += "|"
        self._failureString += "Dependency not found: %s" % or_str
        return False
        

    def checkDeb(self):
        self._dbg(3,"checkDepends")
        # init 
        self._needPkgs = []
        depends = []

        # check arch
        arch = self._sections["Architecture"]
        if  arch != "all" and arch != apt_pkg.CPU:
            self._dbg(1,"ERROR: Wrong architecture dude!")
            self._failureString = "Wrong architecture '%s'" % arch
            return False

        # check version
        # FIXME: same version is not strictly a error
        pkgname = self._sections["Package"]
        debver = self._sections["Version"]
        self._dbg(1,"debver: %s" % debver)
        if self._cache.has_key(pkgname):
            instver = self._cache[pkgname].installedVersion
            if instver != None:
                cmp = apt_pkg.VersionCompare(debver,instver)
                if cmp == 0:
                    self._failureString = "Same version is already installed"
                    return False
                elif cmp == -1:
                    self._failureString = "Newer version is already installed"
                    return False
            
        # check conflicts
        key = "Conflicts"
        if self._sections.has_key(key):
            conflicts = apt_pkg.ParseDepends(self._sections[key])
            for or_group in conflicts:
                if self._satisfyOrGroup(or_group):
                    #print "Conflicts with a exisiting pkg!"
                    self._failureString = "Conflicts with a exisiting pkg!"
                    return False
        
        # FIXME: this sort of error handling sux
        self._failureString = ""

        # FIXME: check conflicts (replace?) as well,
        #        probably just whine and fail for now

        # find depends
        for key in ["Depends","PreDepends"]:
            if self._sections.has_key(key):
                depends.extend(apt_pkg.ParseDepends(self._sections[key]))

        # check depends
        for or_group in depends:
            #print "or_group: %s" % or_group
            #print "or_group satified: %s" % self._isOrGroupSatisfied(or_group)
            if not self._isOrGroupSatisfied(or_group):
                if not self._satisfyOrGroup(or_group):
                    return False

        # now try it out in the cache
        for pkg in self._needPkgs:
            self._cache[pkg].markInstall()

        if self._cache._depcache.BrokenCount > 0:
            self._failureString = "Installing the dependencies impossible (broken cache)"
            # clean the cache again
            self._cache.clear()
            return False

        return True

    def missingDeps(self):
        self._dbg(1, "Installing: %s" % self._needPkgs)
        if self._needPkgs == None:
            self.checkDeb()
        return self._needPkgs
    missingDeps = property(missingDeps)

    def requiredChanges(self):
        install = []
        remove = []
        for pkg in self._cache:
            if pkg.markedInstall or pkg.markedUpgrade:
                install.append(pkg.name)
            if pkg.markedDelete:
                remove.append(pkg.name)
        return (install,remove)
    requiredChanges = property(requiredChanges)
    
    # properties
    def __getitem__(self,item):
        return self._sections[item]

    def _dbg(self, level, msg):
        """Write debugging output to sys.stderr.
        """
        if level <= self.debug:
            print >> sys.stderr, msg


class MyCache(apt.Cache):
    """ helper to provide some additonal functions """

    def clear(self):
        """ unmark all pkgs """
        for pkg in self:
            pkg.markKeep()

    def isVirtualPkg(self, pkgname):
        """ this function returns true if pkgname is a virtual
            pkg """
        try:
            virtual_pkg = self._cache[pkgname]
        except KeyError:
            return False

        if len(virtual_pkg.VersionList) == 0:
            return True
        return False

    def getProvidersForVirtual(self, virtual_pkg):
        providers = []
        try:
            vp = self._cache[virtual_pkg]
            if len(vp.VersionList) != 0:
                return providers
        except IndexError:
            return providers
        for pkg in self:
            v = self._depcache.GetCandidateVer(pkg._pkg)
            if v == None:
                continue
            for p in v.ProvidesList:
                #print virtual_pkg
                #print p[0]
                if virtual_pkg == p[0]:
                    # we found a pkg that provides this virtual
                    # pkg, check if the proivdes is any good
                    providers.append(pkg)
                    #cand = self._cache[pkg.name]
                    #candver = self._cache._depcache.GetCandidateVer(cand._pkg)
                    #instver = cand._pkg.CurrentVer
                    #res = apt_pkg.CheckDep(candver.VerStr,oper,ver)
                    #if res == True:
                    #    self._dbg(1,"we can use %s" % pkg.name)
                    #    or_found = True
                    #    break
        return providers

if __name__ == "__main__":

    cache = MyCache()

    vp = "www-browser"
    print "%s virtual: %s" % (vp,cache.isVirtualPkg(vp))
    providers = cache.getProvidersForVirtual(vp)
    print "Providers for %s :" % vp
    for pkg in providers:
        print " %s" % pkg.name
    
    d = DebPackage(cache, sys.argv[1])
    print d.pkgName
    if not d.checkDeb():
        print "can't be satified"
        print d._failureString
    print d.missingDeps

    #d = DebPackage(cache, sys.argv[1])
    #print d.pkgName
    #print d.missingDeps
