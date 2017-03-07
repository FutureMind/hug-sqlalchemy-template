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


class ModelSerializer(BaseSerializer):

    fields = ()

    def to_dict(self, instance):
        return {
            field: getattr(instance, field) for field in self.fields
        }

    def to_list(self, instances):
        return [
            self.to_dict(instance) for instance in instances
        ]
