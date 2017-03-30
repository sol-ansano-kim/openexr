import os
import sys
import glob
import shutil
import subprocess
import excons
import excons.tools.zlib as zlib
import excons.tools.threads as threads
import excons.tools.python as python
import excons.tools.boost as boost


lib_version = (2, 2, 0)
lib_version_str = "%d.%d.%d" % lib_version
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
      for l in out.split("\r\n"):
         f.write(l+"\n")
   return None


env = excons.MakeBaseEnv()

if sys.platform != "win32":
   env.Append(CPPFLAGS=" -Wno-unused-variable -Wno-unused-parameter")
   if sys.platform == "darwin":
      env.Append(CPPFLAGS=" -Wno-unused-private-field")
   else:
      env.Append(CPPFLAGS=" -Wno-unused-but-set-variable")
else:
   env.Append(CPPDEFINES=["_CRT_SECURE_NO_WARNINGS"])

env["BUILDERS"]["GenerateHeader"] = Builder(action=Action(GenerateHeader, "Generating $TARGET ..."), suffix=".h")

conf = Configure(env)
if conf.TryCompile(gcc_include_asm_avx_check_src, ".cpp"):
   have_gcc_include_asm_avx = True
if conf.TryCompile(_sc_nprocessors_onln_check_src, ".cpp"):
   have_sysconf_nprocessors_onln = True
conf.Finish()

binext = ("" if sys.platform != "win32" else ".exe")

env.GenerateHeader("IlmBase/Half/eLut.h", File("%s/eLut%s" % (excons.OutputBaseDirectory(), binext)))

env.GenerateHeader("IlmBase/Half/toFloat.h", File("%s/toFloat%s" % (excons.OutputBaseDirectory(), binext)))

env.GenerateHeader("OpenEXR/IlmImf/b44ExpLogTable.h", File("%s/b44ExpLogTable%s" % (excons.OutputBaseDirectory(), binext)))

env.GenerateHeader("OpenEXR/IlmImf/dwaLookups.h", File("%s/dwaLookups%s" % (excons.OutputBaseDirectory(), binext)))

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
   openexr_defs.append("ZLIB_WINAPI")

def ilmimf_filter(x):
   name = os.path.splitext(os.path.basename(x))[0]
   return (name not in ["b44ExpLogTable", "dwaLookups"])

ilmimf_headers = env.Install(out_headers_dir, filter(ilmimf_filter, glob.glob("OpenEXR/IlmImf/*.h")))

ilmimf_srcs = filter(ilmimf_filter, glob.glob("OpenEXR/IlmImf/*.cpp"))

ilmimfutil_headers = env.Install(out_headers_dir, glob.glob("OpenEXR/IlmImfUtil/*.h"))

pyiex_headers = env.Install(out_headers_dir, glob.glob("PyIlmBase/PyIex/*.h"))

pyimath_headers = env.Install(out_headers_dir, glob.glob("PyIlmBase/PyImath/*.h"))

def pyimath_filter(x):
   name = os.path.splitext(os.path.basename(x))[0]
   return (name not in ["imathmodule", "PyImathFun", "PyImathBasicTypes", "PyImathM44Array"])

pyimath_all_srcs = glob.glob("PyIlmBase/PyImath/*.cpp")

pyimath_srcs = filter(pyimath_filter, pyimath_all_srcs)

pydefs = (["PLATFORM_BUILD_STATIC"] if sys.platform == "win32" else ["PLATFORM_VISIBILITY_AVAILABLE"])

prjs = []

# Half
prjs.append({"name": "eLut",
             "type": "program",
             "desc": "Half library header generator",
             "prefix": "..",
             "srcs": ["IlmBase/Half/eLut.cpp"]})

prjs.append({"name": "toFloat",
             "type": "program",
             "desc": "Half library header generator",
             "prefix": "..",
             "srcs": ["IlmBase/Half/toFloat.cpp"]})

prjs.append({"name": "Half" + static_lib_suffix,
             "type": "staticlib",
             "desc": "Iex static library",
             "alias": "Half-static",
             "symvis": "default",
             "incdirs": [out_headers_dir],
             "srcs": ["IlmBase/Half/half.cpp"]})

prjs.append({"name": "Half" + lib_suffix,
             "type": "sharedlib",
             "desc": "Half shared library",
             "alias": "Half-shared",
             "defs": (["OPENEXR_DLL", "HALF_EXPORTS"] if sys.platform == "win32" else []),
             "incdirs": [out_headers_dir],
             "srcs": ["IlmBase/Half/half.cpp"]})

