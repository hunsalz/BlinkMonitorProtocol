## Get Camera Config

Retrieve the configuration for the given camera.

`GET /network/{NetworkID}/camera/{CameraID}/config`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Response
A camera configuration object. See example.

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request GET \
  --url "https://rest-{region}.immedia-semi.com/network/{NetworkID}/camera/{CameraID}/config" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json"
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
curl --request GET \
  --url "https://rest-${HOST}/network/${NETWORK_ID}/camera/${CAMERA_ID}/config" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json"
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.


### Example Response
`200 OK`

```javascript
{
  "id": 193210,
  "name": "Camera",
  "serial": "SERIAL123456789",
  "fw_version": "10.72",
  "type": "catalina",
  "enabled": true,
  "thumbnail": "/media/production/account/1234/network/189117/camera/193210/clip_name",
  "status": "online",
  "battery": "ok",
  "usage_rate": true,
  "network_id": 189117,
  "issues": [],
  "signals": {
    "lfr": 3,
    "wifi": 5,
    "temp": 71,
    "battery": 3
  },
  "motion_enabled": true,
  "armed": true
}
```

