#import sqlalchemy si se desea persistencia y modificar la clase. Luego crear un room_controller con todos los metodos.

class Room:

    def __init__(self, name: str, creator: str) -> None:
        self.name = name
        self.creator = creator
        self.user_list = []
        self.messages = []

    def add_user(self, nickname):
        """ Adds a nickname to the user list """

        self.user_list.append(nickname)

    def get_messages(self):
        return self.messages
    