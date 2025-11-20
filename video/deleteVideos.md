## Delete Videos

Delete one or more video clips from the account.

`POST /api/v1/accounts/{AccountID}/media/delete`

### Headers
- **TOKEN_AUTH** -  session auth token
- **Content-Type** - `application/json`

### Body
- **media_ids** - Array of media IDs to delete. Media IDs are obtained from the [Get Video Events](getVideoEvents.md) API response.


### Response
See example.


### Example Request
```sh
curl --request POST \
  --url https://rest-prod.immedia-semi.com/api/v1/accounts/1234/media/delete \
  --header 'TOKEN_AUTH: {AuthToken}' \
  --header 'Content-Type: application/json' \
  --data '{"media_ids": [1234567890, 1234567891]}'
```


### Example Response
`200 OK`

```javascript
{
  "message": "Videos deleted successfully",
  "code": 200,
  "deleted_count": 2
}
```

**Note:** Media IDs are obtained from the `id` field in the response from [Get Video Events](getVideoEvents.md).

