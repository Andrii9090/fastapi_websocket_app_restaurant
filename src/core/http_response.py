class CustomResponse:

    @staticmethod
    def ok(data: dict | list | str = None, msg: str = None) -> dict:
        response = {
            'status': 'success',
            'data': data,
            'msg': msg
        }
        return response

    @staticmethod
    def error(error: str) -> dict:
        response = {
            'status': 'error',
            'error': error
        }
        return response

    @staticmethod
    def unauthorized() -> dict:
        response = {
            'status': 'error',
            'error': 'Unauthorized'
        }
        return response
