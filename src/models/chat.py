class Chat:
    """ Handles all instanced users and rooms """

    _instance = None
    
    nicknames = []
    users = []
    rooms = []

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def add_user(cls, user):
        cls.users.append(user)
        cls.nicknames.append(user.nickname)

    def remove_user(cls, user):
        cls.users.remove(user)
        cls.nicknames.remove(user.nickname)

    def add_room(cls, room):
        cls.rooms.append(room)
    
    def user_exists(cls, username):
        if username in cls.nicknames:
            return True
        return False

    def get_user(cls, username):
        user = None
        for u in cls.users:
            if u.nickname == username:
                user = u
                break
    
        return user

    def get_room(cls, room_name):
        room = None
        for r in cls.rooms:
            if r.name == room_name:
                room = r
                break
        return room
