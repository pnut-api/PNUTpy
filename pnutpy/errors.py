
class PnutError(Exception):
    pass


class PnutAPIException(PnutError):
    def __init__(self, api_response):
        super(PnutAPIException, self).__init__(api_response.meta.error_message)
        self.response = api_response
        self.error_id = api_response.meta.get('error_id')
        self.error_slug = api_response.meta.get('error_slug')

    def __str__(self):
        return "%s error_id: %s error_slug: %s" % (super(PnutAPIException, self).__str__(), self.error_id, self.error_slug)


class PnutBadRequestAPIException(PnutAPIException):
    def __init__(self, response):
        response.meta.error_message = response.meta.error_message.replace('Bad Request: ', '')
        super(PnutBadRequestAPIException, self).__init__(response)


class PnutAuthAPIException(PnutAPIException):
    pass


class PnutRateLimitAPIException(PnutAPIException):
    pass


class PnutInsufficientStorageException(PnutAPIException):
    pass


class PnutPermissionDenied(PnutAPIException):
    pass


class PnutMissing(PnutAPIException):
    pass
