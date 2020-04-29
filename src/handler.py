import logging

import tornado.web
import tornado.escape


class Handler(tornado.web.RequestHandler):
    # available commands
    CMD = {}

    def post(self):
        try:
            logging.debug("Got request: %s" % self.request.body)
            update = tornado.escape.json_decode(self.request.body)
            message = update['message']
            text = message.get('text')
            if text:
                logging.info("MESSAGE\t%s\t%s" % (message['chat']['id'], text))

                if text[0] == '/':
                    command, *arguments = text.split(" ", 1)
                    try:
                        response = self.CMD.get(command)(arguments, message)
                    except KeyError:
                        response = self.help_message(arguments, message)
                    logging.info("REPLY\t%s\t%s" % (message['chat']['id'], response))
                    from src.core import send_reply
                    send_reply(response)
        except Exception as e:
            logging.warning(str(e))

    def help_message(self, arguments, message):
        response = {'chat_id': message['chat']['id']}
        result = ["Hey, %s!" % message["from"].get("first_name"),
                  "\rI can accept only these commands:"]
        for command in self.CMD:
            result.append(command)
        response['text'] = "\n\t".join(result)
        return response
