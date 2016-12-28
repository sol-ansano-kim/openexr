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
static_lib_suffix = lib_suffix + excons.GetArgument("static-lib-suffix", "_s")
namespace_version = (excons.GetArgument("namespace-version", 1, int) != 0)
zlib_win_api = (excons.GetArgument("zlib-win-api", 0, int) != 0)
have_gcc_include_asm_avx = False
have_sysconf_nprocessors_onln = False

gcc_include_asm_avx_check_src = """
int main()
{
#if defined(__GNUC__) && defined(__SSE2__) 
   int n   = 0;
   int eax = 0;
   int edx = 0;
   __asm__(
      \"xgetbv     ;\"
      \"vzeroupper  \"
      : \"=a\"(eax), \"=d\"(edx) : \"c\"(n) : );
#else
   #error No GCC style inline asm supported for AVX instructions
#endif
}
"""

_sc_nprocessors_onln_check_src = """
#include <unistd.h>
int main()
{
   sysconf(_SC_NPROCESSORS_ONLN);
}
"""

def CheckConfigStatus(path):
   if not os.path.isfile(path):
      return True
   else:
      with open(path, "r") as f:
         for line in f.readlines():
            spl = line.strip().split(" ")
            if spl[0] == "namespace_version":
               val = (int(spl[1]) != 0)
               if val != namespace_version:
                  return True
            elif spl[0] == "platform":
               if spl[1] != sys.platform:
                  return True
            elif spl[0] == "have_gcc_include_asm_avx":
               val = (int(spl[1]) != 0)
               if val != have_gcc_include_asm_avx:
                  return True
            elif spl[0] == "have_sysconf_nprocessors_onln":
               val = (int(spl[1]) != 0)
               if val != have_sysconf_nprocessors_onln:
                  return True
      return False

def WriteConfigStatus(path):
   with open(path, "w") as f:
      f.write("namespace_version %d\n" % namespace_version)
      f.write("platform %s\n" % sys.platform)
      f.write("have_gcc_include_asm_avx %d\n" % have_gcc_include_asm_avx)
      f.write("have_sysconf_nprocessors_onln %d\n" % have_sysconf_nprocessors_onln)

def GenerateIlmBaseConfig(config_header):   
   update = False

   if not os.path.isfile(config_header):
      update = True
   else:
      update = CheckConfigStatus("ilmbase_config.status")
      if update:
         os.remove(config_header)

   if update:
      print("Update '%s'..." % os.path.basename(config_header))

      WriteConfigStatus("ilmbase_config.status")

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

def GenerateOpenEXRConfig(config_header):
   update = False

   if not os.path.isfile(config_header):
      update = True
   else:
      update = CheckConfigStatus("openexr_config.status")
      if update:
         os.remove(config_header)

   if update:
      print("Update '%s'..." % os.path.basename(config_header))

      WriteConfigStatus("openexr_config.status")

      d = os.path.dirname(config_header)
      if not os.path.isdir(d):
         os.makedirs(d)

      with open(config_header, "w") as f:
         if sys.platform == "win32":
            f.write("#define OPENEXR_IMF_HAVE_COMPLETE_IOMANIP 1\n")
         elif sys.platform == "darwin":
            f.write("#define OPENEXR_IMF_HAVE_DARWIN 1\n")
            f.write("#define OPENEXR_IMF_HAVE_COMPLETE_IOMANIP 1\n")
            f.write("#include <string.h>\n")
         else:
            f.write("#define OPENEXR_IMF_HAVE_LINUX_PROCFS 1\n")
            f.write("#define OPENEXR_IMF_HAVE_COMPLETE_IOMANIP 1\n")
            f.write("#define OPENEXR_IMF_HAVE_LARGE_STACK 1\n")
         f.write("\n")

         if namespace_version:
            api_version = "%s_%s" % (lib_version[0], lib_version[1])
            f.write("#define OPENEXR_IMF_INTERNAL_NAMESPACE_CUSTOM 1\n")
            f.write("#define OPENEXR_IMF_NAMESPACE Imf\n")
            f.write("#define OPENEXR_IMF_INTERNAL_NAMESPACE Imf_%s\n" % api_version)
         else:
            f.write("#define OPENEXR_IMF_INTERNAL_NAMESPACE_CUSTOM 0\n")
            f.write("#define OPENEXR_IMF_NAMESPACE Imf\n")
            f.write("#define OPENEXR_IMF_INTERNAL_NAMESPACE Imf\n")
         f.write("\n")

         f.write("#define OPENEXR_VERSION_STRING \"%d.%d.%d\"\n" % lib_version)
         f.write("#define OPENEXR_PACKAGE_STRING \"OpenEXR %d.%d.%d\"\n" % lib_version)
         f.write("#define OPENEXR_VERSION_MAJOR %d\n" % lib_version[0])
         f.write("#define OPENEXR_VERSION_MINOR %d\n" % lib_version[1])
         f.write("#define OPENEXR_VERSION_PATCH %d\n" % lib_version[2])
         f.write("#define OPENEXR_VERSION_HEX ((OPENEXR_VERSION_MAJOR << 24) | \\\n")
         f.write("                             (OPENEXR_VERSION_MINOR << 16) | \\\n")
         f.write("                             (OPENEXR_VERSION_PATCH <<  8))\n")
         f.write("\n")

         if have_gcc_include_asm_avx:
            f.write("#define OPENEXR_IMF_HAVE_GCC_INLINE_ASM_AVX 1\n")

         if have_sysconf_nprocessors_onln:
            f.write("#define OPENEXR_IMF_HAVE_SYSCONF_NPROCESSORS_ONLN 1\n")

