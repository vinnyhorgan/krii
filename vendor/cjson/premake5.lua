project "cjson"
  kind "StaticLib"
  language "C"
  targetdir "../../build/cjson/bin/%{cfg.buildcfg}"
  objdir "../../build/cjson/obj/%{cfg.buildcfg}"

  files { "**.c" }

  includedirs {
    "../luajit/include"
  }

  defines { "strncasecmp=_strnicmp" }

  filter "system:windows"
    buildoptions { "/wd4244", "/wd4267", "/wd4311" }

  filter "configurations:debug"
    defines { "DEBUG" }
    symbols "On"

  filter "configurations:release"
    defines { "NDEBUG" }
    optimize "On"
