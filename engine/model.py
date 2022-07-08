from winreg import QueryInfoKey


class Integration:
    def __init__(self, query: str, parameters: dict) -> None:
        self.query = query
        self.parameters = parameters
