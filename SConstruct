import os
import sys
import glob
import shutil
import subprocess
import excons
import excons.tools.zlib as zlib
import excons.tools.threads as threads


lib_version = (2, 2, 0)

lib_suffix = excons.GetArgument("lib-suffix", "-2_2")
static_lib_suffix = excons.GetArgument("static-lib-suffix", "_s")
namespace_version = (excons.GetArgument("namespace-version", 1, int) != 0)


def GenerateConfig(configpath):   
   update = False

   if not os.path.isfile(configpath):
      update = True
   else:
      if not os.path.isfile("config.status"):
         update = True
      else:
         with open("config.status", "r") as f:
            for line in f.readlines():
               spl = line.strip().split(" ")
               if spl[0] == "namespace_version":
                  nv = (int(spl[1]) != 0)
                  if nv != namespace_version:
                     update = True
                     break
               elif spl[0] == "platform":
                  if spl[1] != sys.platform:
                     update = True
                     break
      if update:
         os.remove(configpath)

   if update:
      print("Update 'IlmBaseConfig.h'...")

      with open("config.status", "w") as f:
         f.write("namespace_version %d\n" % namespace_version)
         f.write("platform %s\n" % sys.platform)

      if not os.path.isdir(outhdir):
         os.makedirs(outhdir)

      if sys.platform == "win32":
         shutil.copy("IlmBase/config.windows/IlmBaseConfig.h", configpath)
      else:
         with open(configpath, "w") as f:
            f.write("#define HAVE_PTHREAD 1\n")
            if sys.platform != "darwin":
               f.write("#define ILMBASE_HAVE_LARGE_STACK 1\n")
               f.write("#define HAVE_POSIX_SEMAPHORES 1\n")
               f.write("#define ILMBASE_HAVE_CONTROL_REGISTER_SUPPORT 1\n")
            f.write("\n")
      
      with open(configpath, "a") as f:
         if namespace_version:
            api_version = "%s_%s" % (lib_version[0], lib_version[1])
            f.write("#define ILMBASE_INTERNAL_NAMESPACE_CUSTOM 1\n")
            f.write("#define IMATH_INTERNAL_NAMESPACE Imath_%s\n" % api_version)
            f.write("#define IEX_INTERNAL_NAMESPACE Iex%s\n" % api_version)
            f.write("#define ILMTHREAD_INTERNAL_NAMESPACE IlmThread_%s\n" % api_version)
         else:
            f.write("#define ILMBASE_INTERNAL_NAMESPACE_CUSTOM 0\n")
            f.write("#define IMATH_INTERNAL_NAMESPACE Imath\n")
            f.write("#define IEX_INTERNAL_NAMESPACE Iex\n")
            f.write("#define ILMTHREAD_INTERNAL_NAMESPACE IlmThread\n")
         f.write("\n")

         f.write("#define IMATH_NAMESPACE Imath\n")
         f.write("#define IEX_NAMESPACE Iex\n")
         f.write("#define ILMTHREAD_NAMESPACE IlmThread\n")
         f.write("\n")

         f.write("#define ILMBASE_VERSION_STRING \"%d.%d.%d\"\n" % lib_version)
         f.write("#define ILMBASE_PACKAGE_STRING \"IlmBase %d.%d.%d\"\n" % lib_version)
         f.write("#define ILMBASE_VERSION_MAJOR %d\n" % lib_version[0])
         f.write("#define ILMBASE_VERSION_MINOR %d\n" % lib_version[1])
         f.write("#define ILMBASE_VERSION_PATCH %d\n" % lib_version[2])
         f.write("\n")

         f.write("// Version as a single hex number, e.g. 0x01000300 == 1.0.3\n")
         f.write("#define ILMBASE_VERSION_HEX ((ILMBASE_VERSION_MAJOR << 24) | \\\n")
         f.write("                             (ILMBASE_VERSION_MINOR << 16) | \\\n")
         f.write("                             (ILMBASE_VERSION_PATCH <<  8))\n")
         f.write("\n")

def GenerateHeader(target, source, env):
   p = subprocess.Popen([str(source[0])], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   out, _ = p.communicate()
   with open(str(target[0]), "w") as f:
      f.write(out)
   return None


env = excons.MakeBaseEnv()

env["BUILDERS"]["GenerateHeader"] = Builder(action=GenerateHeader, suffix=".h")

eluth = env.GenerateHeader("IlmBase/Half/eLut.h", File("%s/bin/eLut" % excons.OutputBaseDirectory()))

tofloath = env.GenerateHeader("IlmBase/Half/toFloat.h", File("%s/bin/toFloat" % excons.OutputBaseDirectory()))

outhdir = "%s/include/OpenEXR" % excons.OutputBaseDirectory()

GenerateConfig("%s/IlmBaseConfig.h" % outhdir)

HalfHeaders = env.Install(outhdir, ["IlmBase/Half/half.h",
                                    "IlmBase/Half/halfExport.h",
                                    "IlmBase/Half/halfFunction.h",
                                    "IlmBase/Half/halfLimits.h"])

prjs = [
   {
      "name": "eLut",
      "type": "program",
      "srcs": ["IlmBase/Half/eLut.cpp"]
   },
   {
      "name": "toFloat",
      "type": "program",
      "srcs": ["IlmBase/Half/toFloat.cpp"]
   },
   {
      "name": "Half%s%s" % (lib_suffix, static_lib_suffix),
      "type": "staticlib",
      "alias": "half_static",
      "srcs": ["IlmBase/Half/half.cpp"]
   },
   {
      "name": "Half%s" % (lib_suffix),
      "type": "sharedlib",
      "alias": "half_shared",
      "defs": (["OPENEXR_DLL", "HALF_EXPORTS"] if sys.platform == "win32" else []),
      "srcs": ["IlmBase/Half/half.cpp"]
   },
   # Iex
   # Imath
   # IlmThread
   # IexMath
]

if not lib_suffix:
   # only use shared lib versioning when no lib suffix is provided
   prjs[3]["version"] = "2.2.0"
   prjs[3]["soname"] = "libHalf.so.2"
   prjs[3]["install_name"] = "libHalf.2.dylib"

tgts = excons.DeclareTargets(env, prjs)
