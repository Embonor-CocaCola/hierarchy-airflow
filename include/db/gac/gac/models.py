from django.db import models


class DateTimeWithoutTZField(models.DateTimeField):
    def db_type(self, connection):
        return 'timestamp'


class UnlimitedCharField(models.CharField):
    def __init__(self, *args, db_collation=None, **kwargs):
        # not a typo: we want to skip CharField.__init__ because that adds the max_length validator
        super(models.CharField, self).__init__(*args, db_collation, **kwargs)
        self.db_collation = db_collation

    def check(self, **kwargs):
        # likewise, want to skip CharField.__check__
        return super(models.CharField, self).check(**kwargs)

    def db_type(self, connection):
        return 'varchar'
