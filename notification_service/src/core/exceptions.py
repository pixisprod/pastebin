class WrongCodeException(Exception):
    def __str__(self):
        return 'Incorrect code'
    

class ChannelNotFoundException(Exception):
    def __str__(self):
        return 'Channel not found'