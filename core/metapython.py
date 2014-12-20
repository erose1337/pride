import sys
import codeop
import os
from contextlib import closing

import base
import utilities
import defaults
Event = base.Event
    
    
class Shell(base.Process):
    """(Potentially remote) connection to the interactive interpreter"""
    
    defaults = defaults.Shell
    hotkeys = {}
    
    exit_on_help = False
    
    def __init__(self, **kwargs):
        super(Shell, self).__init__(**kwargs)
        self.line = []
        self.lines = []
        options = {"target" : (self.ip, self.port),
                   "incoming" : self._incoming,
                   "outgoing" : self._outgoing,
                   "on_connection" : self._on_connection}        
        
        self.connection = self.create("networklibrary.Outbound_Connection", **options)
        self.definition = False
        self.keyboard = self.create("vmlibrary.Keyboard")
        
    def run(self):        
        if self.network_buffer:
            sys.stdout.write(self.network_buffer+self.prompt)
            self.network_buffer = None
            
        if self.keyboard.input_waiting():
            self.keyboard.get_line(self)     
            
        if self.keyboard_input:
            for character in self.keyboard_input:
                if character == u'\n':
                    self._handle_return() 
                else:
                    self.line.append(character)
            self.keyboard_input = ''
        
        self.propagate()
            
    def _handle_return(self):
        line = ''.join(self.line)
        
        if line == "": # finished entering defintion
            self.definition = False
        self.lines.append(line+"\n")
        lines = "".join(self.lines)
        try:
            code = codeop.compile_command(lines, "<stdin>", "exec")
        except (SyntaxError, OverflowError, ValueError) as error: # did not compile
            if type(error) == SyntaxError:
                sys.stdout.write(self.traceback())
                self.prompt = ">>> "
                self.lines = []
            else:
                self.prompt = "... "
        else:
            if code and not self.definition:
                self.prompt = ">>> "
                self.lines = []
                Event("Asynchronous_Network", "buffer_data", self.connection, lines).post()
            else:
                self.definition = True
                self.prompt = "... "
        sys.stdout.write(self.prompt)
        self.line = [] 
        
    def _outgoing(self, sock, data):
        sock.send(data)
                      
    def _incoming(self, sock):
        self.network_buffer = sock.recv(self.network_packet_size)
                
    def _on_connection(self, connection, address):
        self.connection = connection
        options = {"auto_login" : self.auto_login,
                   "credentials" : (self.username, self.password),
                   "handle_success" : self._on_login_success,
                   "wait" : self._on_wait}
          
        self.login_thread = self.create("networklibrary.Basic_Authentication_Client", **options)
        Event(self.instance_name, "_login", component=self).post()
    
    def _on_login_success(self, connection):
        Event(self.instance_name, "run", component=self).post()
        print self.network_buffer
        self.network_buffer = ''
        sys.stdout.write(self.prompt)      
        if self.startup_definitions:
            try:
                sys.stdout.write("Attempting to compile startup definitions...\n%s" % self.prompt)              
                compile(self.startup_definitions, "startup_definition", "exec")
            except:
                args = (self.instance_name, traceback.format_exc())
                self.alert("{0} startup definitions failed to compile\n{1}".format(*args), 5)
            else:
                Event("Asynchronous_Network", "buffer_data", self.connection, self.startup_definitions+"\n").post()
    
    def _on_wait(self):
        Event(self.instance_name, "_login", component=self).post()   
    
    def _login(self):
        self.login_thread.run()        
                
                
