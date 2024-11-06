class RemoveHelpTextMixin:
    """
    Миксин, който премахва помощния текст от полетата на формата.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None