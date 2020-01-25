from tornado.escape import json_encode


class JSON:
    @staticmethod
    def ERROR(error: str):
        return json_encode(dict(status=False, error=error))

    @staticmethod
    def DATA(data):
        return json_encode(dict(status=True, data=data))

    @staticmethod
    def TRUE():
        return json_encode(dict(status=True))

    @staticmethod
    def FALSE():
        return json_encode(dict(status=False))
