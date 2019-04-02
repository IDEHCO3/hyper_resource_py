class HyperRouter():
    def db_for_read(self, model, **hints):
        if model._meta.app_label in ["user_management"]:
            return "user_management"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in ["user_management"]:
            return "user_management"
        return None