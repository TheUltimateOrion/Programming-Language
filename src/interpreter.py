########################################
# RUNTIME RESULT
########################################

import math
import os
from pathlib import Path
from errors import RTError
from lexer import KEYWORDS, TT_CONCAT, TT_DIV, TT_EE, TT_GT, TT_GTE, TT_KEYWORD, TT_LT, TT_LTE, TT_MINUS, TT_MOD, TT_MUL, TT_NE, TT_PLUS, TT_POW, TT_BW_OR, Lexer
from parser import Parser
from runtime import RTResult
from token import TT_BW_AND, TT_BW_ANDE, TT_BW_LSHIFT, TT_BW_LSHIFTE, TT_BW_NOT, TT_BW_ORE, TT_BW_RSHIFT, TT_BW_RSHIFTE, TT_BW_XOR, TT_BW_XORE, TT_DECR, TT_DIVE, TT_INCR, TT_MINUSE, TT_MODE, TT_MULE, TT_PLUSE, TT_POWE

########################################
# VALUES
########################################

class Value:
    __class__ = None

    def __init__(self):
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        return None, self.illegal_operation(other)

    def subbed_by(self, other):
        return None, self.illegal_operation(other)

    def multed_by(self, other):
        return None, self.illegal_operation(other)

    def dived_by(self, other):
        return None, self.illegal_operation(other)

    def modded_by(self, other):
        return None, self.illegal_operation(other)

    def powed_by(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)

    def anded_by(self, other):
        return None, self.illegal_operation(other)

    def ored_by(self, other):
        return None, self.illegal_operation(other)

    def concat(self, other):
        return None, self.illegal_operation(other)
    
    def is_in(self, other):
        return None, self.illegal_operation(other)

    def notted(self):
        return None, self.illegal_operation()

    def bw_anded_by(self, other):
        return None, self.illegal_operation(other)

    def bw_xored_by(self, other):
        return None, self.illegal_operation(other)

    def bw_ored_by(self, other):
        return None, self.illegal_operation(other)

    def bw_rshift(self, other):
        return None, self.illegal_operation(other)

    def bw_lshift(self, other):
        return None, self.illegal_operation(other)

    def bw_notted(self):
        return None, self.illegal_operation()
         
    def execute(self):
        return RTResult().failure(self.illegal_operation())

    def copy(self):
        raise Exception('No copy method defined')

    def is_true(self):
        return False

    def illegal_operation(self, other=None):
        if not other: other = self
        return RTError(
            self.pos_start, other.pos_end,
            'Illegal operation',
            self.context
        )

