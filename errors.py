class AntiScriptError(Exception):

    def __init__(
        self,
        message,
        line=None
    ):
        self.message = message
        self.line = line

    def __str__(self):

        if self.line:

            return (
                "\n"
                "AntiScript Error\n"
                f"Line {self.line}\n\n"
                f"{self.message}"
            )

        return self.message