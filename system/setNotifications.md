## Set Account Nofification Flags

`POST /api/v1/accounts/{AccountID}/notifications/configuration`

### Headers
- **Content-Type** - `application/json`
- **TOKEN_AUTH** -  session auth token

### Body
- **notification object** - see example request

### Response
see example


### Example Request
```sh
curl --request POST \
  --url https://rest-prod.immedia-semi.com/api/v1/accounts/1234/notifications/configuration \
  --header 'content-type: application/json' \
  --header 'TOKEN_AUTH: {AuthToken}' \
  --data '{
  "notifications": {
    "low_battery": false
  }
}'
```


### Example Response
`200 OK`

```javascript
{
  "message": "Client Notification Configure Update Successful"
}
```