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


def GenerateConfig(config_header):   
   update = False

   if not os.path.isfile(config_header):
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
         os.remove(config_header)

   if update:
      print("Update 'IlmBaseConfig.h'...")

      with open("config.status", "w") as f:
         f.write("namespace_version %d\n" % namespace_version)
         f.write("platform %s\n" % sys.platform)

      d = os.path.dirname(config_header)
      if not os.path.isdir(d):
         os.makedirs(d)

      if sys.platform == "win32":
         shutil.copy("IlmBase/config.windows/IlmBaseConfig.h", config_header)
      else:
         with open(config_header, "w") as f:
            f.write("#define HAVE_PTHREAD 1\n")
            if sys.platform != "darwin":
               f.write("#define ILMBASE_HAVE_LARGE_STACK 1\n")
               f.write("#define HAVE_POSIX_SEMAPHORES 1\n")
               f.write("#define ILMBASE_HAVE_CONTROL_REGISTER_SUPPORT 1\n")
            f.write("\n")
      
      with open(config_header, "a") as f:
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

env.GenerateHeader("IlmBase/Half/eLut.h", File("%s/bin/eLut" % excons.OutputBaseDirectory()))

env.GenerateHeader("IlmBase/Half/toFloat.h", File("%s/bin/toFloat" % excons.OutputBaseDirectory()))

out_headers_dir = "%s/include/OpenEXR" % excons.OutputBaseDirectory()

GenerateConfig("%s/IlmBaseConfig.h" % out_headers_dir)

half_headers = env.Install(out_headers_dir, ["IlmBase/Half/half.h",
                                             "IlmBase/Half/halfExport.h",
                                             "IlmBase/Half/halfFunction.h",
                                             "IlmBase/Half/halfLimits.h"])

iex_headers = env.Install(out_headers_dir, glob.glob("IlmBase/Iex/*.h"))

iexmath_headers = env.Install(out_headers_dir, glob.glob("IlmBase/IexMath/*.h"))

imath_headers = env.Install(out_headers_dir, glob.glob("IlmBase/Imath/*.h"))

ilmthread_headers = env.Install(out_headers_dir, glob.glob("IlmBase/IlmThread/*.h"))

