## Update Camera Config

Update the configuration for the given camera.

`POST /network/{NetworkID}/camera/{CameraID}/update`

### Headers
- **TOKEN_AUTH** -  session auth token
- **Content-Type** - `application/json`

### Body
- **name** - (optional) Camera name
- **motion_enabled** - (optional) Enable/disable motion detection
- Other camera configuration fields as needed

### Response
A command object. See example. This call is asynchronous and is monitored by the [Command Status](../network/command.md) API call using the returned Command Id.


### Example Request
```sh
curl --request POST \
  --url https://rest-prod.immedia-semi.com/network/189117/camera/193210/update \
  --header 'TOKEN_AUTH: {AuthToken}' \
  --header 'Content-Type: application/json' \
  --data '{"name": "Updated Camera Name", "motion_enabled": true}'
```


### Example Response
`200 OK`

```javascript
{
  "id": 123456789,
  "created_at": "2025-01-19T22:20:16+00:00",
  "updated_at": "2025-01-19T22:20:16+00:00",
  "execute_time": "2025-01-19T22:20:16+00:00",
  "command": "config_update",
  "state_stage": "rest",
  "stage_rest": "2025-01-19T22:20:16+00:00",
  "state_condition": "new",
  "target": "camera",
  "target_id": 193210,
  "camera_id": 193210,
  "network_id": 189117,
  "account_id": 1234,
  "sync_module_id": 123456
}
```

