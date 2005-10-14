import apt_inst, apt_pkg
import apt
import sys, os, subprocess

class DebPackage:
    def __init__(self, cache, file):
        self._cache = cache
        self._debfile = file
        self._needPkgs = []
        # read the deb
        control = apt_inst.debExtractControl(open(file))
        self._sections = apt_pkg.ParseSection(control)

    def checkDepends(self):
        depends = []
        
        arch = self._sections["Architecture"]
        if  arch != "all" and arch != apt_pkg.CPU:
            print "ERROR: Wrong architecture dude!"
            self._failureString = "Wrong architecture '%s'" % arch
            return False

        # FIXME: this sort of error handling sux
        self._failureString = ""

        # check depends
        # FIXME: check conflicts (replace?) as well,
        #        probably just whine and fail for now
        for key in ["Depends","PreDepends"]:
            if self._sections.has_key(key):
                depends.extend(apt_pkg.ParseDepends(self._sections[key]))

        # check them
        for or_group in depends:
            or_found = False
            for dep in or_group:
                depname = dep[0]
                ver = dep[1]
                oper = dep[2]

                print "looking at: %s" % depname
                if not self._cache.has_key(depname):
                    # check apt_pkg cache
                    print "Depenedency %s is either virtual or not found" % (depname)
                    virtual_pkg = self._cache._cache[depname]
                    for pkg in self._cache:
                        v = self._cache._depcache.GetCandidateVer(pkg._pkg)
                        if v == None:
                            continue
                        for p in v.ProvidesList:
                            if depname == p[0]:
                                # we found a pkg that provides this virtual
                                # pkg, check if the proivdes is any good
                                print "%s provides %s" % (pkg.name, depname)
                                cand = self._cache[pkg.name]
                                candver = self._cache._depcache.GetCandidateVer(cand._pkg)
                                instver = cand._pkg.CurrentVer
                                res = apt_pkg.CheckDep(candver.VerStr,oper,ver)
                                if res == True:
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
                    print "Need to get: %s" % depname
                    self._needPkgs.append(depname)
                else:
                    print "Is already installed: %s" % depname

                # ok, if we are here, we have a good version
                or_found = True
                break

            # check if this or group was ok
            if or_found == False:
                self._failureString += "Dependency found: %s" % depname
                return False
        return True
                    

    def installDeps(self):
        print "Installing: %s" % self._needPkgs
        if len(self._needPkgs) == 0:
            return
        cmd = ["/usr/sbin/synaptic", "--hide-main-window",
               "--non-interactive", "--set-selections",
               "-o","Volatile::NoStateSaving=True",
               "-o", "Synaptic::closeZvt=True"
               ]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        f = proc.stdin
        for s in self._needPkgs:
            f.write("%s\tinstall\n" % s)
        f.close()
        proc.wait()
        return

 
    # properties
    def __getitem__(self,item):
        return self._sections[item]



if __name__ == "__main__":

    cache = apt.Cache()

    d = DebPackage(cache, sys.argv[1])
    print d["Package"]
    if not d.checkDepends():
        print "Dependencies can't be satifisied"
        sys.exit(1)
    d.installDeps()
    d.installDeb()
