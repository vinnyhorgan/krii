#include "api.h"

#include <lutf8lib.h>

static const luaL_Reg modules[] = {
  { "lpeg", luaopen_lpeg },
  { "utf8", luaopen_utf8 },
  { NULL, NULL },
};

static int l_krii_get_version(lua_State* L) {
  lua_pushstring(L, KRII_VERSION);
  return 1;
}

int luaopen_krii(lua_State* L) {
  luax_insistglobal(L, "krii");

  lua_pushcfunction(L, l_krii_get_version);
  lua_setfield(L, -2, "get_version");

  for (int i = 0; modules[i].name; i++) {
    luax_preload(L, modules[i].func, modules[i].name);
  }

  return 1;
}
