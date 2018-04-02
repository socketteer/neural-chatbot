# -*- coding: UTF-8 -*-
from fbchat import  Client
from fbchat.models import Message
from getpass import getpass
import re
import subprocess
import time
import random
import vocab_cleaner
import argparse

class FBMessage:
    def __init__(self, text, author_id):
        self.text = text
        self.id = author_id

class FBThread:
    messages = []
    def __init__(self, thread_id, thread_type):
        self.thread_id = thread_id
        self.thread_type = thread_type
        self.messages.append(FBMessage("<START>\n", "None"))
    
    def add_message(self, message, author_id, self_id): #name? #let's just take 1 message at a time
        #pop oldest message if more than maxthread messages in thread
        if(len(self.messages) >= maxthread):
            self.messages.pop(0)
        # "<switch>\n>" is also added before generating text, but not saved
        if(not self.messages[-1].id == author_id):
            self.messages[-1].text = self.messages[-1].text + "<switch>\n"  
        if(author_id == self_id):       
            message = '>' + message
            
        #remove non ascii characters
        message = vocab_cleaner.filter_non_ascii(message)
        message = message + '\n'  
        self.messages.append(FBMessage(message, author_id))
    
    def get_messages(self):
        return ''.join(message.text for message in self.messages) #this is what the nn sees
    
    def print_messages(self):
        print(self.get_messages())


class AutoResponder(Client):
    threads = []
        
    def onMessage(self, author_id, message_object, thread_id, thread_type,**kwargs): #TODO: thread queue and/or interrupt
        if(thread_id not in thread_blacklist):
            self.markAsDelivered(author_id, thread_id)
            self.markAsRead(author_id)
            sender = client.fetchUserInfo(author_id)[author_id]
            sender_name = sender.name.split(' ')[0]
            #update thread
            current_thread = self.get_thread(thread_id, thread_type)
            if(author_id != self.uid):
                current_thread.add_message(message_object.text, author_id, self.uid)
                if(verbose):
                    print("Sender name: %s" % sender_name)
                    print("Current thread: %s" % thread_id)
                    print("Thread content:")
                    current_thread.print_messages()
                if(author_id not in user_blacklist):
                    self.send_message(current_thread)
            
    def send_message(self, thread):
        thread_id = thread.thread_id
        thread_type = thread.thread_type
        messages_input = thread.get_messages() + "<switch>\n>"
        response = subprocess.check_output(['th', \
                                          'sample.lua', \
                                          cv, \
                                          '-length', str(maxlength), \
                                          '-verbose', '0', \
                                          '-seed', str(random.randint(0, 300)), \
                                          '-primetext', messages_input], cwd="./char-rnn").decode("utf-8")
    
        response_list = self.processOutput(response, messages_input, thread)
        #send predicted responses
        if(len(response_list) > maxmessages):
            response_list = response_list[:maxmessages]
        for resp in response_list:
            if(delay):
                time.sleep(0.5 + len(resp)/3)
            thread.add_message(resp, self.uid, self.uid)
            self.send(Message(text=resp), thread_id=thread_id, thread_type=thread_type)
            
    def get_thread(self, thread_id, thread_type):
        for thread in self.threads:
            #if thread is in list
            if(thread.thread_id == thread_id):
                return thread
        #if thread not found, add new thread    
        self.threads.append(FBThread(thread_id, thread_type));
        return self.threads[-1]
    
    def processOutput(self, response, messages_input, thread):
        #delete redundant thread information from generated response
        response = response.replace(messages_input, "", 1)
        response = re.split('<switch>|<START>', response)[0]
        response_list = response.split('\n')
        
        #removing '>'
        response_list = list(filter(None, response_list))
        for i, msg in enumerate(response_list[1:]):
            if(msg[0] == '>'):
                response_list[i+1] = msg[1:]
        return response_list
    

parser = argparse.ArgumentParser()
parser.add_argument("policy", metavar = 'P', help="chatbot policy (.t7 file )")
parser.add_argument("-v", "--verbose", help="display verbose logging during chatbot operation",
                    action="store_true")
parser.add_argument("-l", "--maxlength", type=int, default = 400, help="maximum character length of generated responses")
parser.add_argument("-m", "--maxmessages", type=int, default = 3, help="maximum number of generated messages")
parser.add_argument("-t", "--threadlength", type=int, default = 15, help="maximum number of messages from each thread saved in in memory")
parser.add_argument("-d", "--delay", help="insert realistic delay before sending messages",
                    action="store_true")
args = parser.parse_args()

cv = '../saved_policies/%s' % args.policy
verbose = args.verbose
maxlength = args.maxlength
maxmessages = args.maxmessages
delay = args.delay
maxthread = args.threadlength

user_blacklist = open('blacklist/user_blacklist','r').read().split('\n')
user_blacklist = list(filter(None, user_blacklist))
thread_blacklist = open('blacklist/thread_blacklist','r').read().split('\n')
thread_blacklist = list(filter(None, thread_blacklist))

username = str(input("Username/email: "))
client = AutoResponder(username, getpass())
client.listen()