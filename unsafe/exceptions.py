class UnknownEncoding(Exception):
    """This Error Raising When You Enter an Unavailable Encoding."""

    def __init__(self, encode: str, message: str = 'Your Encode is Not a Valid Encoding.'):
        self.encode = encode
        self.message = message
        super().__init__(self.encode, self.message)

    def __str__(self):
        return f'{self.message}({self.encode})'

class NotWordpress(Exception):
    """This Error Raising When Your Target Website is Not Built with Wordpess."""

    def __init__(self, url: str, message: str = 'Your Target Website is Not Built with Wordpess.'):
        self.url = url
        self.message = message
        super().__init__(self.url, self.message)

    def __str__(self):
        return f'{self.message}({self.url})'

class SiteNotFound(Exception):
    """This Error Raising When The Program cant Connect to Your Target Website."""

    def __init__(self, url: str, message: str = 'The Program cant Connect to Your Target Website or Entered Domain is Not Found.'):
        self.url = url
        self.message = message
        super().__init__(self.url, self.message)

    def __str__(self):
        return f'{self.message}({self.url})'

class UsersFileNotFound(Exception):
    """This Error Raising When cant Find Users File on Site."""

    def __init__(self, message: str = 'cant Find Users File on Site.'):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'

class NotFoundData(Exception):
    """This Error Raising When cant Find any DATA in Your Proccess."""

    def __init__(self, message: str = 'cant Find any DATA in Your Proccess.'):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'
