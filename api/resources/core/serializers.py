class BaseSerializer:
    """
    All validate methods should start with _validate.

    They should return nothing or throw Falcon HTTP exception when validation
    fail.
    """

    def validate(self):
        validate_methods = [
            getattr(self, func) for func in dir(self)
            if callable(getattr(self, func)) and func.startswith("_validate")
        ]
        for method in validate_methods:
            method()
