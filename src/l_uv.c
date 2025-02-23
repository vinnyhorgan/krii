#include "api.h"

#include <stdlib.h>
#include <uv.h>

#define TYPE_TIMER "Timer"

typedef struct {
  lua_State* L;
  int cb;
} TimerData;

static int uv_error(lua_State* L, int status) {
  lua_pushnil(L);
  lua_pushfstring(L, "%s: %s", uv_err_name(status), uv_strerror(status));
  lua_pushstring(L, uv_err_name(status));
  return 3;
}

static void callback(uv_timer_t* timer) {
  TimerData* data = timer->data;
  lua_rawgeti(data->L, LUA_REGISTRYINDEX, data->cb);
  lua_call(data->L, 0, 0);
}

static int l_uv_run(lua_State* L) {
  int ret = uv_run(uv_default_loop(), UV_RUN_DEFAULT);
  if (ret < 0) {
    return uv_error(L, ret);
  }
  lua_pushboolean(L, ret);
  return 1;
}

static int l_uv_new_timer(lua_State* L) {
  uv_timer_t* self = lua_newuserdata(L, sizeof(uv_timer_t));
  luaL_setmetatable(L, TYPE_TIMER);
  int ret = uv_timer_init(uv_default_loop(), self);
  if (ret < 0) {
    lua_pop(L, 1);
    return uv_error(L, ret);
  }

  TimerData* data = malloc(sizeof(TimerData));
  if (!data) {
    luaL_error(L, "out of memory");
  }

  data->L = L;
  data->cb = LUA_NOREF;
  self->data = data;
  return 1;
}

static const luaL_Reg functions[] = {
  { "run", l_uv_run },
  { "new_timer", l_uv_new_timer },
  { NULL, NULL },
};

static int l_timer_start(lua_State* L) {
  uv_timer_t* self = luaL_checkudata(L, 1, TYPE_TIMER);
  int timeout = (int)luaL_checkinteger(L, 2);
  int repeat = (int)luaL_checkinteger(L, 3);

  TimerData* data = self->data;
  luaL_checktype(L, 4, LUA_TFUNCTION);
  luaL_unref(L, LUA_REGISTRYINDEX, data->cb);
  data->cb = luaL_ref(L, LUA_REGISTRYINDEX);

  int ret = uv_timer_start(self, callback, timeout, repeat);
  if (ret < 0) {
    return uv_error(L, ret);
  }
  lua_pushinteger(L, ret);
  return 1;
}

static int l_timer_stop(lua_State* L) {
  uv_timer_t* self = luaL_checkudata(L, 1, TYPE_TIMER);
  int ret = uv_timer_stop(self);
  if (ret < 0) {
    return uv_error(L, ret);
  }
  lua_pushinteger(L, ret);
  return 1;
}

static int l_timer_close(lua_State* L) {
  uv_timer_t* self = luaL_checkudata(L, 1, TYPE_TIMER);
  if (uv_is_closing((uv_handle_t*)self)) {
    luaL_error(L, "cannot close a closing handle");
  }
  uv_close((uv_handle_t*)self, NULL);
  return 0;
}

static const luaL_Reg timer_functions[] = {
  { "start", l_timer_start },
  { "stop", l_timer_stop },
  { "close", l_timer_close },
  { NULL, NULL },
};

int luaopen_krii_uv(lua_State* L) {
  luaL_newmetatable(L, TYPE_TIMER);
  lua_pushvalue(L, -1);
  lua_setfield(L, -2, "__index");
  luaL_setfuncs(L, timer_functions, 0);
  lua_pop(L, 1);

  luax_insistglobal(L, "krii");

  lua_newtable(L);
  luaL_setfuncs(L, functions, 0);
  lua_setfield(L, -2, "uv");

  return 1;
}
