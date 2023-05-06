import ast

_DEBUG = True
def debugprint(*args, **kwargs):
	if _DEBUG:
		print("[Debug]", *args, **kwargs)
if not _DEBUG:
	print("[Debug] debugprint is disabled")

""" Progress Report

== Statements ==
Name				Status				Extra notes

FunctionDef			Implemented
AsyncFunctionDef	Not implemented
ClassDef			Implemented
Return				Implemented

Delete				Implemented
Assign				Implemented
AugAssign			Implemented			Support for an __iXYZ__ attr check? possibly OTT
AnnAssign			Not implemented

For					Implemented			Mostly untested
AsyncFor			Not implemented
While				Implemented
If					Implemented			Partially tested
With				Implemented			Basic implementation works but unsure if there's a more complicated scenario possible
AsyncWith			Not implemented

Match				Not implemented		Switch statement (but called `case`)

Raise				Implemented
Try					Implemented			Mostly untested
Assert				Implemented

Import				Not implemented
ImportFrom			Not implemented

Global				Not implemented		VariableScope needs sorting among other things
Nonlocal			Not implemented		ditto
Expr				Implemented
Pass				Implemented
Break				Implemented			Mostly untested
Continue			Implemented			Mostly untested


== Expressions ==
Name				Status				Extra notes

BoolOp				Implemented
NamedExpr			Implemented
BinOp				Implemented
UnaryOp				Implemented
Lambda				Implemented
IfExp				Implemented
Dict				Implemented
Set					Implemented
ListComp			Implemented			Does not support an async for call
SetComp				Implemented			^
DictComp			Implemented			^
GeneratorExp		Implemented			^

Await				Not implemented
Yield				Not implemented
YieldFrom			Not implemented

Compare				Implemented
Call				Implemented
FormattedValue		Implemented
JoinedStr			Implemented
Constant			Implemented 		`kind` is ignored since idk what the point is

Attribute			Implemented			Some statements manually escape evaluating this (Assign/Delete). That's probably fine though
Subscript			Implemented			ditto
Starred				Implemented			Currently no punishment for >1 Starred expr in Assign. Implemented manually into multiple methods since there's no simple way to provide an unpacking :/
Name				Implemented
List				Implemented
Tuple				Implemented			Leaches off list generator

Slice				Implemented			Part of Subscript. Doesn't support constants (are those a py3.8 thing even?)
Index				Implemented			Undocumented (removed after py3.8?). Part of Subscript.
ExtSlice			Not implemented		Removed after py3.8 (or at least changed). No idea what it actually is cause no damn example is given

== Notes ==

Large lack of support for async calls as of now, and variable scopes need probable work but that'll need full testing to determine
"""
def CreateExecutionLoop(code):
	builtins = __builtins__.__dict__
	builtins["__name__"] = __name__
	class VariableScope:
		def __init__(self, Parent, scopeType):
			self.Parent = Parent
			self.Variables = {}
			self.scopeType = scopeType
			self.References = {}
			self.Assignments = {}
			self.Globals = {}
		def getVar(self, var):
			debugprint("Asked to retrieve variable",var)
			# debugprint(self,self.Variables)
			self.References[var] = True
			if var in self.Variables:
				return self.Variables[var]
			else:
				if self.Parent:
					return self.Parent.getVar(var)
				elif var in builtins:
					return builtins[var]
				else:
					raise NameError(f"name '{var}' is not defined")
		def setVar(self, var, value):
			debugprint("Asked to set variable",var)
			if self.scopeType == "asclause":
				return self.Parent.setVar(var, value)
			if var in self.References and var not in self.Assignments:
				raise UnboundLocalError(f"local variable '{var}' referenced before assignment")
			self.Variables[var] = value
			self.Assignments[var] = True
		def setVarRaw(self, var, value): #Bypass scope-based checks
			debugprint("Asked to raw set variable",var)
			if var in self.References and var not in self.Assignments:
				raise UnboundLocalError(f"local variable '{var}' referenced before assignment")
			self.Variables[var] = value
			self.Assignments[var] = True
		def deleteVar(self, var):
			debugprint("Asked to delete variable",var)
			if self.scopeType == "asclause":
				self.Parent.deleteVar(var)
			if var in self.Variables:
				self.Variables.pop(var)
				self.Assignments[var] = False
				self.References[var] = False
				self.Globals[var] = False
			else:
				self.Parent.deleteVar(var)
		def triggerGlobal(self, var):
			if self.scopeType != "core":
				if var in self.References:
					raise SyntaxError(f"name '{var}' is used prior to global declaration")
				elif var in self.Assignments:
					raise SyntaxError(f"name '{var}' is assigned to before global declaration")
				raise ExecutorException("[!] Asked to trigger global, but this isnt implemented!")
				# if scope.Parent:
				# 	scope.Parent.triggerGlobal(var)
		def triggerNonlocal(self, var):
			raise ExecutorException("[!] Asked to trigger nonlocal, but this isnt implemented!")
		def clean(self):
			self.Variables = {}
			self.References = {}
			self.Assignments = {}
			self.Globals = {}

	class ClassScope(VariableScope):
		def __init__(self, Parent, Class):
			self.Parent = Parent
			self.Variables = {}
			self.scopeType = "class"
			self.Class = Class
		def getVar(self, var):
			return self.Parent.getVar(var) #We don't offer variables, since we dont store them like that
		def setVar(self, var, value):
			self.Variables[var] = value
			setattr(self.Class, var, value)
		def deleteVar(self, var):
			self.Variables.pop(var)
			delattr(self.Class, var)
		def triggerGlobal(self, var):
			raise ExecutorException("What?")
		def triggerNonlocal(self, var):
			raise ExecutorException("What?")
		def clean(self):
			for var in self.Variables:
				delattr(self.Class, var)
			self.Variables = {}

	class ReturnStatement:
		def __init__(self, Type, Data=None):
			self.Type = Type
			self.Data = Data

	class ExecutorException(Exception):
		pass

	def GoodGrammar(arg, tSingular, tPlural):
		if len(arg) == 1:
			return f"{tSingular} '{arg[0]}'"
		elif len(arg) == 2:
			return f"{tPlural} '{arg[0]}' and '{arg[1]}'"
		else:
			s = f"{tSingular} "
			for i in range(len(arg)-2):
				s = s + f"'{arg[i]}', "
			return f"{s}'{arg[len(arg)-2]}' and '{arg[len(arg)-1]}'"

	def ParseOperator(op):
		op = type(op)
		#Boolean operations (and/or) are not supported and are handled just in the BoolOp expr
		#UnaryOp
		if op == ast.Invert:
			return lambda x: ~x
		elif op == ast.Not:
			return lambda x: not x
		elif op == ast.UAdd:
			return lambda x: +x
		elif op == ast.USub:
			return lambda x: -x
		#BinaryOp
		elif op == ast.Add:
			return lambda x,y: x + y
		elif op == ast.Sub:
			return lambda x,y: x - y
		elif op == ast.Mult:
			return lambda x,y: x * y
		elif op == ast.MatMult:
			return lambda x,y: x @ y
		elif op == ast.Div:
			return lambda x,y: x / y
		elif op == ast.Mod:
			return lambda x,y: x % y
		elif op == ast.Pow:
			return lambda x,y: x ** y
		elif op == ast.LShift:
			return lambda x,y: x << y
		elif op == ast.RShift:
			return lambda x,y: x >> y
		elif op == ast.BitOr:
			return lambda x,y: x | y
		elif op == ast.BitXor:
			return lambda x,y: x ^ y
		elif op == ast.BitAnd:
			return lambda x,y: x & y
		elif op == ast.FloorDiv:
			return lambda x,y: x // y
		#Compare
		elif op == ast.Eq:
			return lambda x,y: x == y
		elif op == ast.NotEq:
			return lambda x,y: x != y
		elif op == ast.Lt:
			return lambda x,y: x < y
		elif op == ast.LtE:
			return lambda x,y: x <= y
		elif op == ast.Gt:
			return lambda x,y: x > y
		elif op == ast.GtE:
			return lambda x,y: x >= y
		elif op == ast.Is:
			return lambda x,y: x is y
		elif op == ast.IsNot:
			return lambda x,y: x is not y
		elif op == ast.In:
			return lambda x,y: x in y
		elif op == ast.NotIn:
			return lambda x,y: x not in y
		#None of the above
		else:
			raise ExecutorException(f"Unrecognised operator type '{op}'")

	_DEBUG_LastExpr = None
	_DEBUG_LastStatement = None

	def ExecuteExpression(expr, scope, *, ForcedContext=None):
		nonlocal _DEBUG_LastExpr
		_DEBUG_LastExpr = expr
		exprType = type(expr)
		debugprint("Executing expression...",exprType)

		if exprType == ast.Constant:
			return expr.value

		elif exprType == ast.Name:
			ctx = ForcedContext or type(expr.ctx)
			if ctx == ast.Load:
				return scope.getVar(expr.id)
			elif ctx == ast.Store:
				return expr.id
			elif ctx == ast.Del:
				return expr.id

		elif exprType == ast.NamedExpr:
			target, value = ExecuteExpression(expr.target, scope), ExecuteExpression(expr.value, scope)
			if type(target) == tuple or type(target) == list:
				raise SyntaxError(f"cannot use assignment expressions with {type(target)}")
			scope.setVar(target, value)
			return value

		elif exprType == ast.Starred:
			ctx = ForcedContext or type(expr.ctx)
			if ctx == ast.Load:
				return ExecuteExpression(expr.value, scope)
			elif ctx == ast.Store:
				return ExecuteExpression(expr.value, scope)
			elif ctx == ast.Del:
				raise ExecutorException("Direct call to evaluate a Starred expression")

		elif exprType == ast.Attribute:
			ctx = ForcedContext or type(expr.ctx)
			if ctx == ast.Load:
				return getattr(ExecuteExpression(expr.value, scope), expr.attr)
			elif ctx == ast.Store:
				raise ExecutorException("This shouldn't get called") #stmt.Assign shouldn't let a Store call creep into here. If it does, panic
			elif ctx == ast.Del:
				raise ExecutorException("This shouldn't get called") #ditto for stmt.Delete

		elif exprType == ast.JoinedStr:
			return str().join(ExecuteExpression(value, scope) for value in expr.values)

		elif exprType == ast.FormattedValue:
			value = ExecuteExpression(expr.value, scope)
			if expr.conversion == 115:
				value = str(value)
			elif expr.conversion == 114:
				value = repr(value)
			elif expr.conversion == 97:
				value = ascii(value)
			if expr.format_spec:
				value = format(value, ExecuteExpression(expr.format_spec, scope))
			else:
				value = format(value)
			return value

		elif exprType == ast.keyword:
			return expr.arg, ExecuteExpression(expr.value, scope)

		elif exprType == ast.Tuple:
			out = []
			for entry in expr.elts:
				if type(entry) == ast.Starred:
					out.extend(ExecuteExpression(entry, scope))
				else:
					out.append(ExecuteExpression(entry, scope))
			return tuple(out)

		elif exprType == ast.List:
			out = []
			for entry in expr.elts:
				if type(entry) == ast.Starred:
					out.extend(ExecuteExpression(entry, scope))
				else:
					out.append(ExecuteExpression(entry, scope))
			return out

		elif exprType == ast.Set:
			out = []
			for entry in expr.elts:
				if type(entry) == ast.Starred:
					out.extend(ExecuteExpression(entry, scope))
				else:
					out.append(ExecuteExpression(entry, scope))
			return set(out)

		elif exprType == ast.Dict:
			out = {}
			for i in range(len(expr.keys)):
				key, value = expr.keys[i], expr.values[i]
				if key == None: #value is a dict that needs unpacking
					for k,v in ExecuteExpression(value, scope).items():
						out[k] = v
				else:
					out[ExecuteExpression(key, scope)] = ExecuteExpression(value, scope)
			return out

		elif exprType == ast.ListComp:
			subScope = VariableScope(scope, "generator")
			out = ParseGenerators(expr.generators, [expr.elt], subScope)
			return [x[0] for x in out]

		elif exprType == ast.DictComp:
			subScope = VariableScope(scope, "generator")
			out = ParseGenerators(expr.generators, [expr.key, expr.value], subScope)
			return {x[0]: x[1] for x in out}

		elif exprType == ast.SetComp:
			subScope = VariableScope(scope, "generator")
			out = ParseGenerators(expr.generators, [expr.elt], subScope)
			return {x[0] for x in out}

		elif exprType == ast.GeneratorExp:
			subScope = VariableScope(scope, "generator")
			out = ParseGenerators(expr.generators, [expr.elt], subScope)
			return (x[0] for x in out)

		elif exprType == ast.Index: #Warning: Undocumented. Likely removed after py3.8
			return ExecuteExpression(expr.value, scope)

		elif exprType == ast.Slice:
			lower = expr.lower and ExecuteExpression(expr.lower, scope)
			upper = expr.upper and ExecuteExpression(expr.upper, scope)
			step = expr.step and ExecuteExpression(expr.step, scope)
			return slice(lower, upper, step)

		elif exprType == ast.Subscript:
			ctx = ForcedContext or type(expr.ctx)
			if ctx == ast.Load:
				value = ExecuteExpression(expr.value, scope)
				Slice = ExecuteExpression(expr.slice, scope)
				return value[Slice]
			elif ctx == ast.Store:
				raise ExecutorException("This shouldn't get called")
			elif ctx == ast.Del:
				raise ExecutorException("This shouldn't get called")

		elif exprType == ast.BoolOp:
			op = type(expr.op)
			if op == ast.And:
				for subExpr in expr.values:
					value = ExecuteExpression(subExpr, scope)
					if not value:
						return value
				return value
			elif op == ast.Or:
				for subExpr in expr.values:
					value = ExecuteExpression(subExpr, scope)
					if value:
						return value
				return value

		elif exprType == ast.UnaryOp:
			op = ParseOperator(expr.op)
			operand = ExecuteExpression(expr.operand, scope)
			return op(operand)

		elif exprType == ast.BinOp:
			Lhs = ExecuteExpression(expr.left, scope)
			op = ParseOperator(expr.op)
			Rhs = ExecuteExpression(expr.right, scope)
			return op(Lhs, Rhs)

		elif exprType == ast.Compare:
			subject = ExecuteExpression(expr.left, scope)
			for i in range(len(expr.ops)):
				op, comparison = ParseOperator(expr.ops[i]), ExecuteExpression(expr.comparators[i], scope)
				successState = op(subject, comparison)
				if successState == True:
					if i == len(expr.ops)-1:
						return True
					else:
						subject = comparison
				else:
					return False

		elif exprType == ast.IfExp: #This is in and of itself an IfExp
			return ExecuteExpression(expr.body, scope) if ExecuteExpression(expr.test, scope) else ExecuteExpression(expr.orelse, scope)

		elif exprType == ast.Call:
			func = ExecuteExpression(expr.func, scope)
			args = []
			for entry in expr.args:
				if type(entry) == ast.Starred:
					args.extend(ExecuteExpression(entry, scope))
				else:
					args.append(ExecuteExpression(entry, scope))
			kwargs = {}
			for entry in expr.keywords:
				name, value = ExecuteExpression(entry, scope)
				if name:
					kwargs[name] = value
				else:
					kwargs.update(value)

			return func(*args, **kwargs)

		elif exprType == ast.Lambda:
			def LambdaHandler(args, kwargs):
				subScope = VariableScope(scope, "lambda")
				HandleArgAssignment(subScope, expr, args, kwargs)
				return ExecuteExpression(expr.body, subScope)
			return lambda *args, **kwargs : LambdaHandler(args, kwargs)

		else:
			raise ExecutorException(f"[!] Unimplemented expression type {exprType}")


	def ExecuteStatement(statement, scope):
		nonlocal _DEBUG_LastStatement
		_DEBUG_LastStatement = statement
		stType = type(statement)
		debugprint("Executing statement...",stType)

		if stType == ast.Expr:
			ExecuteExpression(statement.value, scope)

		elif stType == ast.Delete:
			for target in statement.targets:
				if type(target) == ast.Attribute:
					delattr(ExecuteExpression(target.value, scope), target.attr)
				elif type(target) == ast.Subscript:
					del ExecuteExpression(target.value, scope)[ExecuteExpression(target.slice, scope)]
				else:
					scope.deleteVar(ExecuteExpression(target, scope))

		elif stType == ast.Assign:
			def Assign(target, value):
				if type(target) == ast.Name:
					scope.setVar(ExecuteExpression(target, scope), value)
				elif type(target) == ast.Attribute:
					setattr(ExecuteExpression(target.value, scope), target.attr, value)
				elif type(target) == ast.Subscript:
					ExecuteExpression(target.value, scope)[ExecuteExpression(target.slice, scope)] = value
				elif type(target) == ast.Tuple or type(target) == ast.List:
					if type(value) != tuple and type(value) != list:
						raise TypeError(f"cannot unpack non-iterable {type(value)} object")
					for i in range(len(target.elts)):
						item = target.elts[i]
						if type(item) == ast.Starred:
							offset = len(value)-len(target.elts)
							for lower in range(i):
								Assign(target.elts[lower], value[lower])
							scope.setVar(ExecuteExpression(item, scope), list(value[i:offset+i+1]))
							for upper in range(i+1,len(target.elts)):
								Assign(target.elts[upper], value[upper+offset])
							return
					if len(target.elts) < len(value):
						raise ValueError(f"not enough values to unpack (expected {len(target.elts)}, got {len(value)})")
					elif len(target.elts) > len(value):
						raise ValueError(f"too many values to unpack (expected {len(target.elts)})")
					else:
						for i in range(len(target.elts)):
							Assign(target.elts[i], value[i])
				elif type(target) == ast.Starred:
					raise SyntaxError("starred assignment target must be in a list or tuple")
				else:
					raise ExecutorException(f"Unable to assign to unrecognised type '{type(target)}'")
			value = ExecuteExpression(statement.value, scope)
			for target in statement.targets:
				Assign(target, value)

		elif stType == ast.AugAssign:
			value = ExecuteExpression(statement.value, scope)
			target = statement.target
			op = ParseOperator(statement.op)
			if type(target) == ast.Name:
				scope.setVar(ExecuteExpression(target, scope), op(ExecuteExpression(target, scope, ForcedContext=ast.Load), value))
			elif type(target) == ast.Attribute:
				setattr(ExecuteExpression(target.value, scope), target.attr, op(ExecuteExpression(target, scope, ForcedContext=ast.Load), value))
			elif type(target) == ast.Subscript:
				ExecuteExpression(target.value, scope)[ExecuteExpression(target.slice, scope)] = op(ExecuteExpression(target.value, scope)[ExecuteExpression(target.slice, scope)], value)
			else:
				raise ExecutorException(f"Unable to assign to unrecognised type '{type(target)}'")

		elif stType == ast.Assert:
			if not ExecuteExpression(statement.test, scope):
				raise AssertionError(ExecuteExpression(statement.msg, scope))

		elif stType == ast.Raise:
			if statement.exc:
				if statement.cause:
					raise ExecuteExpression(statement.exc, scope) from ExecuteExpression(statement.cause, scope)
				raise ExecuteExpression(statement.exc, scope)
			raise

		elif stType == ast.Global:
			for entry in statement.names:
				scope.triggerGlobal(entry)

		elif stType == ast.Nonlocal:
			for entry in statement.names:
				scope.triggerNonlocal(entry)

		elif stType == ast.Return:
			if statement.value:
				return ReturnStatement("Return", ExecuteExpression(statement.value, scope))
			else:
				return ReturnStatement("Return")

		elif stType == ast.Pass:
			pass #Do literally nothing

		elif stType == ast.Break:
			return ReturnStatement("Break")

		elif stType == ast.Continue:
			return ReturnStatement("Continue")

		elif stType == ast.If:
			if ExecuteExpression(statement.test, scope):
				out = ExecuteStatList(statement.body, scope)
				if out != None:
					return out
			else:
				out = ExecuteStatList(statement.orelse, scope)
				if out != None:
					return out

		elif stType == ast.While:
			while ExecuteExpression(statement.test, scope):
				out = ExecuteStatList(statement.body, scope)
				if out != None:
					if out.Type == "Break":
						break
					elif out.Type == "Continue":
						continue
					elif out.Type == "Return":
						return out
			else:
				out = ExecuteStatList(statement.orelse, scope)
				if out != None:
					return out

		elif stType == ast.For:
			target = ExecuteExpression(statement.target, scope)
			iterRange = ExecuteExpression(statement.iter, scope)
			for value in iterRange:
				scope.setVar(target, value)
				out = ExecuteStatList(statement.body, scope)
				if out != None:
					if out.Type == "Break":
						break
					elif out.Type == "Continue":
						continue
					elif out.Type == "Return":
						return out
			else:
				out = ExecuteStatList(statement.orelse, scope)
				if out != None:
					return out

		elif stType == ast.With:
			toExit = []
			for item in statement.items:
				out = ExecuteExpression(item.context_expr, scope)
				out.__enter__()
				toExit.append(out)
				if item.optional_vars:
					storeAs = ExecuteExpression(item.optional_vars, scope)
					#If this isnt a name expr, then uh, good luck!
					scope.setVar(storeAs, out)
			try:
				out = ExecuteStatList(statement.body, scope)
			except BaseException as exc:
				for item in toExit:
					item.__exit__()
				raise exc
			else:
				for item in toExit:
					item.__exit__()
				return out

		elif stType == ast.Try:
			try:
				out = ExecuteStatList(statement.body, scope)
				if out != None:
					return out
			except ExecutorException as exc: #Executor errors are not to reach the source code ever
				raise exc
			except BaseException as exc:
				debugprint("We had a try call fail",exc)
				for handler in statement.handlers:
					if handler.type == None or isinstance(exc, ExecuteExpression(handler.type, scope)):
						subScope = VariableScope(scope, "asclause")
						if handler.name:
							subScope.setVarRaw(handler.name, exc)
						out = ExecuteStatList(handler.body, subScope)
						if out != None:
							return out
						break
			else:
				out = ExecuteStatList(statement.orelse, scope)
				if out != None:
					return out
			finally:
				out = ExecuteStatList(statement.finalbody, scope)
				if out != None:
					return out


		elif stType == ast.FunctionDef:
			def FunctionHandler(*args, **kwargs):
				subScope = VariableScope(scope, "function")
				HandleArgAssignment(subScope, statement, args, kwargs)
				out = ExecuteStatList(statement.body, subScope)
				if out != None:
					if out.Type == "Break" or out.Type == "Continue":
						raise SyntaxError(f"'{out.Type}' outside loop")
					else:
						return out.Data
			FunctionHandler.__name__ = statement.name
			FunctionHandler.__qualname__ = statement.name #Technically a bit wrong but eh
			FunctionHandler = ImplementObjectDecorators(FunctionHandler, statement.decorator_list, scope)
			scope.setVar(statement.name, FunctionHandler)

		elif stType == ast.ClassDef:
			bases = tuple([ExecuteExpression(entry, scope) for entry in statement.bases])
			keywords = {}
			for entry in statement.keywords:
				keywords[entry.arg] = ExecuteExpression(entry.value)
			class DummyClass(*bases, **keywords): #This is legal, wow. Thanks python!
				pass
			DummyClass.__name__ = statement.name
			DummyClass.__qualname__ = statement.name
			subScope = ClassScope(scope, DummyClass) #Custom class subscope
			out = ExecuteStatList(statement.body, subScope) #We shouldn't end early, period
			if out != None:
				raise SyntaxError(f"Now that is just illegal class logic, I don't even know what to say anymore")
			DummyClass = ImplementObjectDecorators(DummyClass, statement.decorator_list, scope)
			scope.setVar(statement.name, DummyClass)

		else:
			raise ExecutorException(f"[!] Unimplemented statement type {stType}")

	def ExecuteStatList(statList, scope):
		for statement in statList:
			out = ExecuteStatement(statement, scope)
			if out != None: #Send off our return/break/continue statement
				return out

	#def f2(x, y, z=None, *, a, b, c=None, **k):
	#	print('Cool')
	def HandleArgAssignment(scope, obj, args, kwargs):
		"""
		General handler for assigning arguments into an executable body
		This gets messy incredibly fast
		Note: When handling kwarg defaults, its given as a list like [None, None, Constant()],
		but for the posargs, its just a list with no 'None's. Turns out that once a single positional arg is optional,
		all the posargs after that have to be optional too, which explains the weird behaviour.
		"""

		#Setup
		astArgs = obj.args
		representation = type(obj) == ast.Lambda and "<lambda>" or obj.name
		assignedNames = {}
		wantedPositionals = {}
		for pa in astArgs.args:
			wantedPositionals[pa.arg] = True
		wantedKeywords = {}
		for kwa in astArgs.kwonlyargs:
			wantedKeywords[kwa.arg] = True

		posargCollector = []
		kwargCollector = {}

		#Positional defaults
		defaultOffset = len(astArgs.args)-len(astArgs.defaults)
		for i in range(len(astArgs.defaults)):
			scope.setVar(astArgs.args[i+defaultOffset].arg, ExecuteExpression(astArgs.defaults[i], scope.Parent))
			wantedPositionals[astArgs.args[i+defaultOffset].arg] = False

		#Input positionals
		for i in range(len(args)):
			if i < len(astArgs.args):
				scope.setVar(astArgs.args[i].arg, args[i])
				assignedNames[astArgs.args[i].arg] = True
				wantedPositionals[astArgs.args[i].arg] = False
			else:
				posargCollector.append(args[i])

		#kwarg defaults
		for i in range(len(astArgs.kw_defaults)):
			default = astArgs.kw_defaults[i]
			if default != None:
				kw = astArgs.kwonlyargs[i]
				scope.setVar(kw.arg, ExecuteExpression(default, scope.Parent))
				wantedKeywords[kw.arg] = False

		#Input kwargs
		for key, value in kwargs.items():
			if key in assignedNames:
				raise TypeError(f"{representation}() got multiple values for argument '{key}'")
			if key in wantedPositionals:
				scope.setVar(key, value)
				assignedNames[key] = True
				wantedPositionals[key] = False
			elif key in wantedKeywords:
				scope.setVar(key, value)
				assignedNames[key] = True
				wantedKeywords[key] = False
			else:
				kwargCollector[key] = value

		#Final processing and error check
		missing = []
		for key, wanted in wantedPositionals.items():
			if wanted == True:
				missing.append(key)
		if len(missing) > 0:
			raise TypeError(f"{representation}() missing {len(missing)} required positional {GoodGrammar(missing, 'argument:', 'arguments:')}")
		missing = []
		for key, wanted in wantedKeywords.items():
			if wanted == True:
				missing.append(key)
		if len(missing) > 0:
			raise TypeError(f"{representation}() missing {len(missing)} required keyword-only {GoodGrammar(missing, 'argument:', 'arguments:')}")
		if astArgs.vararg:
			scope.setVar(astArgs.vararg.arg, posargCollector)
		elif len(posargCollector) > 0:
			raise TypeError(f"{representation}() received too many positional arguments")
		if astArgs.kwarg:
			scope.setVar(astArgs.kwarg.arg, kwargCollector)
		elif len(kwargCollector) > 0:
			raise TypeError(f"{representation}() received too many keyword arguments")

	def ImplementObjectDecorators(obj, decorators, scope):
		for i in range(len(decorators)-1, -1, -1): #Traverse in reverse order
			decorator = ExecuteExpression(decorators[i], scope)
			obj = decorator(obj)
		return obj

	#x = ["A", "DD", "B", "CCBC"]
	#print([S+str(ord(C)) for S in x if S != "A" for C in S if C != "B"])
	def ParseGenerators(generators, toEvaluate, scope):
		"""
		General generator handler, handling nested for and if statements
		This should always be passed a subscope to avoid complications
		"""
		def RecursiveHandle(generators, i):
			gen = generators[i]
			iterator = ExecuteExpression(gen.iter, scope)
			storage = ExecuteExpression(gen.target, scope)
			combinations = []
			for term in iterator:
				scope.setVar(storage, term)
				ShouldEvaluate = True
				for condition in gen.ifs:
					if not ExecuteExpression(condition, scope):
						ShouldEvaluate = False
						break
				if ShouldEvaluate:
					if i == len(generators)-1: #Last generator
						for term in toEvaluate:
							combinations.append([ExecuteExpression(out, scope) for out in toEvaluate])
					else:
						combinations.extend(RecursiveHandle(generators, i+1))
			return combinations
		return RecursiveHandle(generators, 0)

	#At this point we'd parse the AST if it was obfuscated. Obviously, here in our little testing place, it isn't
	finalCode = code
	def __main__():
		scope = VariableScope(None, "core")
		debugprint("Input code:",code)
		if _DEBUG:
			beforeRun = ast.dump(finalCode)
		try:
			out = ExecuteStatList(finalCode.body, scope)
		except BaseException as exc:
			if _DEBUG:
				afterRun = ast.dump(finalCode)
				if beforeRun != afterRun:
					debugprint("[!] The AST has been modified during execution. New AST:",afterRun)
				debugprint("[!] We ran into a critical error")
				if _DEBUG_LastExpr:
					debugprint("Last expression:",ast.dump(_DEBUG_LastExpr))
				else:
					debugprint("Last expression: None")
				if _DEBUG_LastStatement:
					debugprint("Last statement:",ast.dump(_DEBUG_LastStatement))
				else:
					debugprint("Last statement: None")
			raise exc
		else:
			if _DEBUG:
				afterRun = ast.dump(finalCode)
				if beforeRun != afterRun:
					debugprint("[!] The AST has been modified during execution. New AST:",afterRun)
			if out:
				if out.Type == "Break" or out.Type == "Continue":
					raise SyntaxError(f"'{out.Type}' outside loop")
				else:
					raise SyntaxError(f"'{out.Type}' outside function")

	return __main__


