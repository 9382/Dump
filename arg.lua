-- Turns out, in Lua 5.1, "arg" is a reserved local(??) that the VM will create in any varidic function
-- (Look for `LUA_COMPAT_VARARG` in the source code for a technical explanation)
-- This creates some truly stupid scenarios that you would only experience in Lua 5.1
-- This is so obscure that most VMs probably don't even support this behaviour (FiOne doesn't)

--== Some examples ==--
-- Variable named something that isnt "arg" (works as expected)
local function f1(args)
	return function(...)
		print(args) -- 1
	end
end
f1(1)()
-- Variable named arg, ... isn't used in the body
local function f2(arg)
	return function(...)
		print(arg) -- table: <address>
	end
end
f2(2)()
-- Variable named arg, ... is used in the body
local function f3(arg)
	return function(...)
		print(arg) -- nil
		select("#", ...)
	end
end
f3(3)()

--== Some stupid utility ==--
-- Pure Lua51 testers
local IsLua51 = pcall(function(arg)(function(...)return arg.n end)()end)
local IsLua51 = (function(arg)return(function(...)return arg~=nil end)()end)() -- Alternative version without pcall