if not lib_suffix:
   prjs[-1]["version"] = lib_version_str
   prjs[-1]["soname"] = "libHalf.so.%d" % lib_version[0]
   prjs[-1]["install_name"] = "libHalf.%d.dylib" % lib_version[0]

# Iex
prjs.append({"name": "Iex" + static_lib_suffix,
             "type": "staticlib",
             "desc": "Iex static library",
             "alias": "Iex-static",
             "symvis": "default",
             "incdirs": [out_headers_dir],
             "srcs": glob.glob("IlmBase/Iex/*.cpp")})

prjs.append({"name": "Iex" + lib_suffix,
             "type": "sharedlib",
             "desc": "Iex shared library",
             "alias": "Iex-shared",
             "defs": (["OPENEXR_DLL", "IEX_EXPORTS"] if sys.platform == "win32" else []),
             "incdirs": [out_headers_dir],
             "srcs": glob.glob("IlmBase/Iex/*.cpp")})

if not lib_suffix:
   prjs[-1]["version"] = lib_version_str
   prjs[-1]["soname"] = "libIex.so.%d" % lib_version[0]
   prjs[-1]["install_name"] = "libIex.%d.dylib" % lib_version[0]

# IexMath
prjs.append({"name": "IexMath" + static_lib_suffix,
             "type": "staticlib",
             "desc": "IexMath static library",
             "alias": "IexMath-static",
             "symvis": "default",
             "incdirs": [out_headers_dir],
             "srcs": glob.glob("IlmBase/IexMath/*.cpp")})

prjs.append({"name": "IexMath" + lib_suffix,
             "type": "sharedlib",
             "desc": "IexMath shared library",
             "alias": "IexMath-shared",
             "defs": (["OPENEXR_DLL", "IEXMATH_EXPORTS"] if sys.platform == "win32" else []),
             "incdirs": [out_headers_dir],
             "srcs": glob.glob("IlmBase/IexMath/*.cpp"),
             "libs": ["Iex" + lib_suffix]})

if not lib_suffix:
   prjs[-1]["version"] = lib_version_str
   prjs[-1]["soname"] = "libIexMath.so.%d" % lib_version[0]
   prjs[-1]["install_name"] = "libIexMath.%d.dylib" % lib_version[0]

# Imath
prjs.append({"name": "Imath" + static_lib_suffix,
             "type": "staticlib",
             "desc": "Imath static library",
             "alias": "Imath-static",
             "symvis": "default",
             "incdirs": [out_headers_dir],
             "srcs": glob.glob("IlmBase/Imath/*.cpp")})

prjs.append({"name": "Imath" + lib_suffix,
             "type": "sharedlib",
             "desc": "Imath shared library",
             "alias": "Imath-shared",
             "defs": (["OPENEXR_DLL", "IMATH_EXPORTS"] if sys.platform == "win32" else []),
             "incdirs": [out_headers_dir],
             "srcs": glob.glob("IlmBase/Imath/*.cpp"),
             "libs": ["Iex" + lib_suffix]})

if not lib_suffix:
   prjs[-1]["version"] = lib_version_str
   prjs[-1]["soname"] = "libImath.so.%d" % lib_version[0]
   prjs[-1]["install_name"] = "libImath.%d.dylib" % lib_version[0]

# IlmThread
prjs.append({"name": "IlmThread" + static_lib_suffix,
             "type": "staticlib",
             "desc": "IlmThread static library",
             "alias": "IlmThread-static",
             "symvis": "default",
             "incdirs": [out_headers_dir],
             "srcs": ilmthread_srcs})

prjs.append({"name": "IlmThread" + lib_suffix,
             "type": "sharedlib",
             "desc": "IlmThread shared library",
             "alias": "IlmThread-shared",
             "defs": (["OPENEXR_DLL", "ILMTHREAD_EXPORTS"] if sys.platform == "win32" else []),
             "incdirs": [out_headers_dir],
             "srcs": ilmthread_srcs,
             "libs": ["Iex" + lib_suffix]})

if not lib_suffix:
   prjs[-1]["version"] = lib_version_str
   prjs[-1]["soname"] = "libIlmThread.so.%d" % lib_version[0]
   prjs[-1]["install_name"] = "libIlmThread.%d.dylib" % lib_version[0]

