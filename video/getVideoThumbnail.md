## Get Video Thumbnail

Retrieve the JPEG thumbnail for a video clip. The thumbnail filename is obtained from the [Get Video Events](getVideoEvents.md) API response.

`GET /api/v2/accounts/{AccountID}/media/thumb/{jpg_filename}`

### Headers
- **TOKEN_AUTH** -  session auth token


### Response
`content-type: image/jpeg`

The response is a binary JPEG image file stream.


### Example Request
```sh
curl --request GET \
  --url https://rest-prod.immedia-semi.com/api/v2/accounts/1234/media/thumb/mediathumbnailname.jpg \
  --header 'TOKEN_AUTH: {AuthToken}' \
  --output thumbnail.jpg
```


### Example Response
`200 OK`

Binary JPEG image file stream.

**Note:** The thumbnail filename is obtained from the `thumbnail` field in the response from [Get Video Events](getVideoEvents.md). The path format is typically `/api/v2/accounts/{AccountID}/media/thumb/{filename}.jpg`.