class Number(Value):
    __class__ = "<type 'Number'>"

    def __init__(self, value, overwritable=True):
        super().__init__()
        self.overwritable = overwritable
        self.value = value

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )

            return Number(self.value / other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def modded_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )

            return Number(self.value % other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def powed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def concat(self, other):
        if isinstance(other, Number | String):
            return Number(str(self.value) + str(other.value)), None
        else:
            return None, Value.illegal_operation(self, other)

    def is_in(self, other):
        if isinstance(other, List):
            for x in other.elements:
                if isinstance(x, List):
                    if self.is_in(x)[0].value == 1:
                        return Number(1).set_context(self.context), None
                else:
                    if self.value == x.value:
                        return Number(1).set_context(self.context), None
            
            return Number(int(0)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None

    def bw_anded_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value & other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def bw_ored_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value | other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def bw_xored_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value & other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def bw_notted(self):
        return Number(~self.value).set_context(self.context), None

    def bw_rshift(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >> other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def bw_lshift(self, other):
        if isinstance(other, Number):
            return Number(int(self.value << other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.value != 0

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

class String(Value):
    __class__ = "<type 'String'>"

    def __init__(self, value, overwritable=True):
        super().__init__()
        
        self.overwritable = overwritable
        self.value = value

    def added_to(self, other):
        if isinstance(other, String | Number):
            if isinstance(other, Number):
                value = str(other.value)
            else:
                value = other.value
            return String(self.value + value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def concat(self, other):
        return self.added_to(other)

    def is_in(self, other):
        if isinstance(other, List | String):
            if isinstance(other, List):
                for x in other.elements:
                    if isinstance(x, List):
                        if self.is_in(x)[0].value == 1:
                            return Number(1).set_context(self.context), None
                    else:
                        if self.value == x.value:
                            return Number(1).set_context(self.context), None
            
            elif isinstance(other, String):
                for x in other.value:
                    if self.value == x:
                        return Number(1).set_context(self.context), None
            
            return Number(int(0)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def is_true(self):
        return len(self.value) > 0

    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return self.value

    def __repr__(self):
        return f'\'{self.value}\''

class List(Value):
    __class__ = "<type 'List'>"

    def __init__(self, elements, overwritable=True):
        super().__init__()
        
        self.overwritable = overwritable
        self.elements = elements

    def subbed_by(self, other):
        if isinstance(other, Number):
            new_list = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            except:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Element at this index could not be removed from list because index is out of bounds',
                    self.context
                )
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, Number):
            new_list = self.copy()
            for val in new_list.elements:
                val.value = val.value * other.value
            return new_list, None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_eq(self, other):
        if isinstance(other, List):
            if len(self.elements) == len(other.elements):
                for i in range(len(self.elements)):
                    if isinstance(self.elements[i], Number | String):
                        if self.elements[i].value != other.elements[i].value:
                            return Number(0).set_context(self.context), None
                    elif isinstance(self.elements[i], List):
                        if self.elements[i].get_comparison_eq(other.elements[i])[0].value != 1:
                            return Number(0).set_context(self.context), None
                return Number(1).set_context(self.context), None
            else:
                return Number(0).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def concat(self, other):
        if isinstance(other, List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
        else:
            return None, Value.illegal_operation(self, other)

    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return ", ".join([str(x) for x in self.elements])

    def __repr__(self):
        return f'[{", ".join([repr(x) for x in self.elements])}]'

List.KEYWORDS = List(KEYWORDS, False)

class Dict(Value):
    __class__ = "<type 'Dict'>"

    def __init__(self, elements, keys, values, overwritable=True):
        super().__init__()
        
        self.overwritable = overwritable
        self.elements = elements
        self.keys = keys
        self.values = values

    def copy(self):
        copy = Dict(self.elements, self.keys, self.values)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def get_vals(self):
        keys = self.keys
        values = self.values
        val = '{'
        
        for x in range(len(keys)):
            val += f"'{keys[x]}': {values[x]}"
            if x != len(keys) - 1:
                val += ", "
        val += '}'
        return val

    def __str__(self):
        return self.get_vals()

    def __repr__(self):
        return self.get_vals()

class BaseFunction(Value):
    __class__ = "<type 'Function'>"

    def __init__(self, name):
        super().__init__()
        self.name = name or "<anonymous>"

    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context

    def check_args(self, arg_names, args):
        res = RTResult()

        if len(args) > len(arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(args) - len(arg_names)} too many args passed into {self}",
                self.context
            ))

        if len(args) < len(arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(arg_names) - len(args)} too few args passed into {self}",
                self.context
            ))

        return res.success(None)

    def populate_args(self, arg_names, args, exec_ctx):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name, arg_value)

    def check_and_populate_args(self, arg_names, args, exec_ctx):
        res = RTResult()
        res.register(self.check_args(arg_names, args))
        if res.should_return(): return res
        self.populate_args(arg_names, args, exec_ctx)
        return res.success(None)

class Function(BaseFunction):
    def __init__(self, name, body_node, arg_names, should_auto_return):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names
        self.should_auto_return = should_auto_return

    def execute(self, args):
        res = RTResult()
        interpreter = Interpreter()
        exec_ctx = self.generate_new_context()

        res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
        if res.should_return(): return res

        value = res.register(interpreter.visit(self.body_node, exec_ctx))
        if res.should_return() and res.func_return_value == None: return res
        
        ret_value = (value if self.should_auto_return else None) or res.func_return_value or Number.null
        return res.success(ret_value)

    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names, self.should_auto_return)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<function {self.name}>"

