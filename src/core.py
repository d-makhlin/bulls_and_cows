import logging
import signal
import requests
import tornado.web
import tornado.ioloop

from src.handler import Handler

BOT_TOKEN = '1126940255:AAGXar8Z0FYnzWRGNrjHsRY50vJbx08OA-c'
URL = "https://api.telegram.org/bot%s/" % BOT_TOKEN
HookURL = ""

api = requests.Session()
application = tornado.web.Application([
    (r"/", Handler),
])


def send_reply(response):
    if 'text' in response:
        api.post(URL + "sendMessage", data=response)


def signal_term_handler(signum, frame):
    pass


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, signal_term_handler)
    try:
        set_hook = api.get(URL + "setWebhook?url=%s" % HookURL)
        if set_hook.status_code != 200:
            logging.error("Can't set hook: %s. Quit." % set_hook.text)
            exit(1)
        application.listen(8888)
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        signal_term_handler(signal.SIGTERM, None)
