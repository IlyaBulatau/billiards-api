class BadRequestError(Exception):
    msg: str | None = None

    def __init__(self, msg: str | None = None):
        self.msg = msg or self.msg or ""