class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, args):
        res = RTResult()
        exec_ctx = self.generate_new_context()

        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method)

        res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
        if res.should_return(): return res

        return_value = res.register(method(exec_ctx))
        if res.should_return(): return res
        return res.success(return_value)

    def no_visit_method(self, node, context):
        raise Exception(f'No execute_{self.name} method defined')

    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<built-in function {self.name}>"

########################################

    def execute_print(self, exec_ctx):
        print(str(exec_ctx.symbol_table.get('value')))
        return RTResult().success(Number.null)
    execute_print.arg_names = ['value']

    def execute_print_ret(self, exec_ctx):
        return RTResult().success(String(str(exec_ctx.symbol_table.get('value'))))
    execute_print_ret.arg_names = ['value']

    def execute_input(self, exec_ctx):
        text = input()
        return RTResult().success(String(text))
    execute_input.arg_names = []

    def execute_input_int(self, exec_ctx):
        while True:
            text = input()
            try:
                number = int(text)
                break
            except ValueError:
                print(f"'{text}' must be an integer. Try again!")
        return RTResult().success(Number(number))
    execute_input_int.arg_names = []

    def execute_clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        return RTResult().success(Number.null)
    execute_clear.arg_names = []

    def execute_is_number(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), Number)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_is_number.arg_names = ['value']

    def execute_is_string(self, exec_ctx):
        is_string = isinstance(exec_ctx.symbol_table.get("value"), String)
        return RTResult().success(Number.true if is_string else Number.false)
    execute_is_string.arg_names = ['value']

    def execute_is_list(self, exec_ctx):
        is_list = isinstance(exec_ctx.symbol_table.get("value"), List)
        return RTResult().success(Number.true if is_list else Number.false)
    execute_is_list.arg_names = ['value']

    def execute_is_function(self, exec_ctx):
        is_function = isinstance(exec_ctx.symbol_table.get("value"), BaseFunction)
        return RTResult().success(Number.true if is_function else Number.false)
    execute_is_function.arg_names = ['value']

    def execute_append(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        value = exec_ctx.symbol_table.get("value")

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
            ))

        list_.elements.append(value)
        return RTResult().success(Number.null)
    execute_append.arg_names = ['list', 'value']

    def execute_pop(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        index = exec_ctx.symbol_table.get("index")

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
            ))

        if not isinstance(index, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be number",
                exec_ctx
            ))

        try:
            element = list_.elements.pop(index.value)
        except:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                 'Element at this index could not be removed from list because index is out of bounds',
                exec_ctx
            ))
        return RTResult().success(element)
    execute_pop.arg_names = ['list', 'index']

    def execute_extend(self, exec_ctx):
        listA = exec_ctx.symbol_table.get("listA")
        listB = exec_ctx.symbol_table.get("listB")

        if not isinstance(listA, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
            ))

        if not isinstance(listB, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be list",
                exec_ctx
            ))
        
        listA.elements.extend(listB.elements)
        return RTResult().success(Number.null)
    execute_extend.arg_names = ['listA', 'listB']

    def execute_len(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get('list')
        
        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be list",
                exec_ctx
            ))

        return RTResult().success(Number(len(list_.elements)))
    execute_len.arg_names = ['list']

    def execute_run(self, exec_ctx):
        fn = exec_ctx.symbol_table.get('fn')

        if not isinstance(fn, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be string",
                exec_ctx
            ))

        fn = fn.value

        try:
            with open(fn, "r") as f:
                script = f.read()
        except Exception as e:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Failed to load script \"{fn}\"\n" + str(e),
                exec_ctx
            ))

        _, error = run(fn, script)

        if error:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Failed to finish executing script \"{fn}\"\n" +
                error.as_string(),
                exec_ctx
            ))

        return RTResult().success(Number.null)
    execute_run.arg_names = ['fn']

    def execute_abs(self, exec_ctx):
        number = exec_ctx.symbol_table.get('value')

        if not isinstance(number, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be Number",
                exec_ctx
            ))

        return RTResult().success(Number(number.value * -1) if number.value < 0 else number)
    execute_abs.arg_names = ['value']

    def execute_typeof(self, exec_ctx):
        value = exec_ctx.symbol_table.get('value')

        if not isinstance(value, Value):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a Value",
                exec_ctx
            ))


        return RTResult().success(String(value.__class__))
    execute_typeof.arg_names = ['value']

