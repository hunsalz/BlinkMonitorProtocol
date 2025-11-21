## Update Network

Update network settings and configuration.

`POST /network/{NetworkID}/update`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.
- **Content-Type** - `application/json` - Required for request body

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Request Body
Network update object. The exact fields that can be updated may vary, but commonly includes:
- **name** - Network name (string)

**Note:** Additional fields may be supported. The API may accept partial updates, updating only the fields provided in the request body.

### Response
Returns the updated network object with the same structure as [Get Network Info](get-network.md).

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request POST \
  --url "https://rest-{region}.immedia-semi.com/network/{NetworkID}/update" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{"name": "My Network Name"}' | jq
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
curl -s --request POST \
  --url "https://rest-${HOST}/network/${NETWORK_ID}/update" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{"name": "My Network Name"}' | jq
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.

### Example Response
`200 OK`

```javascript
{
  "network": {
    "id": 1234,
    "created_at": "2025-02-16T11:20:07+00:00",
    "updated_at": "2025-11-21T00:39:06+00:00",
    "deleted_at": null,
    "name": "My Network Name",
    "network_key": "LdSX83Dx232J-H-W",
    "description": "",
    "network_origin": "normal",
    "locale": "",
    "time_zone": "Europe/Berlin",
    "dst": true,
    "ping_interval": 60,
    "encryption_key": null,
    "armed": false,
    "autoarm_geo_enable": false,
    "autoarm_time_enable": false,
    "lv_mode": "relay",
    "lfr_channel": 0,
    "video_destination": "server",
    "storage_used": 0,
    "storage_total": 0,
    "video_count": 0,
    "video_history_count": 4000,
    "sm_backup_enabled": true,
    "arm_string": "Disarmed",
    "busy": false,
    "camera_error": false,
    "sync_module_error": false,
    "feature_plan_id": null,
    "location_id": null,
    "account_id": 123456,
    "lv_save": false
  }
}
```

**Note:** The response includes the complete updated network object. The `updated_at` timestamp will reflect the time of the update.

