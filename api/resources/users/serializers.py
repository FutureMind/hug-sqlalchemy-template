class UserSerializer:

    fields = ('email', 'location', 'about', 'name')

    def __init__(self, user):
        self.user = user

    def to_dict(self):
        return {
            field: getattr(self.user, field) for field in self.fields
        }

    @property
    def data(self):
        return self.to_dict()