BuiltInFunction.print       = BuiltInFunction("print")
BuiltInFunction.print_ret   = BuiltInFunction("print_ret")
BuiltInFunction.input       = BuiltInFunction("input")
BuiltInFunction.input_int   = BuiltInFunction("input_int")
BuiltInFunction.clear       = BuiltInFunction("clear")
BuiltInFunction.is_number   = BuiltInFunction("is_number")
BuiltInFunction.is_string   = BuiltInFunction("is_string")
BuiltInFunction.is_list     = BuiltInFunction("is_list")
BuiltInFunction.is_function = BuiltInFunction("is_function")
BuiltInFunction.append      = BuiltInFunction("append")
BuiltInFunction.pop         = BuiltInFunction("pop")
BuiltInFunction.extend      = BuiltInFunction("extend")
BuiltInFunction.len         = BuiltInFunction("len")
BuiltInFunction.run         = BuiltInFunction("run")
BuiltInFunction.abs         = BuiltInFunction("abs")
BuiltInFunction.typeof      = BuiltInFunction("typeof")
    
Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)
Number.math_PI = Number(math.pi, False)
Number.math_POS_INF = Number(float("inf"), False)
Number.math_NEG_INF = Number(-1 * float("inf"), False)

class Import:
    def __init__(self, import_name):
        self.import_name = import_name
        self.set_context()
        self.set_pos()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def import_module(self):
        fn = self.import_name

        if not isinstance(fn, String):
            return None, RTError(
                self.pos_start, self.pos_end,
                "Argument must be string",
                self.context
            )

        fn = fn.value + ".my"

        if not Path(fn).exists():
            return None, RTError(
                    self.import_name.pos_start, self.import_name.pos_end,
                    f"Module does not exist \"{fn}\"\n",
                    self.context
                )

        f = open(fn)

        module = f.read()

        _, error = run(fn, module)

        if error:
            return None, RTError(
                self.import_name.pos_start, self.import_name.pos_end,
                f"Failed to finish importing script \"{fn}\"\n" +
                error.as_string(),
                self.context
            )

        return RTResult().success(Number.null), None

    def __repr__(self):
        return str(self.import_name)

########################################
# CONTEXT
########################################

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None

########################################
# SYMBOL TABLE
########################################

class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]

########################################
# INTERPRETER
########################################

class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

