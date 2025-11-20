## Get Video

Download a video clip by filename. The filename is obtained from the [Get Video Events](getVideoEvents.md) API response.

`GET /api/v2/accounts/{AccountID}/media/clip/{mp4_Filename}`

### Headers
- **TOKEN_AUTH** -  session auth token


### Response
`content-type: video/mp4`

The response is a binary MP4 video file stream.


### Example Request
```sh
curl --request GET \
  --url https://rest-prod.immedia-semi.com/api/v2/accounts/1234/media/clip/mediavideoname.mp4 \
  --header 'TOKEN_AUTH: {AuthToken}' \
  --output video.mp4
```


### Example Response
`200 OK`

Binary MP4 video file stream.

**Note:** The video filename is obtained from the `media` field in the response from [Get Video Events](getVideoEvents.md). The path format is typically `/api/v2/accounts/{AccountID}/media/clip/{filename}.mp4`.