# IlmImf
prjs.append({"name": "b44ExpLogTable",
             "type": "program",
             "desc": "IlmImf library header generator",
             "prefix": "..",
             "symvis": "default",
             "incdirs": [out_headers_dir, "OpenEXR/IlmImf"],
             "srcs": ["OpenEXR/IlmImf/b44ExpLogTable.cpp"],
             "staticlibs": ["IlmThread" + static_lib_suffix,
                            "Iex" + static_lib_suffix,
                            "Half" + static_lib_suffix],
             "custom": [threads.Require]})

prjs.append({"name": "dwaLookups",
             "type": "program",
             "prefix": "..",
             "desc": "IlmImf library header generator",
             "symvis": "default",
             "incdirs": [out_headers_dir, "OpenEXR/IlmImf"],
             "srcs": ["OpenEXR/IlmImf/dwaLookups.cpp"],
             "staticlibs": ["IlmThread" + static_lib_suffix,
                            "Iex" + static_lib_suffix,
                            "Half" + static_lib_suffix],
             "custom": [threads.Require]})

prjs.append({"name": "IlmImf" + static_lib_suffix,
             "type": "staticlib",
             "desc": "IlmImf static library",
             "alias": "IlmImf-static",
             "symvis": "default",
             "defs": openexr_defs,
             "incdirs": [out_headers_dir],
             "srcs": ilmimf_srcs,
             "custom": [zlib.Require]})

prjs.append({"name": "IlmImf" + lib_suffix,
             "type": "sharedlib",
             "desc": "IlmImf shared library",
             "alias": "IlmImf-shared",
             "defs": openexr_defs + (["OPENEXR_DLL", "ILMIMF_EXPORTS"] if sys.platform == "win32" else []),
             "incdirs": [out_headers_dir],
             "srcs": ilmimf_srcs,
             "libs": ["IlmThread" + lib_suffix,
                      "Imath" + lib_suffix,
                      "Iex" + lib_suffix,
                      "Half" + lib_suffix],
             "custom": [threads.Require, zlib.Require]})

if not lib_suffix:
   prjs[-1]["version"] = lib_version_str
   prjs[-1]["soname"] = "libIlmImf.so.%d" % lib_version[0]
   prjs[-1]["install_name"] = "libIlmImf.%d.dylib" % lib_version[0]

# IlmImfUtil
prjs.append({"name": "IlmImfUtil" + static_lib_suffix,
             "type": "staticlib",
             "desc": "IlmImfUtil static library",
             "alias": "IlmImfUtil-static",
             "symvis": "default",
             "defs": openexr_defs,
             "incdirs": [out_headers_dir],
             "srcs": glob.glob("OpenEXR/IlmImfUtil/*.cpp"),
             "custom": [zlib.Require]})

prjs.append({"name": "IlmImfUtil" + lib_suffix,
             "type": "sharedlib",
             "desc": "IlmImfUtil shared library",
             "alias": "IlmImfUtil-shared",
             "defs": openexr_defs + (["OPENEXR_DLL", "ILMIMF_EXPORTS"] if sys.platform == "win32" else []),
             "incdirs": [out_headers_dir],
             "srcs": glob.glob("OpenEXR/IlmImfUtil/*.cpp"),
             "libs": ["IlmImf" + lib_suffix,
                      "IlmThread" + lib_suffix,
                      "Imath" + lib_suffix,
                      "Iex" + lib_suffix,
                      "Half" + lib_suffix],
             "custom": [threads.Require, zlib.Require]})

if not lib_suffix:
   prjs[-1]["version"] = lib_version_str
   prjs[-1]["soname"] = "libIlmImfUtil.so.%d" % lib_version[0]
   prjs[-1]["install_name"] = "libIlmImfUtil.%d.dylib" % lib_version[0]

# Python
prjs.append({"name": "PyIex" + static_lib_suffix,
             "type": "staticlib",
             "desc": "Iex python helper library",
             "symvis": "default",
             "alias": "PyIex",
             "prefix": "python/" + python.Version(),
             "bldprefix": "python" + python.Version(),
             "defs": ["PYIEX_EXPORTS"] + pydefs,
             "incdirs": [out_headers_dir],
             "srcs": ["PyIlmBase/PyIex/PyIex.cpp"],
             "custom": [python.SoftRequire, boost.Require(libs=["python"])]})