########################################

    def visit_NumberNode(self, node, context):
        return RTResult().success(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_StringNode(self, node, context):
        return RTResult().success(
            String(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_ListNode(self, node, context):
        res = RTResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.should_return(): return res

        return res.success(
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_DictNode(self, node, context):
        res = RTResult()
        elements = {}
        keys = []
        values = []

        for element_node in node.element_nodes:
            elements.update({res.register(self.visit(element_node, context)) : res.register(self.visit(node.element_nodes[element_node], context))})
            keys.append(res.register(self.visit(element_node, context)))
            if res.should_return(): return res
            values.append(res.register(self.visit(node.element_nodes[element_node], context)))
            if res.should_return(): return res

        return res.success(
            Dict(elements, keys,values).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_VarAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"'{var_name}' is not defined",
                context
            ))
        
        value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.should_return(): return res

        if node.constant and not isinstance(value, BaseFunction):
            value.overwritable = False

        if isinstance(context.symbol_table.get(var_name), BuiltInFunction):
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"Cannot redeclare a built-in function: {var_name}",
                context
            ))

        if context.symbol_table.get(var_name):
            if context.symbol_table.get(var_name).overwritable == False:
                return res.failure(RTError(
                    node.pos_start, node.pos_end,
                    f"Cannot redeclare a constant variable: {var_name}",
                    context
                ))

        if node.reassign:
            prev_val = context.symbol_table.get(var_name)

            if not prev_val:
                return res.failure(RTError(
                    node.pos_start, node.pos_end,
                    f"'{var_name}' is not defined",
                    context
                ))

            if node.op_tok.type == TT_PLUSE:
                if isinstance(prev_val, String | Number):
                    value = Number(prev_val.value + value.value) if isinstance(prev_val, Number) else String(prev_val.value + str(value.value))
                else:
                    return res.failure(RTError(
                        node.pos_start, node.pos_end,
                        f"Invalid variable type",
                        context
                    ))
            
            if node.op_tok.type == TT_MINUSE:
                if isinstance(prev_val, Number):
                    value = Number(prev_val.value - value.value)
                else:
                    return res.failure(RTError(
                        node.pos_start, node.pos_end,
                        f"Invalid variable type",
                        context
                    ))
            
            if node.op_tok.type == TT_MULE:
                if isinstance(prev_val, String | Number):
                    value = Number(prev_val.value * value.value) if isinstance(prev_val, Number) else String(prev_val.value * value.value)
                else:
                    return res.failure(RTError(
                        node.pos_start, node.pos_end,
                        f"Invalid variable type",
                        context
                    ))

            if node.op_tok.type == TT_POWE:
                if isinstance(prev_val, Number):
                    value = Number(prev_val.value ** value.value) if isinstance(prev_val, Number) else String(prev_val.value * value.value)
                else:
                    return res.failure(RTError(
                        node.pos_start, node.pos_end,
                        f"Invalid variable type",
                        context
                    ))
            
            if node.op_tok.type == TT_BW_ANDE:
                if isinstance(prev_val, Number):
                    value = Number(prev_val.value & value.value)
                else:
                    return res.failure(RTError(
                        node.pos_start, node.pos_end,
                        f"Invalid variable type",
                        context
                    ))

            if node.op_tok.type == TT_BW_ORE:
                if isinstance(prev_val, Number):
                    value = Number(prev_val.value | value.value)
                else:
                    return res.failure(RTError(
                        node.pos_start, node.pos_end,
                        f"Invalid variable type",
                        context
                    ))

            if node.op_tok.type == TT_BW_XORE:
                if isinstance(prev_val, Number):
                    value = Number(prev_val.value ^ value.value)
                else:
                    return res.failure(RTError(
                        node.pos_start, node.pos_end,
                        f"Invalid variable type",
                        context
                    ))

            if node.op_tok.type == TT_BW_LSHIFTE:
                if isinstance(prev_val, Number):
                    value = Number(prev_val.value << value.value)
                else:
                    return res.failure(RTError(
                        node.pos_start, node.pos_end,
                        f"Invalid variable type",
                        context
                    ))

            if node.op_tok.type == TT_BW_RSHIFTE:
                if isinstance(prev_val, Number):
                    value = Number(prev_val.value >> value.value)
                else:
                    return res.failure(RTError(
                        node.pos_start, node.pos_end,
                        f"Invalid variable type",
                        context
                    ))

            else:
                if value.value == 0:
                    return res.failure(RTError(
                        value.pos_start, value.pos_end,
                        'Division by zero',
                        context
                    ))

                if node.op_tok.type == TT_DIVE:
                    if isinstance(prev_val, Number):
                        value = Number(prev_val.value / value.value)
                    else:
                        return res.failure(RTError(
                            node.pos_start, node.pos_end,
                            f"Invalid variable type",
                            context
                        ))

                if node.op_tok.type == TT_MODE:
                    if isinstance(prev_val, Number):
                        value = value.modded_by(prev_val)
                    else:
                        return res.failure(RTError(
                            node.pos_start, node.pos_end,
                            f"Invalid variable type",
                            context
                        ))
                
        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.should_return(): return res
        right = res.register(self.visit(node.right_node, context))
        if res.should_return(): return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == TT_MOD:
            result, error = left.modded_by(right)
        elif node.op_tok.type == TT_POW:
            result, error = left.powed_by(right)
        elif node.op_tok.type == TT_CONCAT:
            result, error = left.concat(right)
        elif node.op_tok.type == TT_EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.type == TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.matches(TT_KEYWORD, 'and'):
            result, error = left.anded_by(right)
        elif node.op_tok.matches(TT_KEYWORD, 'or'):
            result, error = left.ored_by(right)
        elif node.op_tok.matches(TT_KEYWORD, 'in'):
            result, error = left.is_in(right)
        elif node.op_tok.type == TT_BW_AND:
            result, error = left.bw_anded_by(right)
        elif node.op_tok.type == TT_BW_XOR:
            result, error = left.bw_xored_by(right)
        elif node.op_tok.type == TT_BW_OR:
            result, error = left.bw_ored_by(right)
        elif node.op_tok.type == TT_BW_RSHIFT:
            result, error = left.bw_rshift(right)
        elif node.op_tok.type == TT_BW_LSHIFT:
            result, error = left.bw_lshift(right)
        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.should_return(): return res

        error = None

        if node.op_tok.type == TT_MINUS:
            number, error = number.multed_by(Number(-1))
        elif node.op_tok.type == TT_INCR:
            number, error = number.added_to(Number(1))
        elif node.op_tok.type == TT_DECR:
            number, error = number.subbed_by(Number(1))
        elif node.op_tok.type == TT_BW_NOT:
            number, error = number.bw_notted()
        elif node.op_tok.matches(TT_KEYWORD, 'not'):
            number, error = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))

    def visit_IfNode(self, node, context):
        res = RTResult()

        for condition, expr, should_return_null in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.should_return(): return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.should_return(): return res
                return res.success(Number.null if should_return_null else expr_value)

        if node.else_case:
            expr, should_return_null = node.else_case
            expr_value = res.register(self.visit(expr, context))
            if res.should_return(): return res
            return res.success(Number.null if should_return_null else expr_value)

        return res.success(Number.null)

    def visit_ForNode(self, node, context):
        res = RTResult()
        elements = []

        start_value = res.register(self.visit(node.start_value_node, context))
        if res.should_return(): return res

        end_value = res.register(self.visit(node.end_value_node, context))
        if res.should_return(): return res

        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node, context))
            if res.should_return(): return res
        else:
            step_value = Number(1)

        i = start_value.value

        if step_value.value >= 0:
            condition = lambda: i < end_value.value
        else:
            condition = lambda: i > end_value.value

        while condition():
            context.symbol_table.set(node.var_name_tok.value, Number(i))
            i += step_value.value

            value = res.register(self.visit(node.body_node, context))
            if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res

            if res.loop_should_continue:
                continue

            if res.loop_should_break:
                break

            elements.append(value)

        return res.success(
            Number.null if node.should_return_null else
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_WhileNode(self, node, context):
        res = RTResult()
        elements = []

        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.should_return(): return res
            
            if not node.is_do_while:
                if not condition.is_true(): 
                    break

            value = res.register(self.visit(node.body_node, context))
            if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res

            if res.loop_should_continue:
                continue

            if res.loop_should_break:
                break

            elements.append(value)
            if not condition.is_true(): 
                break

        return res.success(
            Number.null if node.should_return_null else
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_FuncDefNode(self, node, context):
        res = RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(func_name, body_node, arg_names, node.should_auto_return).set_context(context).set_pos(node.pos_start, node.pos_end)

        if isinstance(context.symbol_table.get(func_name), BuiltInFunction):
            return res.failure(RTError(
                node.var_name_tok.pos_start, node.var_name_tok.pos_end,
                f"Cannot delete a built-in function",
                context
            ))

        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    def visit_ImportNode(self, node, context):
        res = RTResult()

        import_name = res.register(self.visit(node.import_name, context))
        if res.should_return(): return res
        _import = Import(import_name).set_context(context).set_pos(node.pos_start, node.pos_end)
        _, error = _import.import_module()

        if error: return res.failure(error)

        return res.success(Number.null)

    def visit_ArrAccessNode(self, node, context):
        res = RTResult()
        iterable = res.register(self.visit(node.iterable, context))
        if res.should_return(): return res
        iterable = iterable.copy().set_pos(node.pos_start, node.pos_end)

        index = res.register(self.visit(node.index, context))
        if res.should_return(): return res

        if isinstance(index, Number):
            if not isinstance(iterable, List | String):
                return res.failure(RTError(
                    iterable.pos_start, iterable.pos_end,
                    'Object is not a list',
                    context
                ))
            try:
                if isinstance(iterable, List):
                    value = iterable.elements[index.value]
                elif isinstance(iterable, String):
                    value = iterable.value[index.value]
            except:
                return res.failure(RTError(
                    index.pos_start, index.pos_end,
                    'Element at this index could not be retrieved from list because index is out of bounds',
                    context
                ))
        elif isinstance(index, String):
            if not isinstance(iterable, Dict):
                return res.failure(RTError(
                    iterable.pos_start, iterable.pos_end,
                    'Object is not a dictionary',
                    context
                ))
            value = None
            for x in range(len(iterable.elements.keys())):
                if iterable.keys[x].value == index.value:
                    value = iterable.values[x]

            if value == None:
                return res.failure(RTError(
                    index.pos_start, index.pos_end,
                    f"Not a valid key: '{index.value}'",
                    context
                ))
        else:
            return res.failure(RTError(
                    index.pos_start, index.pos_end,
                    'Index is not a number or string',
                    context
                ))

        return res.success(value)

    def visit_CallNode(self, node, context):
        res = RTResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.should_return(): return res
        if not isinstance(value_to_call, BaseFunction):
            return res.failure(RTError(
                value_to_call.pos_start, value_to_call.pos_end,
                'Object is not callable',
                context
            ))
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.should_return(): return res

        return_value = res.register(value_to_call.execute(args))
        if res.should_return(): return res
        return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(return_value)

    def visit_ReturnNode(self, node, context):
        res = RTResult()

        if node.node_to_return:
            value = res.register(self.visit(node.node_to_return, context))
            if res.should_return(): return res
        else:
            value = Number.null

        return res.success_return(value)

    def visit_ContinueNode(self, node, context):
        return RTResult().success_continue()

    def visit_BreakNode(self, node, context):
        return RTResult().success_break()

    def visit_DeleteNode(self, node, context):
        res = RTResult()
        var_name = node.var_name.var_name_tok
        val = res.register(self.visit(node.var_name, context))
        if res.should_return(): return res

        if isinstance(val, BuiltInFunction):
            return res.failure(RTError(
                val.pos_start, val.pos_end,
                f"Cannot delete a built-in function",
                context
            ))

        if not context.symbol_table.get(var_name.value):
            return res.failure(RTError(
                var_name.pos_start, node.pos_end,
                f"'{var_name.value}' is not defined",
                context
            ))

        context.symbol_table.remove(var_name.value)
        return res.success(Number.null)

########################################
# RUN
########################################

global_symbol_table = SymbolTable()
global_symbol_table.set("PI", Number.math_PI)
global_symbol_table.set("POS_INF", Number.math_POS_INF)
global_symbol_table.set("NEG_INF", Number.math_NEG_INF)

global_symbol_table.set("__keywords__", List.KEYWORDS)

global_symbol_table.set("print", BuiltInFunction.print)
global_symbol_table.set("print_ret", BuiltInFunction.print_ret)
global_symbol_table.set("input", BuiltInFunction.input)
global_symbol_table.set("input_int", BuiltInFunction.input_int)
global_symbol_table.set("clear", BuiltInFunction.clear)
global_symbol_table.set("cls", BuiltInFunction.clear)
global_symbol_table.set("is_num", BuiltInFunction.is_number)
global_symbol_table.set("is_str", BuiltInFunction.is_string)
global_symbol_table.set("is_list", BuiltInFunction.is_list)
global_symbol_table.set("is_func", BuiltInFunction.is_function)
global_symbol_table.set("append", BuiltInFunction.append)
global_symbol_table.set("pop", BuiltInFunction.pop)
global_symbol_table.set("extend", BuiltInFunction.extend)
global_symbol_table.set("len", BuiltInFunction.len)
global_symbol_table.set("run", BuiltInFunction.run)
global_symbol_table.set("abs", BuiltInFunction.abs)
global_symbol_table.set("typeof", BuiltInFunction.typeof)

def run(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error
    
    # Run program
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error