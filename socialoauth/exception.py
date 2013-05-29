# -*- coding: utf-8 -*-

class SocialOAuthException(Exception):
    pass


class SocialConfigError(Exception):
    pass



class SocialAPIError(SocialOAuthException):
    """Occurred when doing API call"""
    def __init__(self, site_name, url, code, error_msg, *args, **kwargs):
        self.site_name = site_name
        self.url = url
        self.code = code
        self.error_msg = error_msg
        SocialOAuthException.__init__(self, error_msg, *args, **kwargs)
