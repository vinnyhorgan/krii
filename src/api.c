#include "api.h"

void luax_preload(lua_State* L, lua_CFunction f, const char* name) {
  lua_getglobal(L, "package");
  lua_getfield(L, -1, "preload");
  lua_pushcfunction(L, f);
  lua_setfield(L, -2, name);
  lua_pop(L, 2);
}

void luax_insistglobal(lua_State* L, const char* k) {
  lua_getglobal(L, k);
  if (!lua_istable(L, -1)) {
    lua_pop(L, 1);
    lua_newtable(L);
    lua_pushvalue(L, -1);
    lua_setglobal(L, k);
  }
}
