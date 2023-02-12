local function CreateExecutionLoop(ast)

	local stringsub, stringbyte, stringrep, stringchar
		= string.sub, string.byte, string.rep, string.char

	local mathfloor, mathlog
		= math.floor, math.log

	local Type, Pairs, Select, Unpack, Getfenv, Error, Tonumber, Tostring, Assert
		= type, pairs, select, unpack, getfenv, error, tonumber, tostring, assert

	local True, False, Nil
		= true, false, nil

	local executeStatList
	local executeExpression

	local function CreateExecutionScope(parent)
		local scope = {}
		scope.P = parent
		scope.L = {}
		function scope:GL(name)
			local my = scope.L[name]
			if my then return my end

			if scope.P then
				local par = scope.P:GL(name)
				if par then return par end
			end

			return Nil
		end
		function scope:SL(name, value)
			local l = scope:GL(name)
			if not l then
				Error("Bad SL "..Tostring(name))
			end
			l[16] = value
		end
		function scope:ML(name, value)
			--create my own var
			local my = {}
			my.S = scope
			my[0] = name
			my[16] = value
			scope.L[name] = my
			return my
		end
		return scope
	end

	local FunctionEnvironment = __ENV or Getfenv()
	local AmbiguityTracker = {}
	local function HandleReturnAmbiguity(t,...)
		--Doing this via a function gets around some of the confusion caused when using {...}
		--This means select cant accidentally trim values inappropriately.

		--Note that the response still has to be sent as a table and later unpacked
		--This means we could lose trailing nils in some scenarios,
		--or varargs in a function call (meaning select("#",...) may become unreliable :/)

		--This is still, however, better than the alternative/old implementation of {...}

		--Note that this automatically handles stupid truncation logic, E.g.
		---- < local a,b,c,d,e = (function()return 1,2,3,4,5 end)(), (function()return 3 end)(); print(a,b,c,d,e)
		---- > 1 3 nil nil nil
		local data = AmbiguityTracker[t] or {1,1}
		--data[1] is data start point, data[2] is truncation end point
		local dots = {...} --This is safe here, no panic needed
		local iterateIndex = data[1]
		for i = iterateIndex,data[2] do --Truncate out old values
			t[i] = Nil
		end
		for i = 1,Select("#",...) do --Push in new values
			t[iterateIndex] = dots[i]
			iterateIndex = iterateIndex + 1
		end
		AmbiguityTracker[t] = {data[1]+1, iterateIndex}
	end
	executeExpression = function(expr, scope, SpecialState)
		if expr[7] == 2 then
			if SpecialState then
				return expr, True
			else
				local LocalDefinition = scope:GL(expr[0])
				if not LocalDefinition then
					if expr[17] then
						Error("Expected '" .. Tostring(expr[0]) .. "' was missing")
					end
				else
					return LocalDefinition[16]
				end
				return FunctionEnvironment[expr[0]]
			end

		elseif expr[7] == 8 then
			return Tonumber(expr[16][29])

		elseif expr[7] == 9 then
			return expr[16][30]

		elseif expr[7] == 11 then
			return expr[16]

		elseif expr[7] == 10 then
			return Nil

		elseif expr[7] == 15 then
			local Lhs = executeExpression(expr[8], scope)
			local Rhs = executeExpression(expr[9], scope)
			local op = expr[12]
			if op == 1 then
				return Lhs + Rhs
			elseif op == 2 then
				return Lhs - Rhs
			elseif op == 3 then
				return Lhs % Rhs
			elseif op == 4 then
				return Lhs / Rhs
			elseif op == 5 then
				return Lhs * Rhs
			elseif op == 6 then
				return Lhs ^ Rhs
			elseif op == 7 then
				return Lhs .. Rhs
			elseif op == 8 then
				return Lhs == Rhs
			elseif op == 9 then
				return Lhs < Rhs
			elseif op == 10 then
				return Lhs <= Rhs
			elseif op == 11 then
				return Lhs ~= Rhs
			elseif op == 12 then
				return Lhs > Rhs
			elseif op == 13 then
				return Lhs >= Rhs
			elseif op == 14 then
				return Lhs and Rhs
			elseif op == 15 then
				return Lhs or Rhs
			end

		elseif expr[7] == 14 then
			local Rhs = executeExpression(expr[9], scope)
			local op = expr[12]
			if op == 1 then
				return -Rhs
			elseif op == 2 then
				return not Rhs
			elseif op == 3 then
				return #Rhs
			end

		elseif expr[7] == 12 then
			return Unpack(scope:GL("...")[16])

		elseif expr[7] == 5 or
		expr[7] == 7 or
		expr[7] == 6 then
			local args = {}
			for _, arg in Pairs(expr[3]) do
				if expr[7] == 6 then
					args = {arg[30]}
				else
					HandleReturnAmbiguity(args, executeExpression(arg, scope))
				end
			end
			return executeExpression(expr[5], scope)(Unpack(args))

		elseif expr[7] == 4 then
			if SpecialState then
				return expr, True
			else
				return executeExpression(expr[5], scope)[executeExpression(expr[2], scope)]
			end

		elseif expr[7] == 3 then
			if SpecialState then
				return expr, True
			else
				if expr[6] == False then
					return executeExpression(expr[5], scope)[expr[4][29]]
				elseif expr[6] == True then --Account for namecall calls of functions by forcing in a self
					local Container = executeExpression(expr[5], scope)
					local out = Container[expr[4][29]]
					if Type(out) == "function" then
						return function(...)
							return out(Container, ...)
						end
					else
						return out
					end
				end
			end

		elseif expr[7] == 1 then
			return function(...)
				local childScope = CreateExecutionScope(scope)
				local inputArgs = {...}
				for i = 1,#expr[3] do
					local arg = expr[3][i]
					if arg then
						childScope:ML(arg[0], inputArgs[i])
					end
				end
				if expr[14] then
					local varargs = {}
					for i = #expr[3]+1, #inputArgs do
						varargs[#varargs+1] = inputArgs[i]
					end
					childScope:ML("...", varargs)
				end
				local ReturnData = executeStatList(expr[1], childScope)
				if not ReturnData then --No return statement to handle
					return
				elseif ReturnData.T == 1 then --Get the return data
					return Unpack(ReturnData.D)
				else --Uh oh!
					local statement = ReturnData.T == 2 and "break" or "continue"
					Error("You tried to "..statement.." when not in a loop and look at where that landed you. Go think about your actions.")
				end
			end

		elseif expr[7] == 13 then
			local out = {}
			--Process all key'd entries first
			for _, entry in Pairs(expr[13]) do
				if entry[27] == 0 then
					out[executeExpression(entry[28], scope)] = executeExpression(entry[16], scope)
				elseif entry[27] == 1 then
					out[entry[28]] = executeExpression(entry[16], scope)
				end
			end
			--And then do the unkey'd ones
			for _, entry in Pairs(expr[13]) do
				if entry[27] == 2 then
					HandleReturnAmbiguity(out, executeExpression(entry[16], scope))
				end
			end
			return out

		end
	end

	local executeStatement = function(statement)
		if statement[7] == 12 then
			local out = {}
			for i = 1, #statement[9] do
				HandleReturnAmbiguity(out, executeExpression(statement[9][i], statement.S))
			end
			for i = 1, #statement[8] do
				local Lhs, wasExprExit = executeExpression(statement[8][i], statement.S, True)
				local Rhs = out[i]
				if wasExprExit then
					if Lhs[7] == 2 then
						if Lhs[17] then
							statement.S:SL(Lhs[0], Rhs)
						else
							FunctionEnvironment[Lhs[0]] = Rhs
						end

					elseif Lhs[7] == 3 then
						local Container = executeExpression(Lhs[5], statement.S)
						Container[Lhs[4][29]] = Rhs

					elseif Lhs[7] == 4 then
						local Container = executeExpression(Lhs[5], statement.S)
						Container[executeExpression(Lhs[2], statement.S)] = Rhs

					else
						Error("Freaky handle "..Tostring(statement[7]))
					end
				end
			end

		elseif statement[7] == 13 then
			executeExpression(statement[21], statement.S)

		elseif statement[7] == 8 then
			local out = {}
			for i = 1, #statement[15] do
				HandleReturnAmbiguity(out, executeExpression(statement[15][i], statement.S))
			end
			for i = 1, #statement[18] do
				local l = statement[18][i]
				statement.S:ML(l[0], out[i])
			end

		elseif statement[7] == 2 then
			for _, Clause in Pairs(statement[11]) do
				if not Clause[10] or executeExpression(Clause[10], statement.S) then
					return executeStatList(Clause[1], CreateExecutionScope(statement.S))
				end
			end

		elseif statement[7] == 3 then
			while executeExpression(statement[10], statement.S) do
				local ReturnData = executeStatList(statement[1], CreateExecutionScope(statement.S))
				if ReturnData then
					if ReturnData.T == 2 then --Break, get out
						return
					elseif ReturnData.T == 1 then
						return ReturnData --Return, propogate
					end --Else: A continue, just keep going
				end
			end

		elseif statement[7] == 4 then
			return executeStatList(statement[1], CreateExecutionScope(statement.S))

		elseif statement[7] == 9 then
			local arguments = {}
			for _, arg in Pairs(statement[3]) do
				HandleReturnAmbiguity(arguments, executeExpression(arg, statement.S))
			end
			return arguments

		elseif statement[7] == 10 then
			return True --This just works, ok?

		elseif statement[7] == 11 then
			return False --This too

		elseif statement[7] == 7 then
			repeat
				local ReturnData = executeStatList(statement[1], CreateExecutionScope(statement.S))
				if ReturnData then
					if ReturnData.T == 2 then --Break, get out
						return
					elseif ReturnData.T == 1 then
						return ReturnData --Return, propogate
					end --Else: A continue, just keep going
				end
			until executeExpression(statement[10], statement.S)

		elseif statement[7] == 1 then
			local name = statement[0]
			if name[7] == 3 then
				if name[6] == False then
					local Container = executeExpression(name[5], statement.S)
					local f = executeExpression(statement, statement.S)
					Container[name[4][29]] = f
				elseif name[6] == True then
					--Make room for a "self" arg
					for i = #statement[3],1,-1 do
						statement[3][i+1] = statement[3][i]
					end
					statement[3][1] = {[0]="self", [17]=True}
					--Continue normal execution
					local Container = executeExpression(name[5], statement.S)
					local f = executeExpression(statement, statement.S, True)
					Container[name[4][29]] = f
				end

			else
				local f = executeExpression(statement, statement.S)
				if statement[22] then
					statement.S:ML(name[0], f)
				else
					FunctionEnvironment[name[0]] = f
				end
			end

		elseif statement[7] == 6 then
			local gen1, gen2, gen3
			local generators = statement[19]
			if not generators[2] then
				gen1, gen2, gen3 = executeExpression(generators[1], statement.S)
			else
				gen1 = executeExpression(generators[1], statement.S)
				gen2 = executeExpression(generators[2], statement.S)
				if generators[3] then
					gen3 = executeExpression(generators[3], statement.S)
				end
			end
			while True do
				local childScope = CreateExecutionScope(statement.S)
				local args = {gen1(gen2, gen3)}
				--We aren't gonna use HandleReturnAmbiguity here, it just isnt worth it as far as im concerned
				gen3 = args[1]
				if gen3 == Nil then
					break
				end
				--Define for-loop locals
				for i = 1, #args do
					childScope:ML(statement[20][i][0], args[i])
				end
				local ReturnData = executeStatList(statement[1], childScope)
				if ReturnData then
					if ReturnData.T == 2 then --Break, get out
						return
					elseif ReturnData.T == 1 then
						return ReturnData --Return, propogate
					end --Else: A continue, just keep going
				end
			end

		elseif statement[7] == 5 then
			local var = Tonumber(executeExpression(statement[23], statement.S))
			local limit = Tonumber(executeExpression(statement[24], statement.S))
			local step = statement[25] and Tonumber(executeExpression(statement[25], statement.S)) or 1

			while (step > 0 and var <= limit) or (step <= 0 and var >= limit) do
				local childScope = CreateExecutionScope(statement.S)
				childScope:ML(statement[26][0], var)
				local ReturnData = executeStatList(statement[1], childScope)
				if ReturnData then
					if ReturnData.T == 2 then --Break, get out
						return
					elseif ReturnData.T == 1 then
						return ReturnData --Return, propogate
					end --Else: A continue, just keep going
				end
				var = var + step
			end

		else
			Error("Had no handle for "..Tostring(statement[7]))
		end
	end

	executeStatList = function(statList, scope)
		--A type of 1 is a return
		--A type of 2 is a break
		--A type of 3 is a continue
		for _, stat in Pairs(statList[1]) do
			stat.S = scope
			local out = executeStatement(stat)
			if Type(out) == "table" then
				if not out.P then --Create an internal token
					return {P = True, T = 1, D = out}
				else --Pass on an internal token
					return out
				end
			elseif Type(out) == "boolean" then --The statement was escaped via a break or continue
				return {P = True, T = (out==True and 2 or 3)}
			end
		end
	end

	return (function()
		ast = (function(x)
			local function padleft(s,n,p)
				return stringrep(p,n-#s)..s
			end
			local function ToNum(b)
				return Tonumber(b,2)
			end
			local function ToBit(n,pad)
				Assert(mathfloor(n) == n,"Can't convert non-int")
				if n == 0 then
					return padleft("0",pad or 1,"0")
				end
				local pow = mathfloor(mathlog(n,2))
				local final = ""
				while pow >= 0 do
					if n >= 2^pow then
						n = n - 2^pow
						final = final .. "1"
					else
						final = final .. "0"
					end
					pow = pow - 1
				end
				return padleft(final,pad or 1,"0")
			end
			local function DBitToNum(dbits)
				local pow = 0
				local result = 0
				for index = 1,#dbits do
					local bit = stringsub(dbits,index,index)
					if bit == "1" then
						result = result + 2^pow
					end
					pow = pow - 1
				end
				return result
			end

			local Buffer = x
			local BitData = ""
			local function BufferSanityCheck(len)
				for i = 1, mathfloor((len-#BitData-1)/6)+1 do
					BitData = BitData .. stringsub(ToBit(stringbyte(Buffer,1,1),8),3,-1)
					Buffer = stringsub(Buffer,2,-1)
				end
			end
			local function ReadRaw(len)
				BufferSanityCheck(len)
				local RequestedData = stringsub(BitData,1,len)
				BitData = stringsub(BitData,len+1)
				return RequestedData
			end
			local function Read(len)
				return ToNum(ReadRaw(len))
			end
			local function ReadByte()
				return stringchar(Read(8))
			end
			local function ReadDouble()
				local sign,Exponent,Mantissa = Read(1),Read(11),ReadRaw(52)
				sign,Exponent = (sign==0 and 1 or -1),2^(Exponent-1023)
				return sign * Exponent * DBitToNum("1"..Mantissa)
			end

			local TYPE_TABLE_START=0
			local TYPE_TABLE_END=1
			local TYPE_STRING=2
			local TYPE_NUMBER=3
			local TYPE_BOOLEAN=4
			local TYPE_NUMBER_BASIC=5
			local TYPE_NUMBER_SUPERBASIC=6
			local TYPE_NUMBER_SIMPLE=7

			local TYPE_WIDTH=3

			local function Deserialize(NoAssert)
				if not NoAssert then
					Assert(Read(TYPE_WIDTH) == TYPE_TABLE_START,"Invalid SD")
				end
				local Output = {}
				local Saved = Nil
				local function HandleKVSorting(Data)
					if Saved then
						Output[Saved] = Data
						Saved = Nil
					else
						Saved = Data
					end
				end
				while True do
					local ObjType = Read(TYPE_WIDTH)
					if ObjType == TYPE_TABLE_END then
						return Output
					elseif ObjType == TYPE_TABLE_START then
						HandleKVSorting(Deserialize(True))
					elseif ObjType == TYPE_STRING then
						local Result = ""
						while True do
							local NextByte = ReadByte()
							if NextByte == "\0" then
								HandleKVSorting(Result)
								break
							elseif NextByte == "\\" then
								Result = Result .. ReadByte()
							else
								Result = Result .. NextByte
							end
						end
					elseif ObjType == TYPE_NUMBER then
						HandleKVSorting(ReadDouble())
					elseif ObjType == TYPE_BOOLEAN then
						HandleKVSorting(Read(1) == 1) --Simple enough
					elseif ObjType == TYPE_NUMBER_BASIC then
						HandleKVSorting(Read(4))
					elseif ObjType == TYPE_NUMBER_SUPERBASIC then
						HandleKVSorting(Read(3))
					elseif ObjType == TYPE_NUMBER_SIMPLE then
						HandleKVSorting(Read(5))
					else
						Error("Unknown Ot "..Tostring(ObjType).." during DS")
					end
				end
			end
			return Deserialize()
		end)(ast)
		local ReturnData = executeStatList(ast, CreateExecutionScope())
		if not ReturnData then --No return statement to handle
			return
		elseif ReturnData.T == 1 then --Get the return data
			return Unpack(ReturnData.D)
		else --Uh oh!
			local statement = ReturnData.T == 2 and "break" or "continue"
			Error("You tried to "..statement.." when not in a loop and look at where that landed you. Go think about your actions.")
		end
	end)
end

local t = CreateExecutionLoop([=[]=])()
print(t)