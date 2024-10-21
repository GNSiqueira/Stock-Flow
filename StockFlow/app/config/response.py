class Response:
    def __init__(self, code, msg, data):
        self.__code = code
        self.__msg = msg
        self.__data = data

    @property
    def code(self):
        return self.__code

    @property
    def msg(self):
        return self.__msg

    @property
    def data(self):
        return self.__data
