class AuthRouter:
    ROUTE_APP_LABELS = {'auth', 'contenttypes'}

    # def db_for_read(self, model, **hints):
    #     if model._meta.app_label in self.ROUTE_APP_LABELS:
    #         return 'auth_db'
    #     return None

    # def db_for_write(self, model, **hints):
    #     if model._meta.app_label in self.ROUTE_APP_LABELS:
    #         return 'auth_db'
    #     return None

    # def allow_relation(self, obj1, obj2, **hints):
    #     if obj1._meta.app_label in self.ROUTE_APP_LABELS or \
    #             obj2._meta.app_label in self.ROUTE_APP_LABELS:
    #         return True
    #     return None

    # def allow_migrate(self, db, app_label, model_name=None, **hints):
    #     if app_label in self.ROUTE_APP_LABELS:
    #         return db == 'auth_db'
    #     return None