prjs.append({"name": "PyImath" + static_lib_suffix,
             "type": "staticlib",
             "desc": "Imath python helper library",
             "symvis": "default",
             "alias": "PyImath",
             "prefix": "python/" + python.Version(),
             "bldprefix": "python" + python.Version(),
             "defs": ["PYIMATH_EXPORTS"] + pydefs,
             "incdirs": [out_headers_dir],
             "srcs": pyimath_srcs,
             "custom": [python.SoftRequire, boost.Require(libs=["python"])]})

prjs.append({"name": "iexmodule",
             "type": "dynamicmodule",
             "desc": "Iex library python bindings",
             "ext": python.ModuleExtension(),
             "prefix": python.ModulePrefix() + "/" + python.Version(),
             "bldprefix": "python" + python.Version(),
             "symvis": "default",
             "defs": pydefs,
             "incdirs": [out_headers_dir],
             "srcs": ["PyIlmBase/PyIex/iexmodule.cpp"],
             "libdirs": [excons.OutputBaseDirectory() + "/lib/python/" + python.Version()],
             "staticlibs": ["PyIex" + static_lib_suffix,
                            "Iex" + static_lib_suffix],
             "custom": [python.SoftRequire, boost.Require(libs=["python"])]})

prjs.append({"name": "imathmodule",
             "type": "dynamicmodule",
             "desc": "Imath library python bindings",
             "ext": python.ModuleExtension(),
             "prefix": python.ModulePrefix() + "/" + python.Version(),
             "bldprefix": "python" + python.Version(),
             "symvis": "default",
             "defs": pydefs,
             "incdirs": [out_headers_dir],
             "srcs": ["PyIlmBase/PyImath/imathmodule.cpp",
                      "PyIlmBase/PyImath/PyImathFun.cpp",
                      "PyIlmBase/PyImath/PyImathBasicTypes.cpp"],
             "libdirs": [excons.OutputBaseDirectory() + "/lib/python/" + python.Version()],
             "staticlibs": ["PyImath" + static_lib_suffix,
                            "PyIex" + static_lib_suffix,
                            "IexMath" + static_lib_suffix,
                            "Imath" + static_lib_suffix,
                            "Iex" + static_lib_suffix],
             "custom": [python.SoftRequire, boost.Require(libs=["python"])]})

# Command line tools
for d in glob.glob("OpenEXR/exr*"):
   if not os.path.isdir(d):
      continue
   
   if not os.path.isfile(d+"/CMakeLists.txt"):
      continue

   prjs.append({"name": os.path.basename(d),
                "type": "program",
                "desc": "Command line tool",
                "defs": openexr_defs,
                "symvis": "default",
                "incdirs": [out_headers_dir, d],
                "srcs": glob.glob(d+"/*.cpp"),
                "staticlibs": ["IlmImf" + static_lib_suffix,
                               "IlmThread" + static_lib_suffix,
                               "Imath" + static_lib_suffix,
                               "Iex" + static_lib_suffix,
                               "Half" + static_lib_suffix],
                "custom": [threads.Require, zlib.Require]})

# Tests
prjs.append({"name": "HalfTest",
             "type": "program",
             "desc": "Half library tests",
             "symvis": "default",
             "incdirs": [out_headers_dir, "IlmBase/HalfTest"],
             "srcs": glob.glob("IlmBase/HalfTest/*.cpp"),
             "staticlibs": ["Half" + static_lib_suffix]})

prjs.append({"name": "IexTest",
             "type": "program",
             "desc": "Iex library tests",
             "symvis": "default",
             "incdirs": [out_headers_dir, "IlmBase/IexTest"],
             "srcs": glob.glob("IlmBase/IexTest/*.cpp"),
             "staticlibs": ["Iex" + static_lib_suffix]})

prjs.append({"name": "ImathTest",
             "type": "program",
             "desc": "Imath library tests",
             "symvis": "default",
             "incdirs": [out_headers_dir, "IlmBase/ImathTest"],
             "srcs": glob.glob("IlmBase/ImathTest/*.cpp"),
             "staticlibs": ["Imath" + static_lib_suffix,
                            "Iex" + static_lib_suffix]})

prjs.append({"name": "IlmImfTest",
             "type": "program",
             "desc": "IlmImf library tests",
             "defs": openexr_defs,
             "symvis": "default",
             "incdirs": [out_headers_dir, "OpenEXR/IlmImfTest"],
             "srcs": glob.glob("OpenEXR/IlmImfTest/*.cpp"),
             "staticlibs": ["IlmImf" + static_lib_suffix,
                            "IlmThread" + static_lib_suffix,
                            "Imath" + static_lib_suffix,
                            "Iex" + static_lib_suffix,
                            "Half" + static_lib_suffix],
             "custom": [threads.Require, zlib.Require]})

