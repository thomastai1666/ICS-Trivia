S_ALONE = 0
S_TALKING = 1

#==============================================================================
# Group class:
# member fields: 
#   - An array of items, each a Member class
#   - A dictionary that keeps who is a chat group
# member functions:
#    - join: first time in
#    - leave: leave the system, and the group
#    - list_my_peers: who is in chatting with me?
#    - list_all: who is in the system, and the chat groups
#    - connect: connect to a peer in a chat group, and become part of the group
#    - disconnect: leave the chat group but stay in the system
#==============================================================================

class Group:
    
    def __init__(self):
        self.members = {}
        self.chat_grps = {}
        self.grp_ever = 0
        
    def join(self, name):
        self.members[name] = S_ALONE
        return
        
    #implemented   
    def is_member(self, name):
        #If in members list, return true, otherwise return false
        if(name in self.members):
            return True
        else:
            return False
            
    #implemented
    def leave(self, name):
        #Disconnect user, and delete from member list
        self.disconnect(name)
        del self.members[name]
        return None
        
    #implement                
    def find_group(self, name):
        found = False
        group_key = 0
        #Iterate through chat groups until user is found
        #otherwise return false
        for key, value in self.chat_grps.items():
            if name in value:
                found = True
                group_key = key
        return found, group_key
        
    #implemented  
    def connect(self, me, peer):
        peer_in_group, group_key = self.find_group(peer)
        #If member is already talking, don't do anything
        if(self.members[me] == S_TALKING):
            return None
        #if peer is in a group and you're not chatting, join it
        elif peer_in_group and self.is_member(me):
            self.chat_grps[group_key].append(me)
            #Change states
            self.members[me] = S_TALKING
        # otherwise, create a new group with you and your peer
        else:
            #Make sure both members exist before connecting
            if me != peer and self.is_member(me) and self.is_member(peer):
                #Increment chat group counter
                self.grp_ever += 1
                #Add chat group to dictionary
                self.chat_grps[self.grp_ever] = [me, peer]
                #Change states
                self.members[me] = S_TALKING
                self.members[peer] = S_TALKING

    #implemented         
    def disconnect(self, me):
        # find myself in the group, quit
        isInGroup, group_key = self.find_group(me)
        # if in group, remove from members and chat groups
        if(isInGroup):
            self.chat_grps[group_key].remove(me)
            #Change user state to alone
            self.members[me] = S_ALONE
            #If one peer left in group, delete group and change state
            if(len(self.chat_grps[group_key]) == 1):
                lastmember = self.chat_grps[group_key][0]
                self.members[lastmember] = S_ALONE
                del self.chat_grps[group_key]
        return None
        
    def list_all(self):
        # a simple minded implementation
        full_list = "Users: ------------" + "\n"
        full_list += str(self.members) + "\n"
        full_list += "Groups: -----------" + "\n"
        full_list += str(self.chat_grps) + "\n"
        return full_list

    #implement
    def list_me(self, me):
        # return a list, "me" followed by other peers in my group
        my_list = []
        isInGroup, group_key = self.find_group(me)
        if(isInGroup):
            my_list = self.chat_grps[group_key][:]
            my_index = my_list.index(me)
            #Rearrange to put "me" first in list
            my_list[my_index],my_list[0] = my_list[0],my_list[my_index]
        return my_list

if __name__ == "__main__":
    g = Group()
    g.join('a')
    g.join('b')
    g.join('c')
    g.join('d')
    
    g.connect('a','b')
    g.connect('c','b')
    print(g.list_all())
    print(g.list_me('c'))
    print(g.find_group('c'))
    g.leave('c')
    print(g.list_all())