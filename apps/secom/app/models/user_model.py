class UserModel:
    def __init__(
        self,
        username: str,
        name: str,
        email: str,
        role: str,
    ) -> None:
        self.username = username
        self.name = name
        self.email = email
        self.role = role
