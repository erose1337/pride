import sys
import random
import hashlib
import os
import getpass

from pride import Instruction
import pride.security
import pride.decorators
import pride.contextmanagers
import pride.utilities
from pride.security import hash_function
from pride.errors import SecurityError, UnauthorizedError             

# generate encryption/signing key pairs
# encrypt the private key symmetrically via a password
    # private key can be stored on device, or on the server
    
# send session key to partner
# xor key with key sent by partner

# server stores: identifier, encrypted private key, (possibly encrypted) public key, hmac(keypair, client_HMAC_key)

#client --request public key-user:server----------------------------> server
#client <----------------------------------------servers public key-- server
#

#client --.request private key


#client --register-username-password-keypair_tag-encrypted_private_key-public_key-> server
#
#client --login-username--encrypted_session_secret1------------> server
#client <--encrypted_private_key-encrypted_session_secret2------ server
# |                                                                |
# |                                                                |
# |                                                                |
#derive session secret                                       derive session secret
#    - decrypt encrypted_session_secret via private key
#    - xor both session secrets together to obtain final session secret

    
                    
@pride.decorators.required_arguments(no_args=True)
def remote_procedure_call(callback_name='', callback=None):
    def decorate(function):       
        call_name = function.__name__
        def _make_rpc(self, *args, **kwargs):  
            if callback_name:
                _callback = getattr(self, callback_name)
            else:
                _callback = callback or None
                
            instruction = Instruction(self.target_service, call_name, *args, **kwargs)
            if not self.logged_in and call_name not in ("register", "login", "login_stage_two"):                 
                self.handle_not_logged_in(instruction, _callback)            
            else:
                self.alert("Making request '{}.{}'", (self.target_service, call_name),
                           level=self.verbosity[call_name])    
                self.session.execute(instruction, _callback)
        return _make_rpc
    return decorate
      
def _split_byte(byte):
    """ Splits a byte into high and low order bytes. 
        Returns two integers between 0-15 """
    bits = format(byte, 'b').zfill(8)
    a, b = int(bits[:4], 2), int(bits[4:], 2)
    return a, b     
        
