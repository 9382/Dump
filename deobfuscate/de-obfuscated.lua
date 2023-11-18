--FOR COMMENTS ON THE FLOW OF THE FUNCTION ORIGINALLY OBFUSCATED, LOOK FOR local function N(n, A, B, ...)
--[[ General comments:
Part of this script was simplified using some basic regexs
Then I applied my own rewriter logic to make it neat
And then the rest of the simplification is manual work
Quite a lot of this script is all bark and no bite:
  it tries to be threatening with statements like "((-...)._ * (-...)._) <= (-(#(not ...)))"
  but, when the script is neatened, its plain obvious these never fire, beginning with statements like "if (not true) then"
  (as if the modifications it was applying wasn't obvious enough to realise beforehand it couldn't ever be firing)
After removing the bait, its literally just an incredibly standard process of decrypt a string for tables with statement/expression info and run it in a VM
Really not that hard to decompile given just a decent amount of patience
--]]
return (function(F, n)
	--All of these are from the `n` table, written here for convenience
	local M = 2479
	local I = 628
	local b = 1803
	local U = 2305
	local P = 1431
	local W = 1614
	local Q = 820
	local L = 1836
	local O = 421
	local Un = 1364
	local Vn = 1023
	local Gn = 2047
	local Nn = 32
	local Wn = 21
	local In = 1272
	local Hn = 1359
	local B = 65536
	local h = 16777216
	local A = 4
	local d = 16
	local u = 3
	local Mn = 36
	local c = 256
	local bn = 1266
	local sn = 2892
	local Pn = 2822
	local wn = 1238
	local hn = 2787
	local un = 2735
	local fn = 2652
	local rn = 2627
	local cn = 2538
	local An = 2451
	local Dn = 1198
	local Bn = 1191
	local Cn = 2421
	local En = 1162
	local Fn = 2354
	local kn = 2314
	local vn = 1137
	local Ln = 1132
	local zn = 1034
	local pn = 2276
	local qn = 1031
	local yn = 967
	local oo = 913
	local eo = 895
	local to = 855
	local xo = 840
	local lo = 2264
	local mn = 2202
	local no = 833
	local jn = 762
	local Yn = 2138
	local Kn = 679
	local Tn = 102
	local On = 1627
	local Qn = 1599
	local Zn = 12
	local Rn = 81
	local Sn = 120
	local gn = 478
	local Xn = 1950
	local an = 402
	local Jn = 1867
	local Z = 308
	local xn = 1808
	local p = 1766
	local X = 1395
	local R = 1366
	local Y = 265
	local S = 1727
	local i = 222
	local v = 162
	local m = 1628
	local j = 1518
	local y = 204
	local q = 1432
	local K = 586
	local g = 2063
	local T = 2005
	local G = 499
	local s = 1983
	local w = 497
	local D = 1319
	local E = 355
	local N = 382
	local H = 393
	local V = 489
	local J = 1247
	local f = 568
	local a = 1089
	local z = 773
	local nn = 633
	local C = 725
	local dn = 1163
	local x = 0
	local tn = 801
	local l = 1038
	local on = 993
	local en = 981
	local ln = 880
	local e = 2
	local t = 1
	local getfenv = (getfenv or function(...)
		return _ENV
	end)
	local r, o = "", (getfenv(1))
	local ao, ao = (e ^ 32), ((e ^ ((#{[542] = 379, 973}) + 31)) - t)
	local l = (o[(n[ln] .. ("i" .. (n[en] .. (n[on] .. n[l]))))] or o["bit"])
	--bit xor, not important to us
	local l = ((l and l[("bxor")]) or function(n, o)
		local t, d = t, 0
		while ((n > x) and (o > x)) do
			local x, l = (n % e), (o % (4 - 2))
			if (x ~= l) then
				d = (d + t)
			end
			n, o, t = ((n - x) / e), ((o - l) / e), (t * (2 + 0))
		end
		if (n < o) then
			n = o
		end
		while (n > x) do
			local o = (n % e)
			if (o > x) then
				d = (d + t)
			end
			n, t = ((n - o) / e), (t * (4 - 2))
		end
		return d
	end)
	--A bunch of standard functions, pre-compiled from the `n` table
	local C = string.char
	local a = string.byte
	local f = string.sub
	local r = rawset
	local g = math.ldexp
	local E = tonumber
	local H = select
	local r = pairs
	local w = unpack or table.unpack
	local J = setmetatable
	local r = table.remove
	local r = table.insert
	local G = table.concat
	local S = (table.create or function(n)
		return {unpack({}, 1, n)} --table with n nil elements (why though???)
	end)
	-- From this point on is the string decrypting process - I frankly do not care what it does because thats not important to us, we can just hook the output later and borrow it
	local i = 256
	local r, D = {}, {}
	for n = 0, 255 do
		local o = string.char(n)
		r[n] = o
		D[n] = o
		D[o] = n
	end
	local function s(l)
		local o, d, e = "", "", {}
		local n = t
		local function x()
			local o = E(string.sub(l, n, n), Mn)
			n = (n + t)
			local t = E(string.sub(l, n, ((n + o) - t)), 36)
			n = (n + o)
			return t
		end
		o = string.char(x())
		e[t] = o
		while (n < (#l)) do
			local n = x()
			if r[n] then
				d = r[n]
			else
				d = (o .. string.sub(o, t, 1))
			end
			r[i] = (o .. string.sub(d, t, 1))
			e[((#e) + t)], o, i = d, d, (i + t)
		end
		return (G(e))
	end
	local r, o = (s(F)), t
	local function C()
		local n, t, x, e = string.byte(r, o, (o + u))
		n = l(n, d)
		t = l(t, d)
		x = l(x, d)
		e = l(e, d)
		o = (o + A)
		return ((((e * h) + (x * B)) + (t * c)) + n)
	end
	local function R()
		local t, n = string.byte(r, o, (o + e))
		t = l(t, d)
		n = l(n, d)
		o = (o + e)
		return ((n * c) + t)
	end
	local function Y()
		local n = l(string.byte(r, o, o), d)
		o = (o + t)
		return n
	end
	local function E(d, n, o)
		if o then
			local n = ((d / (e ^ (n - t))) % (((#{((#{}) + 815), [359] = 677, 589}) + 0) ^ (((o - t) - (n - t)) + 1)))
			return (n - (n % t))
		else
			local n = (e ^ (n - t))
			return ((((d % (n + n)) >= n) and t) or 0)
		end
	end
	local K = n[(-Hn)]
	local function GetVarargsInfo(...)
		return {...}, select(K, ...)
	end
	local function V(...) --this function decrypts the string into useful tables. Not important how it does, it just does - what a convenient hook point!
		local i = {}
		local G = {}
		local N = {}
		local F, s, w, n = string.byte(r, o, (o + u))
		F = l(F, d)
		s = l(s, d)
		w = l(w, d)
		n = l(n, d)
		o = (o + A)
		local n = ((((n * h) + (w * B)) + (s * c)) + F)
		for n = x, (n - t), 1 do
			local F = R()
			if (F == Z) then
				local d = l(string.byte(r, o, o), d)
				o = (o + t)
				local o = d
				local o = o
				i[n] = (o ~= x)
			elseif (F == In) then
				while true do
					local r, a, u, f = string.byte(r, o, (o + u))
					r = l(r, d)
					a = l(a, d)
					u = l(u, d)
					f = l(f, d)
					o = (o + A)
					local o = ((((f * h) + (u * B)) + (a * c)) + r)
					local o = o
					local d = C()
					local a = t
					local l = ((E(d, t, 20) * (e ^ 32)) + o)
					local o = E(d, Wn, ((#{[285] = 472, 115, 799}) + 29))
					local d = ((-t) ^ E(d, Nn))
					if (o == x) then
						if (l == x) then
							i[n] = (d * x)
							break
						else
							o = t
							a = x
						end
					elseif (o == Gn) then
						i[n] = (((l == x) and (d * (t / 0))) or (d * (x / 0)))
						break
					end
					i[n] = (g(d, (o - Vn)) * (a + (l / (e ^ 52))))
					break
				end
			elseif (F == Un) then
				local e = ''
				local E, C, u, F = string.byte(r, o, (o + u))
				E = l(E, d)
				C = l(C, d)
				u = l(u, d)
				F = l(F, d)
				o = (o + A)
				local c = ((((F * h) + (u * B)) + (C * c)) + E)
				local c = c
				if (c == x) then
					i[n] = e
				else
					local x = string.sub(r, o, ((o + c) - t))
					o = (o + c)
					for n = t, (#x), t do
						e = (e .. D[l(string.byte(string.sub(x, n, n)), d)])
					end
					i[n] = e
				end
			else
				i[n] = nil
			end
		end
		for n = x, (C() - t), ((#{2, [930] = ((#{}) + 627), ((#{}) + 536), [519] = ((#{}) + 385), ((#{847}) + 792), ((#{[815] = 4, 817, 573, 739, [648] = 652, 392}) + 618)}) - 3) do
			N[n] = V()
		end
		for w = t, C(), t do
			local D = Y()
			if (E(D, t, 1) == x) then
				local F = (C())
				local i, f, x, n = string.byte(r, o, (o + u))
				i = l(i, d)
				f = l(f, d)
				x = l(x, d)
				n = l(n, d)
				o = (o + A)
				local n = ((((n * h) + (x * B)) + (f * c)) + i)
				local C = n
				local f, x, n, i = string.byte(r, o, (o + u))
				f = l(f, d)
				x = l(x, d)
				n = l(n, d)
				i = l(i, d)
				o = (o + A)
				local n = ((((i * h) + (n * B)) + (x * c)) + f)
				local x = n
				local n, a = string.byte(r, o, (o + e))
				n = l(n, d)
				a = l(a, d)
				o = (o + e)
				local n = ((a * c) + n)
				local l = n
				local d = E(D, e, 3)
				if ((d == e) or (d == u)) then
					x = (x - (e ^ 16))
				end
				G[(w - t)] = {[O] = C, [L] = l, [Q] = x, [W] = F}
			end
		end
		local n = Y()
		return {[P] = N, [U] = n, [b] = i, [I] = G, [M] = (2 - 2)}
	end
	local function N(n, A, B, ...)
		--This is basically a lua VM in lua, written in the worst way possible (on purpose of course)
		local V = n[1431] --A table - in our example, it's got one table in it, similar to the input table. I assume this is the body of every function that isn't the main function
		local s = n[628] --A table of instructions with a type (1836) and 3 other potential values to mean things in context
		local c = n[1803] --Some sort of constants table
		local h = n[2305] --A number, in our example its 1. Unsure what role this plays as of now
		local u = n[2479] --A number, in our example its 0. Seems to be our starting instruction (and is only incremented by the decrypt statement, which makes sense)
		return function(...)
			local i = -1
			local U = {}
			local C = {...}
			local F = (select(K, ...) - 1) --the -1 is because everything here is 0 indexed
			local E = {} --A magical table related to function execution. Its never read from (Not fully removed debug stacktrace maybe?).
			local o = {} --register holder (if thats what it is anyways)
			local r = 1614
			local e = 820
			local d = 421
			for n = x, F, 1 do --store the varargs into the "pointers"... i think
				if (n >= h) then
					U[(n - h)] = C[(n + 1)]
				else
					o[n] = C[(n + 1)]
				end
			end
			local x = u
			local n, t = nil, nil
			while true do
				n = s[x]
				t = n[1836]
				--[=[ Notes on the function flow
				They seem to have used 2 IDs for each potential statement/expression, possibly in an attempt to obscure because 21 events was too easy to debug
				Either way, I've merged each of them for simplicity
				I also simplified the weird <= > < == format used to make tracking the flow harder and turned it into simple a if elseif chain since thats what it is in disguise
				Each statement has a comment before it on what it does

				For convenience, I will be referencing indexes 421, 820, and 1614 (originally d, e, and r) as 1, 2, and 3 respectively
				In a similar pattern, you can consider expr[4] / expr[0] to be the "type" if this was to be sequentially ordered (I won't generally be commenting on that though)

				Note that while I call the table `o` a "register" table, I'm not actually sure thats 100% right - just go with me here ok?
				Also saying "upvalue" to describe table A may not be entirely accurate but its close enough I guess

				What we do, based on a dump of the original V() input, picked apart by hand:
				* 8  -> Decrypt constant 2 ("¨Óõ■Ô♥☺♣♦☻") and write the output ("print") to constant 0, and then skip this instruction in the future
				* 12 -> Reset the register and then assign the VarArgs to it (not important to us here since this is the main scope and we don't care about them)
				* 3  -> Set reg[0] to false
				* 7  -> Jump to instruction 7+1 as reg[0] is not truthy (not too sure why this jump exists)
				[ Jumping ... ]
				* 15 -> Set reg[0] to {} (this is the nums table)
				* 17 -> Set reg[1] to nil
				* 21 -> Set reg[1] to the function V[0] with the planned upvalues:
					* 9  -> Set to-be-upvalue[0] to (reg, 0)
					* 9  -> Set to-be-upvalue[1] to (reg, 1)
				* 31 -> Set reg[2] to getfenv()[constant[0] ("print")]
				* 43 -> Copy reg[1] (V[0]) to reg[3]
				* 25 -> Copy constant[1] (46) to reg[4]
				* 14 -> Call reg[3] (V[0]) with argument reg[4] (46) and write the (what we know to be singular) output to reg[3] onwards (so just reg[3])
				[ Moving to V[0] (fib) ... ] (Keep in mind reg/constant now refers to this specific function's register)
				* 12 -> Clear the registry and then write the arguments to the registory (so reg[0] = 46)
				* 38 -> Jump to instruction 5+1 because reg[0] (46) is not <= constant[1] (1)
				[ Jumping ... ]
				* 16 -> Set reg[1] to upvalue[0] (the nums table)
				* 37 -> Set reg[1] to __index(reg[1] (nums), reg[0] (46))
				NOTE: In this specific case, reg[1] is nil, as this is our first execution, so the table nums has no cache values
				* 7  -> Jump to instruction 13+1 as reg[1] is not truthy
				[ Jumping ... ]
				* 16 -> Set reg[1] to upvalue[0] (nums)
				* 16 -> Set reg[2] to upvalue[1] (V[0])
				* 39 -> Set reg[3] to reg[0] (46) - constant[1] (1)
				* 32 -> Set reg[2] to reg[2] (V[0]) called with arg reg[3] (46-1)
				[ Skipping over V[0] self-call for simplicity ]
				* 16 -> Set reg[3] to upvalue[1] (V[0])
				* 39 -> Set reg[4] to reg[0] (46) - constant[0] (2)
				* 32 -> Set reg[3] to reg[3] (V[0]) called with arg reg[4] (46-2)
				[ Skipping over V[0] self-call for simplicity ]
				* 1  -> Set reg[2] to reg[2] ( fib(46-1) ) + reg[3] ( fib(46-2) )
				* 20 -> __newindex(reg[1] (nums), reg[0] (46), reg[2] ( the solution to fib(46) ))
				* 16 -> Set reg[1] to upvalue[0] (nums)
				* 37 -> Set reg[1] to __index(reg[1] (nums), reg[0] (46))
				* 26 -> return reg[1] ( nums[46], aka the solution )
				[ Moving back to main scope ... ]
				* 36 -> Call reg[2] (print) with reg[3] ( the output of fib(46) ) (and onwards, if we had more args)
				* 0  -> Finish execution, return nothing

				^^^ This is what the VM does when it executes, decoded by hand
				I've saved myself time by not writing out paths we didn't take and by not doing the self-call stuff (that'd take me years to do by hand!)

				Alternatively, what happened as lua code (kind of, since we ignored seperate paths) with some comments as guidance:
				```lua
				--In this lua-translated example, each "scope" has an incrementally higher registry value
				local reg0 = {}
				reg0[0] = false
				if reg0[0] then
					--[ Undocumented logic ] --not even sure why this exists but its whatever
				else
					reg0[0] = {}
					reg0[1] = nil
					reg0[1] = function(...)
						local reg1 = {}
						local args = {...}
						for i = 1,select("#", ...) do
							reg1[i-1] = args[i]
						end
						--Note: basically just reg1[0] = args[1] since we don't expect more
						if reg1[0] <= 1 then
							--[ Undocumented logic ]
						else
							reg1[1] = reg0[0]
							reg1[1] = reg1[1][reg1[0]] --nums[n]
							if reg1[1] then
								--[ Undocumented logic ]
							else
								reg1[1] = reg0[0]
								reg1[2] = reg0[1]
								reg1[3] = reg1[0] - 1
								reg1[2] = reg1[2](reg1[3]) --fib(n-1)
								reg1[3] = reg0[1]
								reg1[4] = reg1[0] - 2
								reg1[3] = reg1[3](reg1[4]) --fib(n-2)
								reg1[2] = reg1[2] + reg1[3]
								reg1[1][reg1[0]] = reg1[2] --nums[n] = fib(n-1) + fib(n-2)
								reg1[1] = reg0[0]
								reg1[1] = reg1[1][reg1[0]]
								return reg1[1] --return nums[n]
							end
						end
					end
					reg0[2] = getfenv()["print"]
					reg0[3] = reg0[1]
					reg0[4] = 46
					reg0[3] = reg0[3](reg0[4])
					reg0[2](reg0[3]) --print(fib(46))
					return
				end
				```
				--]=]

				--End the statement, return nothing
				if t == 0 or t == 18 then
					return

				--Add the values in register expr[2] and expr[3] and put the result in register expr[1]
				elseif t == 1 or t == 42 then
					o[n[421]] = (o[n[820]] + o[n[1614]])

				--Jump to the instruction expr[2] IF the value in expr[1] is lower than the constant at expr[3] (Not really sure what this is implying?)
				elseif t == 2 or t == 38 then
					if (o[n[421]] <= c[n[1614]]) then
						x = (x + 1)
					else
						x = n[820]
					end

				--Set the value in register expr[1] to the boolean expr[2] (where 0 is false and 1 is true)
				elseif t == 3 or t == 22 then
					o[n[421]] = (n[820] ~= 0)

				--Decrypt the constant in position expr[1] and write it to constant expr[2], then increase the starting instruction by one. Protects constant dumping while being performative I suppose
				elseif t == 4 or t == 8 then
					local x, t = {}, c[n[421]]
					local d = ""
					local o = ((#t) / 2)
					for n = 1, o, 1 do
						x[string.byte(string.sub(t, (o + n), (o + n)))] = D[l(string.byte(string.sub(t, n, n)), 144)]
					end
					for n = 1, o, 1 do
						d = (d .. x[n])
					end
					c[n[820]] = d
					u = (u + 1)

				--Subtracts the values in register expr[2] and expr[3] and put the result in register expr[1]
				elseif t == 5 or t == 39 then
					o[n[421]] = (o[n[820]] - c[n[1614]])

				--Calls the value in register expr[1] with the unpack of register values expr[1]+1 to expr[1]+i (`i` is controlled by statement 10/14, dunno really)
				elseif t == 6 or t == 36 then
					local n = n[421]
					o[n](unpack(o, (n + 1), i))

				--If the value of register expr[1] exists, simply skip the next statement. Otherwise, jump to statement expr[2]
				elseif t == 7 or t == 41 then
					if o[n[421]] then
						x = (x + 1)
					else
						x = n[820]
					end

				--Copy register expr[2] to register expr[1]
				elseif t == 9 or t == 43 then
					o[n[421]] = o[n[820]]

				--Execute the function in register expr[1] with the argument in register expr[1]+1, then assign all the outputs to registers expr[1] onwards (I think)
				elseif t == 10 or t == 14 then
					local n = n[421]
					local d, t = GetVarargsInfo(o[n](o[(n + 1)]))
					i = ((t + n) - 1)
					local t = 0
					for n = n, i do
						t = (t + 1)
						o[n] = d[t]
					end

				--Remove all register values from expr[1] to expr[2]
				elseif t == 11 or t == 17 then
					for n = n[421], n[820] do
						o[n] = nil
					end

				--Reset the registers table and then assign the varargs given into this function to each value in the register from 0 onwards
				--I can't figure out what role "h" plays here considering its part of the entire primary statement - maybe its some sort of indicator about the amount of inputs expected?
				elseif t == 12 or t == 34 then
					o = {}
					for n = 0, F do
						if (n < h) then
							o[n] = C[(n + 1)]
						else
							break
						end
					end

				--Copy constant expr[2] to register expr[1]
				elseif t == 13 or t == 25 then
					o[n[421]] = c[n[820]]

				--Set the value in register expr[1] to an empty table (technically a table with 256 reserved nil values)
				elseif t == 15 or t == 30 then
					o[n[421]] = {} --S(256) -- a table with 256 nil values (aka just an empty table COME ON GUYS)

				--Copy upvalue (kinda) expr[2] to register expr[1]
				elseif t == 16 or t == 33 then
					o[n[421]] = A[n[820]]

				--Return the value in register expr[1]
				elseif t == 19 or t == 26 then
					return o[n[421]]

				--I don't know how to write this in words, so have this: __newindex(register expr[1], register expr[2], register expr[3])
				elseif t == 20 or t == 28 then
					o[n[421]][o[n[820]]] = o[n[1614]]

				--Execute a statementlist (basically a function). "l" is the function's upvalue (kinda) table
				--Not entirely sure what the "for d = " line does, and my brain is dying right now so I'm not gonna solve that one
				elseif t == 21 or t == 23 then
					local a = V[n[820]]
					local l, t = nil, {}
					l = setmetatable({}, {__index = function(o, n)
						local n = t[n]
						return n[1][n[2]]
					end, __newindex = function(d, n, o)
						local n = t[n]
						n[1][n[2]] = o
					end})
					for d = 1, n[1614], 1 do
						x = (x + 1)
						local n = s[x]
						if (n[1836] == 9) then
							t[(d - 1)] = {o, n[820]}
						else
							t[(d - 1)] = {A, n[820]}
						end
						E[((#E) + 1)] = t
					end
					o[n[421]] = N(a, l, B)

				--Set register expr[1] to register expr[1] called wih argument register expr[1]+1
				elseif t == 24 or t == 32 then
					local n = n[421]
					o[n] = o[n](o[(n + 1)])

				--Set register expr[1] to getfenv()[constant expr[2]] (The global that constant expr[2] represents)
				elseif t == 27 or t == 31 then
					o[n[421]] = B[c[n[820]]]

				--Jump to instruction expr[2] (why not expr[1]? oh well, probably some synergy with statement 2/38)
				elseif t == 29 or t == 40 then
					x = n[820]

				--Set the value of register expr[1] to __index(register expr[2], register expr[3])
				elseif t == 35 or t == 37 then
					o[n[421]] = o[n[820]][o[n[1614]]]

				end
				--Move to the next instruction
				x = (x + 1)
			end
		end
	end
	local a, b, c = V(), {}, getfenv()
	-- "a" is the decrypted abstract syntax tree, "b" is the upvalues table (kinda) (an empty table for the main function), and "c" is the env / _G
	-- print("A=", PrintTable(a), "B=", PrintTable(b), "C=", PrintTable(c))
	local out = N(a, b, c)() --Main body/entrance point
	-- print("A=", PrintTable(a), "B=", PrintTable(b), "C=", PrintTable(c))
	return out
end)("1L1G27521W2742751G26G1K27927922F228277122791Y2132111Z27L2152142132122131W1Z2142102122111W2771Q27926H26O26S26M26Q1J1H1L1K1I27H27J27L27N21127P27R27T27V27X27Z1H2791I27927B27D27922828T28U26821B27D1B28U29328U1S1G21I28P29327428P21I1G27C29429B1G21K1G27I2792991G29N1929329N28R2751A29E2941G29Q28P29J28U29N27D1029R29M27921H1G1M27D29N1T29O1G1N29W2942AE2A02A62932A52A22A72752A92AP27529T1G29V29F29329Z29I2AM28U2AO27D2AV29N2A521C29N1J29421J2AU28Q2BF27521C2932BB2752B71G2BI2792AY27D2BD1G2AV2BK2BT2792BO2BV2AV2B62BE2BL294142B22A42B229N2AS2AC2BG2AW29X2C32AC1329X2BV27D1O2CE2952CM27D2BB2AB2942AH28P2AH2BQ27D2CT2B12CW2BP2AF2A12CO1G2CJ2932AV29V2D41G1V2C8279112AA2C12CB152DA1G1P2CM29N2DM29L2C228U1F2BJ2AQ1G21N29K27D2AY29P2DU2752AY1U2CF2BW29321G2DN293", {[-4019]=2479, [-3927]=1614, [-3864]=421, [-3790]=1364, [-3733]=1023, [-3676]=2047, [-3585]=21, [-3499]=1272, [-3469]=1359, [-3441]=16, [-3352]=1266, [-3312]=1238, [-3288]=2735, [-3229]=2627, [-3132]=2538, [-3053]=2421, [-2975]=2314, [-2963]=1132, [-2950]=1034, [-2886]=2276, [-2820]=967, [-2775]=913, [-2698]=855, [-2690]=840, [-2680]=2264, [-2619]=2202, [-2546]=102, [-2499]=1627, [-2441]=1599, [-2388]=81, [-2312]=120, [-2304]=478, [-2256]=402, [-2216]=1867, [-2174]=1808, [-2100]=1766, [-2086]=1395, [-2006]=265, [-1971]=222, [-1953]=162, [-1859]=1628, [-1795]=204, [-1774]=1432, [-1762]=586, [-1715]=499, [-1711]=1983, [-1697]=355, [-1637]=393, [-1592]=1247, [-1559]=568, [-1471]=633, [-1465]=880, [-1420]=2, [-1359]="#", [-1266]="u", [-1238]="r", [-1198]="c", [-1191]="e", [-1162]="a", [-1137]="c", [-1132]="o", [-1034]="e", [-1031]="a", [-967]="t", [-913]="t", [-895]="r", [-855]="i", [-840]="e", [-833]="e", [-762]="l", [-679]="a", [-586]="p", [-499]="l", [-497]="a", [-478]="k", [-402]="l", [-308]="k", [-222]="e", [-162]="l", [-102]="e", [-12]="e", [81]="e", [120]="s", [204]="o", [222]="i", [265]="a", [355]="e", [382]="s", [393]="w", [489]="r", [568]="s", [633]="a", [725]="h", [773]="y", [801]="b", [880]="b", [981]="t", [993]="3", [1038]="2", [1089]="t", [1163]="c", [1247]="u", [1319]="t", [1366]="r", [1395]="s", [1432]="t", [1518]="n", [1599]="t", [1627]="l", [1628]="e", [1727]="c", [1766]="n", [1808]="c", [1867]="b", [1950]="a", [1983]="h", [2005]="e", [2063]="x", [2138]="b", [2202]="r", [2264]="e", [2276]="b", [2314]="a", [2354]="t", [2421]="b", [2451]="r", [2538]="e", [2627]="a", [2652]="t", [2735]="s", [2787]="t", [2822]="g", [2892]="s", [2955]=1, [2993]=981, [3020]=993, [3044]=1038, [3137]=801, [3149]=0, [3157]=1163, [3251]=725, [3308]=773, [3336]=1089, [3340]=489, [3385]=382, [3470]=1319, [3553]=497, [3627]=2005, [3692]=2063, [3763]=1518, [3802]=1727, [3872]=1366, [3935]=308, [4015]=1950, [4080]=12, [4124]=679, [4150]=2138, [4182]=762, [4264]=833, [4334]=895, [4389]=1031, [4401]=1137, [4423]=2354, [4501]=1162, [4526]=1191, [4556]=1198, [4634]=2451, [4702]=2652, [4768]=2787, [4844]=2822, [4932]=2892, [5014]=256, [5033]=36, [5130]=3, [5171]=4, [5178]=16777216, [5185]=65536, [5248]=32, [5296]=1836, [5347]=820, [5428]=1431, [5515]=2305, [5594]=1803, [5619]=628}, function() end);
