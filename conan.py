import os
import re
import sys
import subprocess

def ParseBuildInfo(path, libs=None, verbose=False):
   if not os.path.isfile(path):
      return {}

   e = re.compile(r"^\[([^]]+)\]$")

   opts = {"includedirs": [],
           "libdirs": [],
           "bindirs": [],
           "libs": [],
           "defines": [],
           "cppflags": [],
           "cflags": [],
           "sharedlinkflags": [],
           "exelinkflags": [],
           "rootpaths": {}}

   with open(path, "r") as f:
      tgtdict = None
      tgtkey = None
      tgtislist = True

      for line in f.readlines():
         m = e.match(line)

         if m is not None:
            opt = m.group(1)
            spl = opt.split("_")

            if len(spl) == 2:
               key, lib = spl
            else:
               key = spl[0]
               lib = None

            if key == "rootpath":
               tgtdict = opts["rootpaths"]
               tgtkey = lib
               tgtislist = False
            else:
               if not key in opts:
                  if verbose:
                     if lib is None:
                        print("Ignore global %s" % key)
                     else:
                        print("Ignore '%s' %s" % (lib, key))
                  continue
               if not libs:
                  if lib:
                     if verbose:
                        print("Ignore '%s' %s" % (lib, key))
                     continue
                  tgtdict = opts
                  tgtkey = key
                  tgtislist = True
               else:
                  if not lib or not lib in libs:
                     if verbose:
                        if lib is None:
                           print("Ignore global %s" % key)
                        else:
                           print("Ignore '%s' %s" % (lib, key))
                     continue
                  tgtdict = opts
                  tgtkey = key
                  tgtislist = True

         else:
            val = line.strip()
            if val:
               if tgtdict is None or tgtkey is None:
                  continue
               if not tgtislist:
                  tgtdict[tgtkey] = val
                  tgtdict = None
                  tgtkey = None
                  tgtislist = True
               else:
                  tgtdict[tgtkey].append(val)
            else:
               tgtdict = None
               tgtkey = None
               tgtislist = True

   return opts

def GetLibConf(directory=".", lib=None, verbose=False):
   cfg = {}
   if lib is not None:
      opts = ParseBuildInfo(os.path.join(directory, "conanbuildinfo.txt"), libs=lib, verbose=verbose)
      for k, v in opts.iteritems():
         if k == "defines":
            cfg["CPPDEFINES"] = v
         elif k == "includedirs":
            cfg["CPPPATH"] = v
         elif k == "cflags":
            cfg["CCFLAGS"] = v
         elif k == "cppflags":
            cfg["CPPFLAGS"] = v
         elif k == "libdirs":
            cfg["LIBPATH"] = v
         elif k == "libs":
            cfg["LIBS"] = v
   return cfg

def Require(directory=".", libs=None, link=None, userproc=None, verbose=False):
   def _RealRequire(env):
      path = os.path.join(directory, "conanbuildinfo.txt")
      opts = ParseBuildInfo(path, libs=libs, verbose=verbose)
      if userproc:
         opts = userproc(opts)

      defs = opts.get("defines", None)
      if defs:
         env.Append(CPPDEFINES=defs)
      incdirs = opts.get("includedirs", None)
      if incdirs:
         env.Append(CPPPATH=incdirs)
      cflags = opts.get("cflags", None)
      if cflags:
         env.Append(CCFLAGS=" %s" % " ".join(cflags))
      cppflags = opts.get("cppflags", None)
      if cppflags:
         env.Append(CPPFLAGS=" %s" % " ".join(cppflags))
      libdirs = opts.get("libdirs", None)
      if libdirs:
         env.Append(LIBPATH=libdirs)
      l = opts.get("libs", None)
      if l:
         env.Append(LIBS=l)
      ldflags = None
      if link == "shared":
         ldflags = opts.get("sharedlinkflags", None)
      elif link == "static":
         ldflags = opts.get("exelinkflags", None)
      if ldflags:
         env.Append(LINKFLAGS=" %s" % " ".join(ldflags))

   return _RealRequire

def Install(directory=".", args="", settings={}):
   path = os.path.join(directory, "conanbuildinfo.txt")
   if not os.path.isfile(path):
      cmd = "conan install \"%s\"" % directory
      if args:
         cmd += " %s" % " ".join(args)
      if settings:
         cmd += " %s" % " ".join(["-s %s=%s" % (k, v) for k, v in settings.iteritems()])
      print(cmd)
      p = subprocess.Popen(cmd, shell=True)
      p.communicate()
      if p.returncode != 0:
         print("'%s' command failed!" % cmd)
         sys.exit(1)
   else:
      print("conan update?")
