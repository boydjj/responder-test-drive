import logging

import responder

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

api = responder.API()


@api.route('/get')
def echo(req, resp):
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
        logger.info(f'{k}, {v}')
        headers[k.title()] = v

    if req.headers:
        response['headers'] = headers

    resp.media = response


if __name__ == '__main__':
    logger.info('Kicking off new app...')
    api.run()