class Metapython(base.Process):
    
    defaults = defaults.Metapython
    
    parser_ignore = ("environment_setup", "prompt", "copyright", "authentication_scheme",
                     "auto_start", "keyboard_input", "traceback", "pypy", "jython",
                     "python", "network_buffer", "stdin_buffer_size", "memory_size",
                     "network_packet_size", "interface", "port")
    parser_modifiers = {"command" : {"types" : ("positional", ),
                                     "nargs" : '?'},           
                        "help" : {"types" : ("short", "long"),
                                  "nargs" : '?'}
                        }
    exit_on_help = False
    
    for attribute in parser_ignore:
        parser_modifiers[attribute] = "ignore"
    
    def __init__(self, **kwargs):
        self.process_requests = []
        self.connected_clients = []
        self.login_threads = []
        self.authenticate = {"root" : hash("password")}
        self.client_namespaces = {}
        self.swap_file = open("log_swap_file", "w+")
        self.log_file = open("%s_log" % self.__class__.__name__, "a")
        
        super(Metapython, self).__init__(**kwargs)
        self.objects.setdefault(self.authentication_scheme.split(".", 1)[-1], [])
        self.network_buffer = {}
        self.setup_environment()
        self.start_interpreter()
        
    def setup_environment(self):
        modes = {"=" : "equals",
                 "+=" : "__add__", # append strings or add ints
                 "-=" : "__sub__", # integer values only
                 "*=" : "__mul__", 
                 "/=" : "__div__"}               
        
        for command in self.environment_setup:
            variable, mode, value = command.split()
            if modes[mode] == "equals":
                result = value        
            else:
                environment_value = os.environ[variable]
                method = modes[mode]
                result = getattr(environment_value, method)(value)
            os.environ[variable] = result
    
    def start_interpreter(self):
        options = {"incoming" : self._read_socket,
                   "outgoing" : self._write_socket,
                   "on_connection" : self._on_connection,
                   "name" : "Metapython_Interpreter",
                   "interface" : self.interface,
                   "port" : self.port}
        
        Event("Asynchronous_Network", "create", "networklibrary.Server", **options).post()
        module_name = self.command.split(".py")[0]
        try:
            module = __import__(module_name)
        except ImportError:
            raise
        else:            
            machine = self.create("vmlibrary.Machine")
            machine.create("networklibrary.Asynchronous_Network")
            machine.run()                
            
    def _on_connection(self, connection, address):
        self.network_buffer[connection] = ''
        args = (connection, address)
        options = {"handle_success" : self.handle_login_success}
        login_thread = self.create(self.authentication_scheme, *args, **options)
                               
    def _read_socket(self, connection):
        self.network_buffer[connection] = connection.recv(8096)
            
    def _write_socket(self, connection, data):
        connection.send(data)
        
    def run(self):    
        self.handle_logins()
        
        for client in self.connected_clients:
            input = self.network_buffer[client]
            self.network_buffer[client] = ''
            if input:
                self._main(client, input)

        #for index, process in enumerate(self.process_requests):
         #   self.process_requests.remove[index]
            #utilities.shell("{0} {1}".format(*process))
        
        Event(self.instance_name, "run", component=self, priority=self.priority).post()

    def handle_logins(self):
        for login_thread in self.objects["Basic_Authentication"]:
            login_thread.run()
                    
    def handle_login_success(self, connection, address):
        username = connection.username
        prompt = self.prompt
        string_info = (username, address, sys.version, sys.platform, self.copyright, 
                       self.__class__.__name__, self.implementation)
        
        response = "Welcome {0} from {1}\nPython {2} on {3}\n{4}\n{5} ({6})\n".format(*string_info)   
        Event("Asynchronous_Network", "buffer_data", connection, response).post()
                                
        self.connected_clients.append(connection)
        self.network_buffer[connection] = ""    
                
        # controls namespace that clients have access to        
        #self.client_namespaces[connection] = {"__builtins__" : globals()["__builtins__"], \
        #"__doc__" : globals()["__doc__"], \
        #"__name__" : "%s __main__" % username, \
        #"Event" : Event, \
        #self.parent.name : self.parent}
                
    def _main(self, connection, input):     
        backup = sys.stdout
        sys.stdout = self.swap_file
        code = self._compile(input)
        if code:
            self.execute_code(code)
            
        sys.stdout.seek(0)
        results = sys.stdout.read()
        if results:
            self.log_file.write("Results: " + results)
            Event("Asynchronous_Network", "buffer_data", connection, results).post()
        sys.stdout.seek(0)
        sys.stdout.truncate() # delete contents
        sys.stdout = backup
            
    def _compile(self, input):
        try:
            code = codeop.compile_command(input, "<stdin>", "exec")
        except (SyntaxError, OverflowError, ValueError) as error: # did not compile
            if type(error) == SyntaxError:
                sys.stdout.write(self.traceback())
        else:
            self.log_file.write("Command:\n"+input)
            return code                                                                       
        
    def execute_code(self, code):
        try:
            exec code in locals(), globals()
        except BaseException as error:
            sys.stdout = self.swap_file # can be changed by code and not changed back
            if type(error) == SystemExit:
                raise
            else:
                sys.stdout.write(self.traceback())      
                
    @staticmethod           
    def start_process(sys_argvs):
        os.execlp(*sys_argvs)
                         
 
if __name__ == "__main__": 
    metapython = Metapython(parse_args=True, parent=__name__)
    