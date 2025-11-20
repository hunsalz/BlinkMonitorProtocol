## Upload Logs

Upload diagnostic logs to Blink servers. This endpoint is typically used for troubleshooting purposes.

`POST /app/logs/upload`

### Headers
- **TOKEN_AUTH** -  session auth token
- **Content-Type** - `multipart/form-data` or `application/json`

### Body
Log data. The exact format may vary depending on the client implementation.


### Response
See example.


### Example Request
```sh
curl --request POST \
  --url https://rest-prod.immedia-semi.com/app/logs/upload \
  --header 'TOKEN_AUTH: {AuthToken}' \
  --header 'Content-Type: application/json' \
  --data '{"logs": "log data here"}'
```


### Example Response
`200 OK`

```javascript
{
  "message": "Logs uploaded successfully",
  "code": 200,
  "upload_id": "abc123def456"
}
```

**Note:** This endpoint is primarily used by the official Blink mobile apps for diagnostic purposes. The exact request format may vary and is not fully documented in the public API.

