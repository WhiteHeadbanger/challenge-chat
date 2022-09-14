#import sqlalchemy si se desea persistencia y modificar la clase. Luego crear un user_controller con todos los metodos.
import json

class User:

    def __init__(self, nickname) -> None:
        """ Represents a user """

        self.nickname = nickname
        self.friend_list = []
        self.friend_requests = []
        self.groups = []
        self.messages = []

    def receive_friend_request(self, data) -> None:
        """ Receives a friend request from <nickname> """

        # Check if exists a previous friend request from user
        req = [r for r in self.friend_requests if r["from"] == data["from"]]
        if not req:
            self.friend_requests.append(data)

    def add_friend(self, nickname: str) -> None:
        """ Adds <nickname> to friend list """

        self.friend_list.append(nickname)

    def remove_friend(self, nickname: str) -> None:
        """ Removes <nickname> from friend list """

        self.friend_list.remove(nickname)

    def in_friendlist(self, nickname: str) -> bool:
        """ Returns true if nickname in friendlist """
        
        if nickname in self.friend_list:
            return True
        return False

    def in_group(self, groupname: str) -> bool:
        """ Returns true if groupname in groups list"""

        if groupname in self.groups:
            return True
        return False
        
    def add_group(self, groupname: str) -> None:
        """ Adds a group to the list of groups """

        self.groups.append(groupname)

    def get_private_messages(self):
        return self.messages