prjs.append({"name": "IlmImfUtilTest",
             "type": "program",
             "desc": "IlmImfUtil library tests",
             "defs": openexr_defs,
             "symvis": "default",
             "incdirs": [out_headers_dir, "OpenEXR/IlmImfUtilTest"],
             "srcs": glob.glob("OpenEXR/IlmImfUtilTest/*.cpp"),
             "staticlibs": ["IlmImfUtil" + static_lib_suffix,
                            "IlmImf" + static_lib_suffix,
                            "IlmThread" + static_lib_suffix,
                            "Imath" + static_lib_suffix,
                            "Iex" + static_lib_suffix,
                            "Half" + static_lib_suffix],
             "custom": [threads.Require, zlib.Require]})

build_opts = """OPENEXR OPTIONS
   lib-suffix=<str>             : Library suffix                     ["-2_2"]
   static-lib-suffix=<str>      : Static library addition suffix     ["_s"]
   namespace-version=0|1        : Internally use versioned namespace [1]
   zlib-win-api=0|1             : Use zlib win API                   [0]"""

excons.AddHelpOptions(openexr=build_opts)
excons.AddHelpTargets({"libs": "All libraries",
                       "libs-static": "All static libraries",
                       "libs-shared": "All shared libraries",
                       "ilmbase": "All IlmBase libraries",
                       "ilmbase-static": "All IlmBase static libraries",
                       "ilmbase-shared": "All IlmBase shared librarues",
                       "bins": "All command line tools",
                       "python": "All python bindings",
                       "tests": "All tests"})

tgts = excons.DeclareTargets(env, prjs)

env.Depends(tgts["Half-static"], half_headers)
env.Depends(tgts["Half-shared"], half_headers)

env.Depends(tgts["Iex-static"], iex_headers)
env.Depends(tgts["Iex-shared"], iex_headers)

env.Depends(tgts["IexMath-static"], iexmath_headers)
env.Depends(tgts["IexMath-shared"], iexmath_headers)

env.Depends(tgts["Imath-static"], imath_headers)
env.Depends(tgts["Imath-shared"], imath_headers)

env.Depends(tgts["IlmThread-static"], ilmthread_headers)
env.Depends(tgts["IlmThread-shared"], ilmthread_headers)

env.Depends(tgts["IlmImf-static"], ilmimf_headers)
env.Depends(tgts["IlmImf-shared"], ilmimf_headers)

env.Depends(tgts["IlmImfUtil-static"], ilmimfutil_headers)
env.Depends(tgts["IlmImfUtil-shared"], ilmimfutil_headers)

env.Alias("libs-static", [tgts["Half-static"],
                          tgts["Iex-static"],
                          tgts["IexMath-static"],
                          tgts["Imath-static"],
                          tgts["IlmThread-static"],
                          tgts["IlmImf-static"],
                          tgts["IlmImfUtil-static"]])

env.Alias("libs-shared", [tgts["Half-shared"],
                          tgts["Iex-shared"],
                          tgts["IexMath-shared"],
                          tgts["Imath-shared"],
                          tgts["IlmThread-shared"],
                          tgts["IlmImf-shared"],
                          tgts["IlmImfUtil-shared"]])

env.Alias("ilmbase-static", [tgts["Half-static"],
                             tgts["Iex-static"],
                             tgts["IexMath-static"],
                             tgts["Imath-static"],
                             tgts["IlmThread-static"]])

env.Alias("ilmbase-shared", [tgts["Half-shared"],
                             tgts["Iex-shared"],
                             tgts["IexMath-shared"],
                             tgts["Imath-shared"],
                             tgts["IlmThread-shared"]])

env.Alias("libs", ["libs-static", "libs-shared"])

env.Alias("ilmbase", ["ilmbase-static", "ilmbase-shared"])

env.Alias("bins", [tgts[y] for y in filter(lambda x: x.startswith("exr"), tgts.keys())])

env.Alias("python", [tgts["PyIex"],
                     tgts["PyImath"],
                     tgts["iexmodule"],
                     tgts["imathmodule"]])

env.Alias("tests", [tgts["HalfTest"],
                    tgts["IexTest"],
                    tgts["ImathTest"],
                    tgts["IlmImfTest"],
                    tgts["IlmImfUtilTest"]])
