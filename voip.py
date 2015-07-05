import mpre
import mpre.authentication

class Message_Server(mpre.authentication.Authenticated_Service):
    
    defaults = mpre.authentication.Authenticated_Service.defaults.copy()
    defaults.update({"contact_lists" : None})
    
    def __init__(self, **kwargs):
        super(Message_Server, self).__init__(**kwargs)
        self.contact_lists = self.contact_lists or {}
        self.mailbox = {"nobody" : []}
        
    def register(self, username, password):
        result = super(Message_Server, self).register(username, password)
        if result:
            self.contact_lists[username] = []
            self.mailbox[contact_name] = []
            return result
            
    @mpre.authentication.authenticated
    def add_to_contacts(self, user_name, contact_name):
        if user_name != self.logged_in[self.requester_address]:
            self.alert("Detected attempt to add a contact to another users entry; {} @ {}: attempted to add {} to {}",
                       [self.logged_in[self.requester_address], self.requester_address, contact_name, user_name], level=0)
            raise UnauthorizedError()
        self.contact_lists[username].append(contact_name)
     
    @mpre.authentication.authenticated
    def send_message(self, username, contact_name, message):
        self.alert("Attempting to send message:\nFrom: {}\nTo: {}\nMessage: {}",
                   (username, contact_name, message), level='')
        print self, "looking up address for: ", contact_name, self.logged_in
        try:
            contact_address = self.logged_in.reverse_lookup(contact_name)
        except KeyError:
            self.mailbox[contact_name].append((username, message))
        else:
            mpre.Instruction("Message_Client", "receive_message", 
                             username, message).execute(host_info=contact_address)
        
        
class Message_Client(mpre.authentication.Authenticated_Client):
            
    defaults = mpre.authentication.Authenticated_Client.defaults.copy()
    defaults.update({"keyword_string" : "messenger",
                     "target_service" : "Message_Server"})
    
    def __init__(self, **kwargs):
        super(Message_Client, self).__init__(**kwargs)
        mpre.objects["Keyword_Handler"].set_keyword(self.keyword_string, self.handle_keystrokes)
    
    def handle_keystrokes(self, keystrokes):
        self.alert("Splitting keystrokes: {}".format(keystrokes))
        if keystrokes != "\n":
            contact, message = keystrokes.strip().split(" ", 1)
            mpre.Instruction(self.target_service, "send_message", 
                            self.username, contact, message).execute(host_info=self.host_info)
                    
    def receive_message(self, sender, message):
        self.alert("{}: {}".format(sender, message), level='v')
        
if __name__ == "__main__":
    objects["Metapython"].create(Message_Server)
    client = objects["Metapython"].create(Message_Client)