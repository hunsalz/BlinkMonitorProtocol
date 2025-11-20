## Get Account Nofification Flags

`GET /api/v1/accounts/{AccountID}/notifications/configuration`

### Headers
- **TOKEN_AUTH** -  session auth token


### Response
Flag status for various notifications, see example


### Example Request
```sh
curl --request GET \
  --url https://rest-prod.immedia-semi.com/api/v1/accounts/1234/notifications/configuration \
  --header 'TOKEN_AUTH: {AuthToken}'
```


### Example Response
`200 OK`

```javascript
{
  "notifications": {
    "low_battery": true,
    "camera_offline": true,
    "camera_usage": true,
    "scheduling": true,
    "motion": true,
    "sync_module_offline": true,
    "temperature": true,
    "doorbell": true,
    "wifi": true,
    "lfr": true,
    "bandwidth": true,
    "battery_dead": true
  }
}
```