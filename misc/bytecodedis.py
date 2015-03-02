import sys
import dis
import ast
from collections import OrderedDict

import bytecodemap

symbol_translator = {"*" : "__mul__",
                     "/" : "__div__",
                     "+" : "__add__",
                     "-" : "__sub__"}

block_stack = [0 for x in xrange(256)]
cmp_op = dis.cmp_op
bytecode_counter = []
opcode = []
dictionary = {}
_global = []
continue_loop = []
TOS = []
TOS_TOS1 = []
TOS_TOS2 = []
TOS_TOS3 = []
def translator(statement):
    if "." in statement:
        # base.create("testing.Testing")
        _object, method_call = statement.split('.')
        method, arguments = method_call.split("(")
        arguments = "(" + arguments
    else:
        _object, method, arguments = statement.split()

    try:
        method = symbol_translator[method]
    except KeyError:
        pass
    call = getattr(ast.literal_eval(_object), method)
    return call(ast.literal_eval(arguments))


valid_bytecodes = [opcode for opcode in dis.opname if "<" and ">" not in opcode]

def get_variable_types(function):
    code_object = function.func_code
    opcodes = [ord(char) for char in code_object.co_code]
    
    assignment_operators = ("STORE_FAST", "STORE_GLOBAL", "STORE_ATTR", 
                            "STORE_SUBSCR", "RETURN_VALUE")
    
    assignment_opcodes = [(operator, dis.opmap[operator]) for operator in                       assignment_operators]
                         
    # find a list of assignment operations, which are the "store" opcodes
    assignments = dict((operator, []) for operator in assignment_opcodes)
                        
    for operation_info in assignment_opcodes:
        operation = operation_info[1]
        quantity = opcodes.count(operation)
        last_address = 0
        for assignment_number in range(quantity):
            address = opcodes.index(operation, last_address+1)
            #variable_address = opcodes[address+1]
            assignments[operation_info].append(address)
            last_address = address
    return assignments    


def get_opcode_info(function):
    import opcode
    container_names = ("hasconst", "hasname", "hasjrel", "haslocal", 
                       "hascompare", "hasfree")
    
    containers = dict((name, tuple(getattr(opcode, name))) for 
                       name in container_names)
    
    
    reverse_opmap = dict((value, key) for key, value in dis.opmap.items())
    code_object = function.func_code
    opcodes = code_object.co_code
    results = []
 
    stores_in = {"hasconst" : "co_consts",
                 "hasname" : "co_names",
                 "haslocal" : "co_varnames"}
    
    address = 0
    address_range = len(opcodes)    
    while address < address_range:
        operator = ord(opcodes[address])
        operator_name = reverse_opmap[operator]
        
        if operator >= dis.HAVE_ARGUMENT:
            argument_address = (ord(opcodes[address + 1]) + 
                               (ord(opcodes[address + 2]) * 256))
                               
          #  if operator_name == "STORE_ATTR":
                # resolve the name: go backwards until something other load_attr
                # name resides in code_object.co_names
                
            for container in container_names:
                if operator in containers[container]:
                    if container is "hasjrel":
                        argument = argument_address + address
                    elif container is "hasfree":
                        freevars = code_object.co_cellvars + code_object.co_freevars
                        argument = freevars[argument_address]
                    else:
                        code_attribute = getattr(code_object, stores_in[container])
                        argument = code_attribute[argument_address]
          
            result = (address, operator_name, argument_address, argument)
            address += 2
        else:
            result = (address, operator_name, None, None)
        address += 1
        results.append(result)
    return results

    
if __name__ == "__main__":

    
    import mpre.base as base
    method = base.Base.__init__
    
    dis.dis(method)  
    for address, opcode, arg_addr, arg_value in get_opcode_info(method):
        print "{: >5} {: >15} {} {}".format(address, opcode, arg_addr, arg_value)
    print "variable assignments: ", get_variable_types(method)
    