class Authenticated_Service(pride.base.Base):
   
    defaults = {# security related configuration options
                "iterations" : 100000, "password_hashing_algorithm" : "pbkdf2hmac",
                "sub_algorithm" : "sha512", "salt_size" : 16, "output_size" : 32,
                                                                
                # non security related configuration options
                "database_type" : "pride.database.Database", "database_name" : '',
                "validation_failure_string" :\
                   ".validate: Authorization Failure:\n" +
                   "    ip blacklisted: {}    ip whitelisted: {}\n" +
                   "    session_id logged in: {}\n" + 
                   "    method_name: '{}'    method available remotely: {}\n" +                   
                   "    login allowed: {}    registration allowed: {}",
                "allow_login" : True, "allow_registration" : True,
                "login_message" : "Welcome to the {}, {} from {}"}                     
    
    verbosity = {"register" : "vv", "validate_success" : 'vvv',
                 "login" : "vv", "authentication_success" : "vv",
                 "authentication_failure" : "v", "validate_failure" : "vvv",                
                 "authentication_failure_already_logged_in" : 'v'}
    
    flags = {"current_session" : ('', None)}
     
    database_structure = {"Users" : ("identifier BLOB PRIMARY_KEY", 
                                     "verifier_hash BLOB", "salt BLOB")}
                              
    database_flags = {"primary_key" : {"Users" : "identifier"}}
    
    remotely_available_procedures = ("register", "login", "change_credentials", "logout")
    
    rate_limit = {"login" : 2, "register" : 2}       
    
    mutable_defaults = {"_rate" : dict, "ip_whitelist" : list, "ip_blacklist" : list,
                        "_challenge_answer" : dict, "session_id" : dict, "peer_ip" : dict}
                        
    inherited_attributes = {"database_structure" : dict, "database_flags" : dict,
                            "remotely_available_procedures" : tuple, "rate_limit" : dict}
    
    def _get_current_user(self):
        return self.session_id[self.current_session[0]]
        
    def _set_current_user(self, session_id, ip, username):
        self.session_id[session_id] = username
        self.peer_ip[session_id] = ip
        
    def _del_current_user(self):
        id = self.current_session[0]
        del self.session_id[id]
        del self.peer_ip[id]
    current_user = property(_get_current_user, _set_current_user, fdel=_del_current_user)
    
    def __init__(self, **kwargs):
        super(Authenticated_Service, self).__init__(**kwargs)
        self._load_database()    
                
    def _load_database(self):
        if not self.database_name:
            _reference = '_'.join(name for name in self.reference.split("/") if name)
            name = self.database_name = os.path.join(pride.site_config.PRIDE_DIRECTORY,
                                                     "{}.db".format(_reference))
        else:
            name = self.database_name
        self.database = self.create(self.database_type, database_name=name,
                                    database_structure=self.database_structure,
                                    **self.database_flags)
            
  #  def register(self, identifier, encrypted_private_key, public_key, keypair_tag):
  #      self.alert("Registering new user", level=self.verbosity["register"])
  #     
  #      self.database.insert_into("Users", (identifier, encrypted_private_key, public_key, 
  #                                          keypair_tag, "\x00" * self.shared_key_size))
  #      return True
  #      
  #  def get_public_key(self, identifier):
  #      public_key = self.database.query("Users", retrieve_fields=("public_key", ), 
  #                                                where={"identifier" : identifier})
  #      return public_key
    
    def register(self, identifier, password_verifier):        
        salt = os.urandom(self.salt_size)
        verifier_hash = self._hash_password(password_verifier, salt)
        self.database.insert_into("Users", (identifier, verifier_hash, salt))
        return self.register_success(identifier)
        
    def change_credentials(self, identifier, password_verifier, new_identifier, new_password_verifier):
        correct_verifier, salt = self.database.query("Users", retrieve_fields=("verifier_hash", "salt"),
                                                              where={"identifier" : identifier})
        if pride.security.constant_time_comparison(correct_verifier, password_verifier):
            return self.register(new_identifier, new_password_verifier)
        else:
            return self.register_failure(identifier)
    
    def register_success(self, username):
        return self.registration_success_message.format(username)
    
    def register_failure(self, username):
        return self.registration_failure_message.format(username)
        
    def login(self, username, password):      
        correct_hash, salt = self.database.query("Users", retrieve_fields=("verifier_hash", "salt"), 
                                                          where={"username" : username})                                                          
        password_hash = self._hash_password(password, salt)
        if pride.security.constant_time_comparison(password_hash, correct_hash):
            return self.login_success(username)
        else:
            return self.login_failure(username)
            
    def login_success(self, username):
        session_id, user_ip = self.current_session
        self.current_user = session_id, username, user_ip
        self.alert("'{}' logged in successfully from {}".format(username, user_ip), level=self.verbosity["login_success"])
        return True
        
    def login_failure(self, username):
        self.alert("'{}' failed to login".format(username), level=self.verbosity["login_failure"])
        return False         
        
    def _hash_password(self, password, salt):
        return pride.security.hash_password(password, self.iterations, algorithm=self.password_hashing_algorithm, 
                                                                       sub_algorithm=self.sub_algorithm,
                                                                       salt=salt, output_size=self.output_size)   
    def logout(self):        
        del self.current_user     
        
    def validate(self, session_id, peername, method_name):
        """ Determines whether or not the peer with the supplied
            session id is allowed to call the requested method.

            Sets current_session attribute to (session_id, peername) if validation
            is successful. """
        if ((method_name not in self.remotely_available_procedures) or
            (peername[0] in self.ip_blacklist) or 
            (session_id == '0' and method_name not in ("register", "login")) or
            (session_id not in self.session_id and method_name not in ("register", "login")) or
            (method_name == "register" and not self.allow_registration) or
            (method_name == "login" and not self.allow_login)):
            
        #    print session_id
        #    print
        #    print self.session_id.keys()[0]
       #     return False
            self.alert(self.validation_failure_string,
                      (peername[0] in self.ip_blacklist, peername[0] in self.ip_whitelist,
                       session_id in self.session_id,
                       method_name, method_name in self.remotely_available_procedures,
                       self.allow_login, self.allow_registration),
                       level=0)#self.verbosity["validate_failure"])
            return False         
        if self.rate_limit and method_name in self.rate_limit:
            _new_connection = False
            try:
                self._rate[session_id][method_name].mark()
            except KeyError:
                latency = pride.datastructures.Latency("{}_{}".format(session_id, method_name))
                try:
                    self._rate[session_id][method_name] = latency
                except KeyError:
                    self._rate[session_id] = {method_name : latency}   
                    _new_connection = True
            if not _new_connection:
                current_rate = self._rate[session_id][method_name].last_measurement                
                if current_rate < self.rate_limit[method_name]:
                    self.alert("Rate of {} calls exceeded 1/{}s ({}); Denying request",
                            (method_name, self.rate_limit[method_name], current_rate),                           
                            level=self.verbosity["validate_failure"])
                    return False

 #       if self.enforce_idle_timeout:
 #           self.not_idle.add(session_id)            
            
        self.alert("Authorizing: {} for {}", 
                  (peername, method_name), 
                  level=self.verbosity["validate_success"])
        return True        

    def execute_remote_procedure_call(self, session_id, peername, method_name, args, kwargs):
        with pride.contextmanagers.backup(self, "current_session"):
            self.current_session = (session_id, peername)            
            return getattr(self, method_name)(*args, **kwargs) 
                
    def __getstate__(self):
        state = super(Authenticated_Service, self).__getstate__()
        del state["database"]
        return state
        
    def on_load(self, attributes):
        super(Authenticated_Service, self).on_load(attributes)
        self._load_database()

  
