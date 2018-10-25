import logging

import responder

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

api = responder.API()


@api.route('/{greeting}/{target}')
def greet(req, resp, *, greeting, target):
    logger.info('Inside request handler')
    resp.text = f'{greeting}, {target}!'


if __name__ == '__main__':
    api.run()
