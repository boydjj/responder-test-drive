import logging
import time

import aiohttp
import responder

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

api = responder.API()


@api.route('/get')
class EchoView:
    counter = 0

    def __init__(self):
        logger.info(f'Starting new instance of EchoView, counter={EchoView.counter}')

    @api.background.task
    def increment_counter(self):
        EchoView.counter += 1
        time.sleep(0.06)
        logger.info(f'counter: {EchoView.counter}')

    async def get_my_ip(self):
        async with aiohttp.ClientSession() as session:
            async with session.get('http://ifconfig.co/ip') as resp:
                return await resp.text()

    async def on_get(self, req, resp):
        response = {'url': req.full_url}

        args = {}
        for k, v in req.params.items_list():
            if len(v) == 1:
                args[k] = v[0]
            else:
                args[k] = v

        if args:
            response['args'] = args

        headers = {}

        for k, v in req.headers.items():
            headers[k.title()] = v

        if req.headers:
            response['headers'] = headers

        my_ip = await self.get_my_ip()
        response['my_ip'] = my_ip.strip()
        self.increment_counter()
        resp.media = response

    def __del__(self):
        logger.info(f'Killing instance of EchoView, counter={EchoView.counter}')


if __name__ == '__main__':
    logger.info('Kicking off new app...')
    api.run()
