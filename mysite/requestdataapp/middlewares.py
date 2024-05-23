import time

from django.http import HttpRequest, HttpResponseForbidden


# class ThrottlingMiddleware:
#     THROTTLE_DELAY = 30
#
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.last_request = {}
#
#     def __call__(self, request: HttpRequest):
#         ip_address = request.META["REMOTE_ADDR"]
#         current_time = time.time()
#
#         if ip_address in self.last_request:
#             if current_time - self.last_request[ip_address] < self.THROTTLE_DELAY:
#                 return HttpResponseForbidden("Exception: to many requests!")
#
#         self.last_request[ip_address] = current_time
#         response = self.get_response(request)
#
#         return response



def set_useragent_on_request_middleware(get_response):

    #print('initial call')

    def middleware(request: HttpRequest):
        #rint('before get_response')
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        #print('after get_response')
        return response

    return middleware


class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        #print('requests_count:', self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        #print('response_count:', self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        #print(f'got {self.exceptions_count} exceptions so far')