class Authenticated_Client(pride.base.Base):   
    
    verbosity = {"register" : 0, "login" : 'v', "answer_challenge" : 'vv',
                 "login_stage_two" : 'vv', "register_sucess" : 0,
                 "auto_login" : 'v', "logout" : 'v', "login_message" : 0,
                 "delayed_request_sent" : "vv", "login_failed" : 0}
                 
    defaults = {"target_service" : "/Python/Authenticated_Service",
                "username_prompt" : "{}: Please provide the user name for {}@{}: ",
                "password_prompt" : "{}: Please provide the pass phrase or word for {}@{}: ",
                "ip" : "localhost", "port" : 40022, "auto_login" : True, 
                 
                "username" : '', "password" : None, "hash_password_clientside" : True,
                "iterations" : 100000, "password_hashing_algorithm" : "pbkdf2hmac",
                "sub_algorithm" : "sha512", "salt" : None, "salt_size" : 16, "output_size" : 32}
    
    mutable_defaults = {"_delayed_requests" : list}
    flags = {"_registering" : False, "logged_in" : False, "_logging_in" : False,
             "_username" : '', "auto_register" : False, "_insert_new_user_into_site_config" : None,
             "_password_hash" : ''}       
                    
    def _get_password(self):
        return self._password or getpass.getpass(self.password_prompt)
    def _set_password(self, value):
        self._password = value
    password = property(_get_password, _set_password)
            
    def _get_password_hash(self):
        return self._password_hash or self._hash_password(self.password)
    def _set_password_hash(self, value):
        self._password_hash = value
    password_hash = property(_get_password_hash, _set_password_hash)
        
    def _get_host_info(self):
        return (self.ip, self.port)
    def _set_host_info(self, value):
        self.ip, self.port = value
    host_info = property(_get_host_info, _set_host_info)      
    
    def _get_username(self):
        if not self._username:
            self._username = raw_input(self.username_prompt.format(self.reference,
                                                                   self.target_service,
                                                                   self.ip))
        return self._username
    def _set_username(self, value):        
        self._username = value
    username = property(_get_username, _set_username)
                
    def _get_insert_new_user_into_site_config(self):
        if self._insert_new_user_into_site_config is None:
            return pride.shell.get_permission("{}: Insert username into site_config?: ".format(self.reference))
        else:
            return self._insert_new_user_into_site_config
    register_username_as_default = property(_get_insert_new_user_into_site_config)
    
    def __init__(self, **kwargs):
        super(Authenticated_Client, self).__init__(**kwargs)
        self.password_prompt = self.password_prompt.format(self.reference, self.ip, self.target_service)
        self.session = self.create("pride.rpc.Session", session_id='0', host_info=self.host_info)
                                                       
        if self.auto_login:
            self.alert("Auto logging in", level=self.verbosity["auto_login"])
            self.login()
    
    def get_credentials(self):
        return (self, (self.username, self.password_hash if self.hash_password_clientside else self.password), {})
                
    @pride.decorators.with_arguments_from(get_credentials)
    @remote_procedure_call(callback_name="register_results")
    def register(self, username, password_hash): 
        pass
    
    def register_results(self, server_response):
        self._registering = False  
        if server_response == True:
            self.register_success()
        else:
            self.register_failure()                                                      
                        
    def register_success(self):
        self.alert("Registered successfully", level=self.verbosity["register_success"])
        
        if pride.shell.get_permission("{}: Insert username into site_config?: ".format(self.reference)):
            entry = '_'.join((self.__module__.replace('.', '_'),
                              self.__class__.__name__,
                              "defaults"))                            
            pride.site_config.write_to(entry, username=self.username)

        if self.auto_login:
            self.login()
                
    def register_failure(self):
        self.alert("Registration failed", level=self.verbosity["register_failure"])
        
    def login(self):
        return self.get_credentials()

    def _login(self):                                
        self._logging_in = True    
        self.session.id = '0'
        return self, self.get_credentials(), {}
            
    @pride.decorators.with_arguments_from(_login)
    @remote_procedure_call(callback_name="login_result")
    def login(self, username, password):
        pass
        
    def login_result(self, server_response):
        self._logging_in = False
        if server_response:
            self.login_success(server_response)
        else:
            self.login_failure(server_response)
    
    def login_success(self, login_message):
        self.alert("Login success; Received server response: {}".format(login_message, level=self.verbosity['login_success']))    
        self.logged_in = True        
        self.alert("{}", [login_message], level=self.verbosity["login_message"])        
        for instruction, callback in self._delayed_requests:
            self.alert("Making delayed request: {}",
                      [(instruction.component_name, instruction.method)],
                      level=self.verbosity["delayed_request_sent"])
            self.session.execute(instruction, callback)
        self._delayed_requests = []
        
    def _reset_login_flags(self):
        self.logged_in = False
        self.session.id = '0'       
        
    def login_failure(self, server_response):        
        self.logged_in = False
        self.alert("Login failure; Received server response: {}".format(server_response, level=self.verbosity['login_failure']))

    @pride.decorators.call_if(logged_in=True)
    @pride.decorators.exit(_reset_login_flags)
    @remote_procedure_call(callback=None)
    def logout(self): 
        """ Logout self.username from the target service. If the user is logged in,
            the logged_in flag will be set to False and the session.id set to '0'.
            If the user is not logged in, this is a no-op. """
    
    def handle_not_logged_in(self, instruction, callback):        
        if self.auto_login or pride.shell.get_permission("Login now? :"):
            self._delayed_requests.append((instruction, callback))
            if not self._logging_in:
                self.alert("Not logged in")       
                self.login()            
                
    def delete(self):
        if self.logged_in:
            self.logout()
        super(Authenticated_Client, self).delete()
        
    def __getstate__(self):
        attributes = super(Authenticated_Client, self).__getstate__()
        del attributes["session"]
        attributes["objects"] = {}
        attributes["logged_in"] = False
        attributes["session_id"] = '0'
        return attributes
    
    def on_load(self, attributes):
        super(Authenticated_Client, self).on_load(attributes)        
        self.session = self.create("pride.rpc.Session", session_id='0', host_info=self.host_info)                               
                                       
        #if self.auto_login:
        #    self.alert("Auto logging in", level=self.verbosity["auto_login"])
        #    self.login()
        
        
    def _hash_password(self, password):
        return pride.security.hash_password(password, self.iterations, algorithm=self.password_hashing_algorithm, 
                                                                       sub_algorithm=self.sub_algorithm,
                                                                       salt=self.salt, salt_size=self.salt_size, 
                                                                       output_size=self.output_size) 
                                                                           












                                                                           #def save_file(self, filename, data, indexable=False):    
        #with self.create(self.token_file_type, self.authentication_table_file, 
        #'wb', encrypted=True, indexable=indexable) as _file:
            #_file.write(new_table + ("\x00" * self.shared_key_size))
        
   # def username_not_registered(self): # called when login fails because user is not registered
   #     if not self._registering:
   #         self.alert("Login token for '{}' not found ({})", (self.username, self.authentication_table_file), level=0)            
   #         if self.auto_register or pride.shell.get_permission("Register now? "):                  
   #             if self.ip in ("localhost", "127.0.0.1"):
   #                 local_service = objects[self.target_service]
   #                 authentication_table = local_service.register(self.username)
   #                 self._store_auth_table(authentication_table)                                       
   #             else:
   #                 self.register()
                    

    
    #def _answer_challenge(self, response):
    #    hashed_answer, challenge = response
    #    if hashed_answer != self._answer:
    #        raise SecurityError("Server responded with incorrect response to challenge")
    #
    #    answer = Authentication_Table.load(self.auth_table).get_passcode(*challenge)
    #    hasher = hash_function(self.hash_function)
    #    hasher.update(answer + ':' + self.shared_key)
    #    self.alert("Answering challenge", level=self.verbosity["answer_challenge"])
    #    return (self, hasher.finalize(), challenge), {}
    #    
    #@pride.decorators.with_arguments_from(_answer_challenge)
    #@remote_procedure_call(callback_name="decrypt_new_secret")
    #def login_stage_two(self, authenticated_table_hash, answer, challenge): pass
    #
    #def unpack_table_and_key(self, saved_data):
    #    table_size = self.authentication_table_size
    #    return saved_data[:table_size], saved_data[table_size:table_size + self.shared_key_size]
    #    
    #def decrypt_new_secret(self, encrypted_key):
    #    storage = pride.objects["/Python/Encryption_Service"]
    #    saved_data = storage.read_from_file(self.authentication_table_file, self.file_system, self.crypto_provider)
    #    auth_table, shared_key = self.unpack_table_and_key(saved_data)
    #    try:
    #        packed_key_and_message = pride.security.decrypt(encrypted_key, shared_key, shared_key)
    #    except ValueError:                
    #        self.alert("Login attempt failed", level=self.verbosity["login_failed"])
    #        self._logging_in = False
    #        self.handle_login_failure()
    #    else:
    #        new_key, login_message = pride.utilities.load_data(packed_key_and_message)
    #        self.shared_key = new_key
    #        hkdf = invoke("pride.security.hkdf_expand", self.hash_function,
    #                      length=self.authentication_table_size,
    #                      info=self.hkdf_table_update_info_string) 
    #            
    #    new_table = hkdf.derive(auth_table + ':' + new_key)            
    #    storage.save_to_file(self.authentication_table_file, new_table + new_key, 'wb', 
    #                         file_system=self.file_system, crypto_provider=self.crypto_provider)
    #    
    #    self.session.id = self._hash_auth_table(new_table, new_key)
    #    self.on_login(login_message)
    #    
    #def on_login(self, login_message):
    #    self.logged_in = True
    #    self._logging_in = False
    #    self.alert("{}", [login_message], level=self.verbosity["login_message"])        
    #    for instruction, callback in self._delayed_requests:
    #        self.alert("Making delayed request: {}",
    #                  [(instruction.component_name, instruction.method)],
    #                  level=self.verbosity["delayed_request_sent"])
    #        self.session.execute(instruction, callback)
    #    self._delayed_requests = []
    #    
    #def _reset_login_flags(self):
    #    self.logged_in = False
    #    self.session.id = '0'
    #    
    #@pride.decorators.call_if(logged_in=True)
    #@pride.decorators.exit(_reset_login_flags)
    #@remote_procedure_call(callback=None)
    #def logout(self): 
    #    """ Logout self.username from the target service. If the user is logged in,
    #        the logged_in flag will be set to False and the session.id set to '0'.
    #        If the user is not logged in, this is a no-op. """
    #
    #def handle_not_logged_in(self, instruction, callback):        
    #    if self.auto_login or pride.shell.get_permission("Login now? :"):
    #        self._delayed_requests.append((instruction, callback))
    #        if not self._logging_in:
    #            self.alert("Not logged in")       
    #            self.login()            
    #            
    #def delete(self):
    #    if self.logged_in:
    #        self.logout()
    #    super(Authenticated_Client, self).delete()
    #    
    #def __getstate__(self):
    #    attributes = super(Authenticated_Client, self).__getstate__()
    #    del attributes["session"]
    #    attributes["objects"] = {}
    #    attributes["logged_in"] = False
    #    attributes["session_id"] = '0'
    #    return attributes
    #
    #def on_load(self, attributes):
    #    super(Authenticated_Client, self).on_load(attributes)        
    #    self.session = self.create("pride.rpc.Session", session_id='0', host_info=self.host_info)                               
    #                                   
    #    #if self.auto_login:
    #    #    self.alert("Auto logging in", level=self.verbosity["auto_login"])
    #    #    self.login()
    
        
        
def test_Authenticated_Service3():    
    service = objects["/Python"].create(Authenticated_Service)
    client = objects["/Python"].create(Authenticated_Client, username="Authenticated_Service3_unit_test", 
                                       auto_register=True, auto_login=True)
    Instruction(client.reference, "delete").execute(priority=1.5, callback=lambda *args, **kwargs: service.delete)    
    
if __name__ == "__main__":
    test_Authenticated_Service3()
    