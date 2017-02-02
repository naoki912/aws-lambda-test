import os
import re
import uuid
import json

import boto3


def lambda_handler(event, context):
    # urlPrefix = os.environ['URL_PREFIX']
    BUCKET = os.environ['BUCKET']

    s3 = boto3.client('s3')

    pattern = r".*(\.|\/)(gif|jpe?g|png)$"

    if not event['body-json'].has_key('contentType'):
        raise Exception
    elif not re.match(pattern, event['body-json']['contentType'], re.IGNORECASE):
        raise Exception

    key = str(uuid.uuid4())

    presigned_url = s3.generate_presigned_url(
        ClientMethod='put_object',
        Params={'Bucket': BUCKET, 'Key': key, 'ContentType': event['body-json']['contentType']},
        ExpiresIn=3600,
        HttpMethod='PUT'
    )

    # return json.dumps({'oneTimeUploadUrl': presigned_url, 'item': { 'key': key, }, 'resultUrl': urlPrefix + key})
    body = {
        'oneTimeUploadUrl': presigned_url,
        'item': {
            'key': key,
        }
    }

    return json.dumps(body)
