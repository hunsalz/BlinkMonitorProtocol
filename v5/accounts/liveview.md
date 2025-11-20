## Liveview

Ask for a live video stream of the given camera

`POST /api/v5/accounts/{AccountID}/networks/{NetworkID}/cameras/{CameraID}/liveview`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.
- **Content-Type** - `application/json` - Required for request body

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Request Body
- **intent** - `liveview`
- **motion_event_start_time** - empty string = immediate?

### Response
A command object containing a Real Time Streaming Protocol (RTSP) URL and connection details. The `server` field contains the RTSP URL, and `liveview_token` is required for authentication when connecting to the stream. 

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request POST \
  --url "https://rest-{region}.immedia-semi.com/api/v5/accounts/{AccountID}/networks/{NetworkID}/cameras/{CameraID}/liveview" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{"intent":"liveview","motion_event_start_time":""}'
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
  --header "User-Agent: Blink" \
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
  --url "https://rest-${HOST}/api/v5/accounts/${ACCOUNT_ID}/networks/${NETWORK_ID}/cameras/${CAMERA_ID}/liveview" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{"intent":"liveview","motion_event_start_time":""}'
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.

### Example Response
`200 OK`

```javascript
{
  "command_id": 1234567890,
  "join_available": true,
  "join_state": "available",
  "server": "immis://<IP>:<PORT>/<PATH>?client_id=<ID>",
  "duration": null,
  "extended_duration": 5400,
  "continue_interval": 30,
  "continue_warning": 10,
  "polling_interval": 15,
  "submit_logs": true,
  "new_command": true,
  "media_id": null,
  "options": {},
  "liveview_token": "<TOKEN>"
}
```

**Note:** The `server` field contains an RTSP URL (using `immis://` protocol) that can be used to stream live video from the camera. The `liveview_token` is required for authentication when connecting to the stream.

