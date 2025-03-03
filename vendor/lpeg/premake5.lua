project "lpeg"
  kind "StaticLib"
  language "C"
  targetdir "../../build/lpeg/bin/%{cfg.buildcfg}"
  objdir "../../build/lpeg/obj/%{cfg.buildcfg}"

  files { "**.c" }

  includedirs {
    "../luajit/include"
  }

  filter "system:windows"
    buildoptions { "/wd4005", "/wd4244", "/wd4267" }

  filter "configurations:debug"
    defines { "LPEG_DEBUG" }
    symbols "On"

  filter "configurations:release"
    defines { "NDEBUG" }
    optimize "On"
