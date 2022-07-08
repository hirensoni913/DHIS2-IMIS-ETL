from winreg import QueryInfoKey


class Integration:
    def __init__(self, query: str, parameters: dict, description: str) -> None:
        self.description = description
        self.query = query
        self.parameters = parameters
