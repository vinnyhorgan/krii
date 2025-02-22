#include "api.h"

#include <uv.h>

int main(int argc, char** argv) {
  argv = uv_setup_args(argc, argv);

  lua_State* L = luaL_newstate();
  luaL_openlibs(L);

  luax_preload(L, luaopen_krii, "krii");

  lua_newtable(L);
  for (int i = 1; i < argc; i++) {
    lua_pushstring(L, argv[i]);
    lua_rawseti(L, -2, i);
  }
  lua_setglobal(L, "arg");

  lua_getglobal(L, "require");
  lua_pushstring(L, "krii");
  lua_call(L, 1, 1);
  lua_pop(L, 1);

  char exe_path[1024];
  size_t size = sizeof(exe_path);
  uv_exepath(exe_path, &size);

  char* last_slash = strrchr(exe_path, '\\');
  if (last_slash) {
    *last_slash = '\0';
  }

  lua_getglobal(L, "package");
  lua_getfield(L, -1, "path");
  const char* current_path = lua_tostring(L, -1);
  lua_pop(L, 1);

  lua_pushfstring(L, "%s/?.lua;%s/?/init.lua;%s", exe_path, exe_path, current_path);
  lua_setfield(L, -2, "path");
  lua_pop(L, 1);

  lua_getglobal(L, "require");
  lua_pushstring(L, "data");
  if (lua_pcall(L, 1, 1, 0) != LUA_OK) {
    printf("failed to load data folder\n");
    lua_close(L);
    return 1;
  }

  lua_call(L, 0, 1);

  int ret = 0;
  if (lua_isnumber(L, -1)) {
    ret = (int)lua_tonumber(L, -1);
  }

  lua_close(L);

  return ret;
}
