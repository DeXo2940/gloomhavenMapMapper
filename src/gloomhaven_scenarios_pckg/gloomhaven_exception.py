class GloomhavenException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


class CoordinatesException(GloomhavenException):
    pass


class RequirementException(GloomhavenException):
    pass


class ScenarioException(GloomhavenException):
    pass
