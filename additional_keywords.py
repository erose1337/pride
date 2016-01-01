__all__ = ["_export"]

import socket

import pride

def _export(*args):
    try:
        module_name, for_fqdn, as_name = args
    except ValueError:
        module_name, for_fqdn = args
        as_name = module_name
    fqdn = for_fqdn[1]
    as_name = as_name[1]
    
    if pride.compiler.find_module(module_name, None):
        module_source = pride.compiler.module_source[module_name][0]
    else:
        raise ValueError("Unable to find module {}".format(module_name))
    
    ip = socket.gethostbyname(fqdn)      
    for shell in pride.objects["->User"].objects["Shell"]:
        if shell.ip == ip:
            shell.handle_input(module_source)
            break
    else:
        pride.objects["->User"].create("pride.interpreter.Shell", ip=ip, 
                                       startup_definitions=module_source)
                  