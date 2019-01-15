import sys

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    msg = str(sys.path)
    return [msg.encode()] # python3
