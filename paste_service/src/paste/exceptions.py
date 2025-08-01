class PasteException(Exception):
    pass


class PasteNotFoundException(PasteException):
    def __str__(self):
        return 'Paste not found'
    

class PublicUrlAlreadyExistsException(PasteException):
    def __str__(self):
        return 'Public url already exists'