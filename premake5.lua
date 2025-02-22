workspace "krii"
  configurations { "debug", "release" }
  architecture "x64"
  location "build"

  include "vendor/lpeg"

project "krii"
  kind "ConsoleApp"
  language "C"
  targetdir "build/bin/%{cfg.buildcfg}"
  objdir "build/obj/%{cfg.buildcfg}"

  files {
    "src/**.c",
    "vendor/luax/lutf8lib.c",
    "tools/krii.rc"
  }

  includedirs {
    "vendor/luajit/include",
    "vendor/luax",
    "vendor/uv/include"
  }

  libdirs {
    "vendor/luajit/lib",
    "vendor/uv/lib"
  }

  links {
    "lpeg",
    "lua51",
    "uv"
  }

  postbuildcommands {
    "{COPYDIR} ../data %{cfg.targetdir}/data",
    "{COPYFILE} ../vendor/luajit/lib/lua51.dll %{cfg.targetdir}",
    "{COPYFILE} ../vendor/uv/lib/uv.dll %{cfg.targetdir}",
  }

  filter "configurations:debug"
    defines { "DEBUG" }
    symbols "On"

  filter "configurations:release"
    defines { "NDEBUG" }
    optimize "On"
