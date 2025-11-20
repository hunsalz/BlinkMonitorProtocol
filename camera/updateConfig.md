## Update Camera Config

Update the configuration for the given camera.

`POST /network/{NetworkID}/camera/{CameraID}/update`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.
- **Content-Type** - `application/json` - Required for request body

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Request Body
- **name** - (optional) Camera name
- **motion_enabled** - (optional) Enable/disable motion detection
- Other camera configuration fields as needed

### Response
A command object. See example. This call is asynchronous and is monitored by the [Command Status](../network/command.md) API call using the returned Command Id.


### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request POST \
  --url "https://rest-{region}.immedia-semi.com/network/{NetworkID}/camera/{CameraID}/update" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{"name": "Updated Camera Name", "motion_enabled": true}'
```

**Complete working example using .env file:**
```sh
source .env && \
REFRESH_TOKEN=$(echo "$BLINK_TOKENS" | sed -n "s/.*refresh_token=\([^|]*\).*/\1/p") && \
CLIENT_ID=$(echo "$BLINK_TOKENS" | sed -n "s/.*client_id=\([^|]*\).*/\1/p") && \
HOST=$(echo "$BLINK_TOKENS" | sed -n "s/.*host=\([^|]*\).*/\1/p") && \
ACCOUNT_ID=$(echo "$BLINK_TOKENS" | sed -n "s/.*account_id=\([^|]*\).*/\1/p") && \
TOKEN_RESPONSE=$(curl -s --request POST --url "https://api.oauth.blink.com/oauth/token" \
  --header "Content-Type: application/x-www-form-urlencoded" \
  --header "User-Agent: Blinkpy" \
  --data-urlencode "grant_type=refresh_token" \
  --data-urlencode "refresh_token=$REFRESH_TOKEN" \
  --data-urlencode "client_id=${CLIENT_ID:-android}" \
  --data-urlencode "scope=client") && \
NEW_TOKEN=$(echo "$TOKEN_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4) && \
HOMESCREEN=$(curl -s --request GET \
  --url "https://rest-${HOST}/api/v3/accounts/${ACCOUNT_ID}/homescreen" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json") && \
NETWORK_ID=$(echo "$HOMESCREEN" | grep -o '"networks":\[{"id":[0-9]*' | grep -o '[0-9]*$' | head -1) && \
CAMERA_ID=$(echo "$HOMESCREEN" | grep -o '"cameras":\[{"id":[0-9]*' | grep -o '[0-9]*$' | head -1) && \
curl --request POST \
  --url "https://rest-${HOST}/network/${NETWORK_ID}/camera/${CAMERA_ID}/update" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{"name": "Updated Camera Name", "motion_enabled": true}'
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.


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

