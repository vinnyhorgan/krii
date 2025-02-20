workspace "krii"
  configurations { "debug", "release" }
  architecture "x64"
  location "build"

project "krii"
  kind "ConsoleApp"
  language "C"
  targetdir "build/bin/%{cfg.buildcfg}"
  objdir "build/obj/%{cfg.buildcfg}"

  files { "src/**.c", "tools/krii.rc" }

  filter "configurations:debug"
    defines { "DEBUG" }
    symbols "On"

  filter "configurations:release"
    defines { "NDEBUG" }
    optimize "On"