def GenerateHeader(target, source, env):
   p = subprocess.Popen([str(source[0])], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   out, _ = p.communicate()
   with open(str(target[0]), "w") as f:
      f.write(out)
   return None


env = excons.MakeBaseEnv()

if sys.platform != "win32":
   env.Append(CPPFLAGS=" -Wno-unused-variable -Wno-unused-parameter")
   if sys.platform == "darwin":
      env.Append(CPPFLAGS=" -Wno-unused-private-field")
   else:
      env.Append(CPPFLAGS=" -Wno-unused-but-set-variable")

env["BUILDERS"]["GenerateHeader"] = Builder(action=GenerateHeader, suffix=".h")

conf = Configure(env)
if conf.TryCompile(gcc_include_asm_avx_check_src, ".cpp"):
   have_gcc_include_asm_avx = True
if conf.TryCompile(_sc_nprocessors_onln_check_src, ".cpp"):
   have_sysconf_nprocessors_onln = True
conf.Finish()

env.GenerateHeader("IlmBase/Half/eLut.h", File("%s/bin/eLut" % excons.OutputBaseDirectory()))

env.GenerateHeader("IlmBase/Half/toFloat.h", File("%s/bin/toFloat" % excons.OutputBaseDirectory()))

env.GenerateHeader("OpenEXR/IlmImf/b44ExpLogTable.h", File("%s/bin/b44ExpLogTable" % excons.OutputBaseDirectory()))

env.GenerateHeader("OpenEXR/IlmImf/dwaLookups.h", File("%s/bin/dwaLookups" % excons.OutputBaseDirectory()))

out_headers_dir = "%s/include/OpenEXR" % excons.OutputBaseDirectory()

GenerateIlmBaseConfig("%s/IlmBaseConfig.h" % out_headers_dir)

GenerateOpenEXRConfig("%s/OpenEXRConfig.h" % out_headers_dir)

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

openexr_defs = []
if zlib_win_api:
   openexr_defs.append("ZLIB_WIN_API")

def ilmimf_filter(x):
   name = os.path.splitext(os.path.basename(x))[0]
   return (name not in ["b44ExpLogTable", "dwaLookups"])

ilmimf_headers = env.Install(out_headers_dir, filter(ilmimf_filter, glob.glob("OpenEXR/IlmImf/*.h")))

ilmimf_srcs = filter(ilmimf_filter, glob.glob("OpenEXR/IlmImf/*.cpp"))

ilmimfutil_headers = env.Install(out_headers_dir, glob.glob("OpenEXR/IlmImfUtil/*.h"))

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
   # Half
   {
      "name": "Half" + static_lib_suffix,
      "type": "staticlib",
      "alias": "half_static",
      "incdirs": [out_headers_dir],
      "srcs": ["IlmBase/Half/half.cpp"]
   },
   {
      "name": "Half" + lib_suffix,
      "type": "sharedlib",
      "alias": "half_shared",
      "defs": (["OPENEXR_DLL", "HALF_EXPORTS"] if sys.platform == "win32" else []),
      "incdirs": [out_headers_dir],
      "srcs": ["IlmBase/Half/half.cpp"]
   },
   # Iex
   {
      "name": "Iex" + static_lib_suffix,
      "type": "staticlib",
      "alias": "iex_static",
      "incdirs": [out_headers_dir],
      "srcs": glob.glob("IlmBase/Iex/*.cpp")
   },
   {
      "name": "Iex" + lib_suffix,
      "type": "sharedlib",
      "alias": "iex_shared",
      "defs": (["OPENEXR_DLL", "IEX_EXPORTS"] if sys.platform == "win32" else []),
      "incdirs": [out_headers_dir],
      "srcs": glob.glob("IlmBase/Iex/*.cpp")
   },
   # IexMath
   {
      "name": "IexMath" + static_lib_suffix,
      "type": "staticlib",
      "alias": "iexmath_static",
      "incdirs": [out_headers_dir],
      "srcs": glob.glob("IlmBase/IexMath/*.cpp")
   },
   {
      "name": "IexMath" + lib_suffix,
      "type": "sharedlib",
      "alias": "iexmath_shared",
      "defs": (["OPENEXR_DLL", "IEXMATH_EXPORTS"] if sys.platform == "win32" else []),
      "incdirs": [out_headers_dir],
      "srcs": glob.glob("IlmBase/IexMath/*.cpp"),
      "libs": ["Iex" + lib_suffix]
   },
   # Imath
   {
      "name": "Imath" + static_lib_suffix,
      "type": "staticlib",
      "alias": "imath_static",
      "incdirs": [out_headers_dir],
      "srcs": glob.glob("IlmBase/Imath/*.cpp")
   },
   {
      "name": "Imath" + lib_suffix,
      "type": "sharedlib",
      "alias": "imath_shared",
      "defs": (["OPENEXR_DLL", "IMATH_EXPORTS"] if sys.platform == "win32" else []),
      "incdirs": [out_headers_dir],
      "srcs": glob.glob("IlmBase/Imath/*.cpp"),
      "libs": ["Iex" + lib_suffix]
   },
   # IlmThread
   {
      "name": "IlmThread" + static_lib_suffix,
      "type": "staticlib",
      "alias": "ilmthread_static",
      "incdirs": [out_headers_dir],
      "srcs": ilmthread_srcs
   },
   {
      "name": "IlmThread" + lib_suffix,
      "type": "sharedlib",
      "alias": "ilmthread_shared",
      "defs": (["OPENEXR_DLL", "ILMTHREAD_EXPORTS"] if sys.platform == "win32" else []),
      "incdirs": [out_headers_dir],
      "srcs": ilmthread_srcs,
      "libs": ["Iex" + lib_suffix]
   },
   # IlmImf
   {
      "name": "b44ExpLogTable",
      "type": "program",
      "incdirs": [out_headers_dir, "OpenEXR/IlmImf"],
      "srcs": ["OpenEXR/IlmImf/b44ExpLogTable.cpp"],
      "staticlibs": ["IlmThread" + static_lib_suffix,
                     "Iex" + static_lib_suffix,
                     "Half" + static_lib_suffix],
      "custom": [threads.Require]
   },
   {
      "name": "dwaLookups",
      "type": "program",
      "incdirs": [out_headers_dir, "OpenEXR/IlmImf"],
      "srcs": ["OpenEXR/IlmImf/dwaLookups.cpp"],
      "staticlibs": ["IlmThread" + static_lib_suffix,
                     "Iex" + static_lib_suffix,
                     "Half" + static_lib_suffix],
      "custom": [threads.Require]
   },
   {
      "name": "IlmImf" + static_lib_suffix,
      "type": "staticlib",
      "alias": "ilmimf_static",
      "defs": openexr_defs,
      "incdirs": [out_headers_dir],
      "srcs": ilmimf_srcs
   },
   {
      "name": "IlmImf" + lib_suffix,
      "type": "sharedlib",
      "alias": "ilmimf_shared",
      "defs": openexr_defs + (["OPENEXR_DLL", "ILMIMF_EXPORTS"] if sys.platform == "win32" else []),
      "incdirs": [out_headers_dir],
      "srcs": ilmimf_srcs,
      "libs": ["IlmThread" + lib_suffix,
               "Imath" + lib_suffix,
               "Iex" + lib_suffix,
               "Half" + lib_suffix],
      "custom": [threads.Require, zlib.Require]
   },
   # IlmImfUtil
   {
      "name": "IlmImfUtil" + static_lib_suffix,
      "type": "staticlib",
      "alias": "ilmimfutil_static",
      "defs": openexr_defs,
      "incdirs": [out_headers_dir],
      "srcs": glob.glob("OpenEXR/IlmImfUtil/*.cpp")
   },
   {
      "name": "IlmImfUtil" + lib_suffix,
      "type": "sharedlib",
      "alias": "ilmimfutil_shared",
      "defs": openexr_defs + (["OPENEXR_DLL", "ILMIMF_EXPORTS"] if sys.platform == "win32" else []),
      "incdirs": [out_headers_dir],
      "srcs": glob.glob("OpenEXR/IlmImfUtil/*.cpp"),
      "libs": ["IlmImf" + lib_suffix,
               "IlmThread" + lib_suffix,
               "Imath" + lib_suffix,
               "Iex" + lib_suffix,
               "Half" + lib_suffix],
      "custom": [threads.Require, zlib.Require]
   },
   # tests
   {
      "name": "HalfTest",
      "type": "program",
      "incdirs": [out_headers_dir, "IlmBase/HalfTest"],
      "srcs": glob.glob("IlmBase/HalfTest/*.cpp"),
      "staticlibs": ["Half" + static_lib_suffix]
   },
   {
      "name": "IexTest",
      "type": "program",
      "incdirs": [out_headers_dir, "IlmBase/IexTest"],
      "srcs": glob.glob("IlmBase/IexTest/*.cpp"),
      "staticlibs": ["Iex" + static_lib_suffix]
   },
   {
      "name": "ImathTest",
      "type": "program",
      "incdirs": [out_headers_dir, "IlmBase/ImathTest"],
      "srcs": glob.glob("IlmBase/ImathTest/*.cpp"),
      "staticlibs": ["Imath" + static_lib_suffix,
                     "Iex" + static_lib_suffix]
   },
   {
      "name": "IlmImfTest",
      "type": "program",
      "defs": openexr_defs,
      "incdirs": [out_headers_dir, "OpenEXR/IlmImfTest"],
      "srcs": glob.glob("OpenEXR/IlmImfTest/*.cpp"),
      "staticlibs": ["IlmImf" + static_lib_suffix,
                     "IlmThread" + static_lib_suffix,
                     "Imath" + static_lib_suffix,
                     "Iex" + static_lib_suffix,
                     "Half" + static_lib_suffix],
      "custom": [threads.Require, zlib.Require]
   },
   {
      "name": "IlmImfUtilTest",
      "type": "program",
      "defs": openexr_defs,
      "incdirs": [out_headers_dir, "OpenEXR/IlmImfUtilTest"],
      "srcs": glob.glob("OpenEXR/IlmImfUtilTest/*.cpp"),
      "staticlibs": ["IlmImfUtil" + static_lib_suffix,
                     "IlmImf" + static_lib_suffix,
                     "IlmThread" + static_lib_suffix,
                     "Imath" + static_lib_suffix,
                     "Iex" + static_lib_suffix,
                     "Half" + static_lib_suffix],
      "custom": [threads.Require, zlib.Require]
   }
]

