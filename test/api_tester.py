import json
import os

import requests


API_GATEWAY_URL = ''

IMAGE_NAME = 'aws.png'
IMAGE_PATH = os.path.join(os.path.curdir, IMAGE_NAME)


def get_pre_signed_url() -> (str, dict):
    print('=== Get PreSigned URL ===')

    res = requests.post(
        url=API_GATEWAY_URL + '/image',
        data=json.dumps({'contentType': 'image/png'}),
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    )

    if not res.status_code == 200:
        print(res.status_code)
        raise Exception

    body = json.loads(res.text)

    return body['oneTimeUploadUrl'], body['item']


def put_image(pre_signed_url: str) -> None:
    print('=== Image Upload ===')

    file = open(IMAGE_PATH, 'rb')

    res = requests.put(
        url=pre_signed_url,
        data=file,
        headers={
            'Accept': 'image/png',
            'Content-Type': 'image/png'
        }
    )

    file.close()

    if not res.status_code == 200:
        print(res.status_code)
        raise Exception


def post_image_info(image_info: dict) -> str:
    print('=== Register Image Info ===')

    res = requests.post(
        url=API_GATEWAY_URL + '/image/{uuid}/info'.format(uuid=image_info['key']),
        data=json.dumps({
            'key': image_info['key'],
            'user': {
                'name': 'test user',
                'mail': 'example@example.org',
            },
        }),
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    )

    if not res.status_code == 200:
        print(res.status_code)
        raise Exception

    return res.text


def main():
    pre_signed_url, upload_image_info = get_pre_signed_url()
    print(pre_signed_url)

    put_image(pre_signed_url=pre_signed_url)
    print('uploaded !')

    body = post_image_info(image_info=upload_image_info)
    print(body)


if __name__ == '__main__':
    main()
