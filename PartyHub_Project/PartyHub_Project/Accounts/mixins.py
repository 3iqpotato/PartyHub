class RemoveHelpTextMixin:
    """
    Mixin that removes help_text from forms
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None