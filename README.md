lambda
===============

## API Design

### API Gateway
- Note
  - `ContentType` はすべて `application/json`
  - `{key}` == UUID

#### 実装済み

- POST /image (`{ contentType: image/(gif|jpe?g|png) }`) -> `{"OneTimeUploadUrl": "...}`
  - lambda: get_presigned_url
  - mapping template
    - Content-Type: [application/json]
    - メソッドリクエストのパススルー
  - TODO: uuidがすでに使われていないか確認する
  - Example request body
    ```json
    {
      "contentType": "image/png"
    }
    ```
  - Example response body
    ```json
    {
      "oneTimeUploadUrl": "{OneTimeUploadURL}",
      "item": {
        "key": "{key}",
      }
    }
    ```

- POST /image/{key}/info (`{"key": "...}`) -> `{"ID": "...}`
  - lambda: register_image_info
  - mapping template
    - Content-Type: [application/json]
    - メソッドリクエストのパススルー
  - Example request body
    ```json
    {
      "key": "3abc0602-3f85-410f-a2b0-c271e02dbe06",
      "user": {
        "name": "user name",
        "mail": "example@example.com"
      }
    }
    ```
  - Example response body
    ```json
    {
      "ID": "3abc0602-3f85-410f-a2b0-c271e02dbe06",
      "Image": {
        "Name": "3abc0602-3f85-410f-a2b0-c271e02dbe06"
      },
      "User": {
        "Mail": "example@example.org",
        "Name": "user name"
      }
    }
    ```
  - TODO: keyは{key}から取得する

#### 未実装

- GET /image/{key} (`None`) -> ImageBinary
  - lambda:
  - mapping template
    - Content-Type: []
    - メソッドリクエストのパススルー

- PUT /image/{key} (ImageBinary) -> `None`
  - lambda:
  - mapping template
    - Content-Type: [image/png, image/jpe?g, image/png]
    - メソッドリクエストのパススルー

#### `OneTimeUploadURL` (S3)

- PUT {OneTimeUploadURL} -> `None`
  - S3 Bucket: images

{OneTimeUploadURL} にアップロードが成功した場合に /image/{uuid} にメタデータをPUT

---

## Webフロントで画像をアップロードするまでの流れ

```
POST /image (`{ contentType: image/(gif|jp?g|png) }`) -> `OneTimeUploadURL`
PUT {OneTimeUploadURL} (Image) -> `None`
POST /image/{key}/info (`{"key": "...}`) -> `{"ID": "...}`
```

## Roles

- `lambda_get_signed_url`
  - lambda: get_presigned_url
  - s3の一時アクセスURLを生成するためのロール
- `lambda_register_image_info`
  - lambda: register_image_info
  - inline policy
    - dynamodb_ImageMetadata_GET_PUT
      - DynamoDB(ImageMetadata)に対して PUT, GET を行う

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PutUpdateDeleteOnBooks",
      "Effect": "Allow",
      "Action": [
        "dynamodb:PutItem",
        "dynamodb:GetItem"
      ],
      "Resource": "arn:aws:dynamodb:ap-northeast-1:000000000000:table/ImageMetadata"
    }
  ]
}
```

## lambda

- `get_presigned_url`
  - file: lambdas/get_presigned_url.py
- `register_image_info`
  - file: lambdas/register_image_information.py

## DynamoDB
* TableName: ImageMetadata
* Primary Key: ID
* schema:
```
{
  ID: UUID,
  Image: {
    Name: UUID
  },
  User: {
    Name: String,
    Mail: String
  }
}
```