ilmthread_srcs = glob.glob("IlmBase/IlmThread/*.cpp")
if sys.platform != "win32":
   ilmthread_srcs = filter(lambda x: "Win32" not in x, ilmthread_srcs)

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
   # Hald
   {
      "name": "Half%s%s" % (lib_suffix, static_lib_suffix),
      "type": "staticlib",
      "alias": "half_static",
      "incdirs": [out_headers_dir],
      "srcs": ["IlmBase/Half/half.cpp"]
   },
   {
      "name": "Half%s" % (lib_suffix),
      "type": "sharedlib",
      "alias": "half_shared",
      "defs": (["OPENEXR_DLL", "HALF_EXPORTS"] if sys.platform == "win32" else []),
      "incdirs": [out_headers_dir],
      "srcs": ["IlmBase/Half/half.cpp"]
   },
   # Iex
   {
      "name": "Iex%s%s" % (lib_suffix, static_lib_suffix),
      "type": "staticlib",
      "alias": "iex_static",
      "incdirs": [out_headers_dir],
      "srcs": glob.glob("IlmBase/Iex/*.cpp")
   },
   {
      "name": "Iex%s" % (lib_suffix),
      "type": "sharedlib",
      "alias": "iex_shared",
      "defs": (["OPENEXR_DLL", "IEX_EXPORTS"] if sys.platform == "win32" else []),
      "incdirs": [out_headers_dir],
      "srcs": glob.glob("IlmBase/Iex/*.cpp")
   },
   # IexMath
   {
      "name": "IexMath%s%s" % (lib_suffix, static_lib_suffix),
      "type": "staticlib",
      "alias": "iexmath_static",
      "incdirs": [out_headers_dir],
      "srcs": glob.glob("IlmBase/IexMath/*.cpp")
   },
   {
      "name": "IexMath%s" % (lib_suffix),
      "type": "sharedlib",
      "alias": "iexmath_shared",
      "defs": (["OPENEXR_DLL", "IEXMATH_EXPORTS"] if sys.platform == "win32" else []),
      "incdirs": [out_headers_dir],
      "libs": ["Iex%s" % lib_suffix],
      "srcs": glob.glob("IlmBase/IexMath/*.cpp")
   },
   # Imath
   {
      "name": "Imath%s%s" % (lib_suffix, static_lib_suffix),
      "type": "staticlib",
      "alias": "imath_static",
      "incdirs": [out_headers_dir],
      "srcs": glob.glob("IlmBase/Imath/*.cpp")
   },
   {
      "name": "Imath%s" % (lib_suffix),
      "type": "sharedlib",
      "alias": "imath_shared",
      "defs": (["OPENEXR_DLL", "IMATH_EXPORTS"] if sys.platform == "win32" else []),
      "incdirs": [out_headers_dir],
      "libs": ["Iex%s" % lib_suffix],
      "srcs": glob.glob("IlmBase/Imath/*.cpp")
   },
   # IlmThread
   {
      "name": "IlmThread%s%s" % (lib_suffix, static_lib_suffix),
      "type": "staticlib",
      "alias": "ilmthread_static",
      "incdirs": [out_headers_dir],
      "srcs": ilmthread_srcs
   },
   {
      "name": "IlmThread%s" % (lib_suffix),
      "type": "sharedlib",
      "alias": "ilmthread_shared",
      "defs": (["OPENEXR_DLL", "ILMTHREAD_EXPORTS"] if sys.platform == "win32" else []),
      "incdirs": [out_headers_dir],
      "libs": ["Iex%s" % lib_suffix],
      "srcs": ilmthread_srcs
   },
   # tests
   {
      "name": "HalfTest",
      "type": "program",
      "libs": ["Half%s%s" % (lib_suffix, static_lib_suffix)],
      "incdirs": [out_headers_dir, "IlmBase/HalfTest"],
      "srcs": glob.glob("IlmBase/HalfTest/*.cpp")
   },
   {
      "name": "IexTest",
      "type": "program",
      "libs": ["Iex%s%s" % (lib_suffix, static_lib_suffix)],
      "incdirs": [out_headers_dir, "IlmBase/IexTest"],
      "srcs": glob.glob("IlmBase/IexTest/*.cpp")
   },
   {
      "name": "ImathTest",
      "type": "program",
      "libs": ["Imath%s%s" % (lib_suffix, static_lib_suffix),
               "Iex%s%s" % (lib_suffix, static_lib_suffix)],
      "incdirs": [out_headers_dir, "IlmBase/ImathTest"],
      "srcs": glob.glob("IlmBase/ImathTest/*.cpp")
   }
]

if not lib_suffix:
   # only use shared lib versioning when no lib suffix is provided
   prjs[3]["version"] = "2.2.0"
   prjs[3]["soname"] = "libHalf.so.2"
   prjs[3]["install_name"] = "libHalf.2.dylib"

   prjs[5]["version"] = "2.2.0"
   prjs[5]["soname"] = "libIex.so.2"
   prjs[5]["install_name"] = "libIex.2.dylib"

   prjs[7]["version"] = "2.2.0"
   prjs[7]["soname"] = "libIexMath.so.2"
   prjs[7]["install_name"] = "libIexMath.2.dylib"

   prjs[9]["version"] = "2.2.0"
   prjs[9]["soname"] = "libImath.so.2"
   prjs[9]["install_name"] = "libImath.2.dylib"

   prjs[11]["version"] = "2.2.0"
   prjs[11]["soname"] = "libIlmThread.so.2"
   prjs[11]["install_name"] = "libIlmThread.2.dylib"

tgts = excons.DeclareTargets(env, prjs)

env.Alias("libs", ["half_static", "half_shared",
                   "iex_static", "iex_shared",
                   "iexmath_static", "iexmath_shared",
                   "imath_static", "imath_shared",
                   "ilmthread_static", "ilmthread_shared"] +
                   half_headers +
                   iex_headers +
                   iexmath_headers +
                   imath_headers +
                   ilmthread_headers)

env.Alias("staticlibs", ["half_static",
                         "iex_static",
                         "iexmath_static",
                         "imath_static",
                         "ilmthread_static"] +
                         half_headers +
                         iex_headers +
                         iexmath_headers +
                         imath_headers +
                         ilmthread_headers)

env.Alias("sharedlibs", ["half_shared",
                         "iex_shared",
                         "iexmath_shared",
                         "imath_shared",
                         "ilmthread_shared"] +
                         half_headers +
                         iex_headers +
                         iexmath_headers +
                         imath_headers +
                         ilmthread_headers)

env.Alias("tests", ["HalfTest",
                    "IexTest",
                    "ImathTest"])