testing = ast.parse("""print("Hey!")
print(False)
print("What?", end="ASD\\n")
print((lambda x,y : y/x)(5,6))
x,y,z = 5,6,7
print(x**2)
def f(arg, arg2):
	print(arg2, arg)
	return arg2*arg, arg/arg2

def f2(x, y, z=None, *, a, b, c=None, **k):
	print(x,y,z,"split",a,b,c,"split",k)

f2(1, 2, z=True, a=5, b=6, p=8, c=7)

print("out=", f(2, 3))

class Test:
	def __init__(self, v):
		self.y = v
	def gety(self):
		return self.y

print("Test=",Test)
TestObj = Test(8)
print("TestObj=",TestObj)
print("TO.gety()=",TestObj.gety())
TestObj.y += 15
print("TO.gety()=",TestObj.gety())

x = {"A":5, 6:True}
y = {**x, 8:True}
z = {**y, **x, "A":1}
print(x,y,z)

x = ["A", "DD", "B", "CCBC"]

print("ListComp")
obj = [S+str(ord(C)) for S in x if S != "A" for C in S if C != "B"]
print(type(obj), obj)

print("SetComp")
obj = {S+str(ord(C)) for S in x if S != "A" for C in S if C != "B"}
print(type(obj), obj)

print("DictComp")
obj = {S+str(ord(C)): S for S in x if S != "A" for C in S if C != "B"}
print(type(obj), obj)

print("Generator")
gen = (S+str(ord(C)) for S in x if S != "A" for C in S if C != "B")
print(type(gen), gen)
for v in gen:
	print("Gen object entry",v)

def d1(obj):
	print("Hooking obj in D1...")
	def ret():
		print("D1 hook on",obj)
		return obj()
	return ret
def d2(obj):
	print("Hooking obj in D2...")
	def ret():
		print("D2 hook on",obj)
		return obj()
	return ret

print("Decorators test 1")
@d1
@d2
def test():
	print("This is test")
	return True
print("out=",test())

print("Test part 2")
@d1
@d2
class test2:
	print("Executing body of test")
print("Running test")
print("out=",test2())

print("Decorators test done")


print("IfExp1", 1 if True else 2 if True else 3 if True else 4)
print("IfExp2", 1 if True else 2 if False else 3 if True else 4)
print("IfExp3", (1 if True else 2) if False else (3 if True else 4))

# try:
# 	with open("with.txt","w") as f:
# 		print("Closed?",f.closed)
# 		print("file",f)
# 		f.write("Test text")
# 		f.dfsajasfjh()
# except:
# 	print("Ignoring intentional fail")
# print("Closed?",f.closed)

x = [2,3,4]
y = {2:3, 4:5}
y2 = {"end":"A\\n"}
print(1,[x],5)
print(1,*[x],5)
print(1, y, 6)
print(1, *y, 6)
print(1, 2, y2)
print(1, 2, *y2)
print(1, 2, **y2)

(n,*y,n) = 1,2,3
print(n,y)
a,*y,b,c = 1,2,3,4,5
print(a,y,b,c)
a,b,*y,c = 1,2,3,4,5
print(a,b,y,c)

x = [5, True]
y = [*x, 8]
z = [*y, *x, "A", 1]
print("x", x, "y", y, "z", z)
print(f"A{x*3}B{y}C{z*2}")
b = 5.4321
print(f"{b:2.3}")
""")

debugprint("AST Dump:",ast.dump(testing))

debugprint("Generating execution loop")
out = CreateExecutionLoop(testing)
debugprint("Executing execution loop")
out()
debugprint("Finished execution loop")
