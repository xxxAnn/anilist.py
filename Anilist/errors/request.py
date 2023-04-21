class RequestError(Exception):
    
    def __init__(self, message: str, code: int, locations: list[tuple[int, int]]):
        super().__init__()

        self._message = message
        self._code = code
        self._line = locations[0][0]
        self._column = locations[0][1]

    def __str__(self):
        return f"API Request returned error with code {self._code}. Error at line {self._line}, column {self._column}: '{self._message}' Use DEBUG logging level to view the query."

    @classmethod
    def from_json(cls, json_obj):
        vars = [json_obj["message"], json_obj["status"], [(i["line"], i["column"]) for i in json_obj["locations"]]]
        if "validation" not in json_obj:
            return cls(*vars)
        return MutationRequestError(json_obj["validation"], *vars)

class MutationRequestError(RequestError):
    
    def __init__(self, validation, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._validation = validation
