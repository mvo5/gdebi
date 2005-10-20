import apt_inst, apt_pkg
import apt
import sys, os, subprocess

class DebPackage:
    debug = 0
    
    def __init__(self, cache, file):
        self._cache = cache
        self.file = file
        self._needPkgs = None
        # read the deb
        control = apt_inst.debExtractControl(open(file))
        self._sections = apt_pkg.ParseSection(control)
        self.pkgName = self._sections["Package"]

    def checkDepends(self):
        self._dbg(3,"checkDepends")
        # init 
        self._needPkgs = []
        depends = []
        
        arch = self._sections["Architecture"]
        if  arch != "all" and arch != apt_pkg.CPU:
            self._dbg(1,"ERROR: Wrong architecture dude!")
            self._failureString = "Wrong architecture '%s'" % arch
            return False

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
            

        # FIXME: this sort of error handling sux
        self._failureString = ""

        # FIXME: check conflicts (replace?) as well,
        #        probably just whine and fail for now


        # check depends
        for key in ["Depends","PreDepends"]:
            if self._sections.has_key(key):
                depends.extend(apt_pkg.ParseDepends(self._sections[key]))

        # check them
        for or_group in depends:
            # FIXME: with this trick we get get most pkgs right,
            # but we really need to be smarter in the or-groups
            # and figure if we already have a single dep installed
            or_group.reverse()

            self._dbg(2,"in or-gr %s " % (or_group))
            or_found = False
            for dep in or_group:
                if or_found:
                    break
                #if dep:
                #    self._dbg(1,"dep found: %s " % (dep))
                depname = dep[0]
                ver = dep[1]
                oper = dep[2]

                self._dbg(2, "looking at: %s" % depname)
                if not self._cache.has_key(depname):
                    # check apt_pkg cache
                    self._dbg(1, "Depenedency %s is either virtual or not found" % (depname))
                    virtual_pkg = self._cache._cache[depname]
                    for pkg in self._cache:
                        v = self._cache._depcache.GetCandidateVer(pkg._pkg)
                        if v == None:
                            continue
                        for p in v.ProvidesList:
                            if depname == p[0]:
                                # we found a pkg that provides this virtual
                                # pkg, check if the proivdes is any good
                                self._dbg(1,"%s provides %s" % (pkg.name, depname))
                                cand = self._cache[pkg.name]
                                candver = self._cache._depcache.GetCandidateVer(cand._pkg)
                                instver = cand._pkg.CurrentVer
                                res = apt_pkg.CheckDep(candver.VerStr,oper,ver)
                                if res == True:
                                    self._dbg(1,"we can use %s" % pkg.name)
                                    or_found = True
                                    break
                    continue

                # now check if we can satisfy the deps with the candidate(s)
                # in the cache
                cand = self._cache[depname]
                candver = self._cache._depcache.GetCandidateVer(cand._pkg)
                res = apt_pkg.CheckDep(candver.VerStr,oper,ver)
                if res != True:
                    continue

                # check if we need to install it
                if cand._pkg.CurrentVer == None:
                    self._dbg(2,"Need to get: %s" % depname)
                    self._needPkgs.append(depname)
                else:
                    self._dbg(2,"Is already installed: %s" % depname)

                # ok, if we are here, we have a good version
                or_found = True
                break

            # check if this or group was ok
            if or_found == False:
                self._failureString += "Dependency found: %s" % depname
                return False
        return True
                    

    def missingDeps(self):
        self._dbg(1, "Installing: %s" % self._needPkgs)
        if self._needPkgs == None:
            self.checkDepends()
        return self._needPkgs
    missingDeps = property(missingDeps)
 
    # properties
    def __getitem__(self,item):
        return self._sections[item]

    def _dbg(self, level, msg):
        """Write debugging output to sys.stderr.
        """
        if level <= self.debug:
            print >> sys.stderr, msg



if __name__ == "__main__":

    cache = apt.Cache()

    d = DebPackage(cache, sys.argv[1])
    print d.pkgName
    print d.missingDeps

    d = DebPackage(cache, sys.argv[1])
    print d.pkgName
    print d.missingDeps
