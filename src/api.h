#ifndef API_H
#define API_H

#include <lauxlib.h>
#include <lua.h>
#include <lualib.h>

#define KRII_VERSION "0.1.0"

int luaopen_krii(lua_State* L);

void luax_preload(lua_State* L, lua_CFunction f, const char* name);
void luax_insistglobal(lua_State* L, const char* k);

#endif
