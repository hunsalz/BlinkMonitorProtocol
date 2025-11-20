## Record Video Clip from Camera

Record a video clip from the camera.  Is this still used in the client?

`POST /network/{NetworkID}/camera/{CameraID}/clip`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.


### Response
A command object or error response. See example. This call is asynchronous and is monitored by the [Command Status](../network/command.md) API call using the returned Command Id.

**Error Responses:**
- `{"message":"System is busy, please wait","error":null,"code":307}` - The system is currently busy processing another request. Wait a few seconds and retry the request.

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request POST \
  --url "https://rest-{region}.immedia-semi.com/network/{NetworkID}/camera/{CameraID}/clip" \
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
  --url "https://rest-${HOST}/network/${NETWORK_ID}/camera/${CAMERA_ID}/clip" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json"
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.

### Example Response

**Success Response:**
`200 OK`

```javascript
{
  "id": 1234567890,
  "created_at": "2020-08-23T11:29:35+00:00",
  "updated_at": "2020-08-23T11:29:35+00:00",
  "execute_time": "2020-08-23T11:29:35+00:00",
  "command": "clip",
  "state_stage": "rest",
  "stage_rest": "2020-08-23T11:29:35+00:00",
  "stage_cs_db": null,
  "stage_cs_sent": null,
  "stage_sm": null,
  "stage_dev": null,
  "stage_is": null,
  "stage_lv": null,
  "stage_vs": null,
  "state_condition": "new",
  "sm_ack": null,
  "lfr_ack": null,
  "sequence": null,
  "attempts": 0,
  "transaction": "aTransactionID",
  "player_transaction": "aPlayerTransactinoId",
  "server": null,
  "duration": null,
  "by_whom": " - 6.0.13 (8528) #df463ac0",
  "diagnostic": false,
  "debug": "",
  "opts_1": 0,
  "target": null,
  "target_id": null,
  "parent_command_id": null,
  "camera_id": 123456,
  "siren_id": null,
  "firmware_id": null,
  "network_id": 1234,
  "account_id": 1234,
  "sync_module_id": 123456
}
```

**Error Response:**
`307 Temporary Redirect` (or `200 OK` with error in body)

```javascript
{
  "message": "System is busy, please wait",
  "error": null,
  "code": 307
}
```