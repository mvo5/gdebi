import apt

class Cache(apt.Cache):
    """ helper to provide some additonal functions """

    def clear(self):
        """ unmark all pkgs """
        self._depcache.Init()

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

    def downloadable(self, pkg, useCandidate=True):
        " check if the given pkg can be downloaded "
        if useCandidate:
            ver = self._depcache.GetCandidateVer(pkg._pkg)
        else:
            ver = pkg._pkg.CurrentVer
        if ver == None:
            return False
        return ver.Downloadable

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

