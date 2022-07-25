from django.db import models


class DateTimeWithoutTZField(models.DateTimeField):
    def db_type(self, connection):
        return 'timestamp'


class AutoUUIDField(models.UUIDField):
    def db_type(self, connection):
        return 'uuid DEFAULT uuid_generate_v4()'

    def rel_db_type(self, connection):
        return 'uuid'
