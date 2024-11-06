from django.core.exceptions import ValidationError


class MaxSizeValidator():
    def __init__(self, size=5, message=None):
        self.__message = message
        self.size = size

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if value is None:
            self.__message = f"File size must not be over {self.size}MB"
        else:
            self.__message = value

    def mb_to_bytes(self):
        return self.size * 1024 * 1024

    def __call__(self, value):
        if value.size > self.mb_to_bytes():
            raise ValidationError(self.message if self.message else f"File size too big max size {self.size}MB")