for d in glob.glob("OpenEXR/exr*"):
   if not os.path.isdir(d):
      continue
   
   if not os.path.isfile(d+"/CMakeLists.txt"):
      continue

   prjs.append({"name": os.path.basename(d),
                "type": "program",
                "defs": openexr_defs,
                "incdirs": [out_headers_dir, d],
                "srcs": glob.glob(d+"/*.cpp"),
                "staticlibs": ["IlmImf" + static_lib_suffix,
                               "IlmThread" + static_lib_suffix,
                               "Imath" + static_lib_suffix,
                               "Iex" + static_lib_suffix,
                               "Half" + static_lib_suffix],
                "custom": [threads.Require, zlib.Require]})

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

   prjs[15]["version"] = "2.2.0"
   prjs[15]["soname"] = "libIlmImf.so.2"
   prjs[15]["install_name"] = "libIlmImf.2.dylib"

   prjs[17]["version"] = "2.2.0"
   prjs[17]["soname"] = "libIlmImfUtil.so.2"
   prjs[17]["install_name"] = "libIlmImfUtil.2.dylib"


tgts = excons.DeclareTargets(env, prjs)


env.Alias("libs", ["half_static", "half_shared",
                   "iex_static", "iex_shared",
                   "iexmath_static", "iexmath_shared",
                   "imath_static", "imath_shared",
                   "ilmthread_static", "ilmthread_shared",
                   "ilmimf_static", "ilmimf_shared",
                   "ilmimfutil_static", "ilmimfutil_shared"] +
                   half_headers +
                   iex_headers +
                   iexmath_headers +
                   imath_headers +
                   ilmthread_headers +
                   ilmimf_headers,
                   ilmimfutil_headers)

env.Alias("staticlibs", ["half_static",
                         "iex_static",
                         "iexmath_static",
                         "imath_static",
                         "ilmthread_static",
                         "ilmimf_static",
                         "ilmimfutil_static"] +
                         half_headers +
                         iex_headers +
                         iexmath_headers +
                         imath_headers +
                         ilmthread_headers +
                         ilmimf_headers,
                         ilmimfutil_headers)

env.Alias("sharedlibs", ["half_shared",
                         "iex_shared",
                         "iexmath_shared",
                         "imath_shared",
                         "ilmthread_shared",
                         "ilmimf_shared",
                         "ilmimfutil_shared"] +
                         half_headers +
                         iex_headers +
                         iexmath_headers +
                         imath_headers +
                         ilmthread_headers +
                         ilmimf_headers,
                         ilmimfutil_headers)

env.Alias("tests", ["HalfTest",
                    "IexTest",
                    "ImathTest",
                    "IlmImfTest",
                    "IlmImfUtilTest"])

env.Alias("bin", filter(lambda x: x.startswith("exr"), tgts.keys()))
