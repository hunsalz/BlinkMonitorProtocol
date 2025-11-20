## Set Video Options

Set video-related options for the account.

`POST /api/v1/account/video_options`

### Headers
- **TOKEN_AUTH** -  session auth token
- **Content-Type** - `application/json`

### Body
Video options object. Exact fields may vary. See example.


### Response
See example.


### Example Request
```sh
curl --request POST \
  --url https://rest-prod.immedia-semi.com/api/v1/account/video_options \
  --header 'TOKEN_AUTH: {AuthToken}' \
  --header 'Content-Type: application/json' \
  --data '{"auto_delete_days": 7, "storage": 1}'
```


### Example Response
`200 OK`

```javascript
{
  "message": "Video options updated successfully",
  "code": 200
}
```

**Note:** The exact request body structure and response format may vary. This endpoint is used to configure video storage and deletion settings.

