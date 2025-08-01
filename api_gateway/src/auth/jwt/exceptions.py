class JwtTokenException(Exception):
    pass


class NoJwtTokenException(Exception):
    def __str__(self):
        return 'Token missing'