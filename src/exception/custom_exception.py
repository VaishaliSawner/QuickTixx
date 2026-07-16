class UserAlreadyExistsException(Exception):
    def __init__(self,message="User Already exists"):
         self.message=message



class InvalidLoginException(Exception):
    def __init__(self,message="Invalid email or password"):
        self.message=message


class MovieNotFoundException(Exception):
    def __init__(self,message="Movie not found"):
        self.message=message

class BookingNotFoundException(Exception):
    def __init__(self,message="Booking not found"):
        self.message=message


class UnauthorizedAccessException(Exception):
    def __init__(self,message="Unauthorized Access"):
        self.message=message

