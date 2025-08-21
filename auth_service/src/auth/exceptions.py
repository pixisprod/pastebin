class UserException(Exception):
    def __str__(self):
        return 'UserException'
    

class UserAlreadyExistsException(UserException):
    def __str__(self):
        return 'User already exists'
    

class UserIncorrectCredentialsException(UserException):
    def __str__(self):
        return 'Incorrect login or password'
    

class UserNotFoundException(UserException):
    def __str__(self):
        return 'User not found'
