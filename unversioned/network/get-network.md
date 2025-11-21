## Get Network Info

Get detailed information about a network.

`GET /network/{NetworkID}`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Response
A network object containing detailed network information:
- **id** - Network ID
- **created_at** - Creation timestamp
- **updated_at** - Last update timestamp
- **deleted_at** - Deletion timestamp (null if not deleted)
- **name** - Network name
- **network_key** - Network key
- **description** - Network description
- **network_origin** - Network origin type
- **locale** - Locale setting
- **time_zone** - Time zone (e.g., "Europe/Berlin")
- **dst** - Daylight saving time enabled
- **ping_interval** - Ping interval in seconds
- **encryption_key** - Encryption key (may be null)
- **armed** - Whether the network is armed
- **autoarm_geo_enable** - Auto-arm based on geolocation enabled
- **autoarm_time_enable** - Auto-arm based on time enabled
- **lv_mode** - Liveview mode (e.g., "relay")
- **lfr_channel** - LFR channel number
- **video_destination** - Video storage destination (e.g., "server")
- **storage_used** - Storage used (bytes)
- **storage_total** - Total storage (bytes)
- **video_count** - Current video count
- **video_history_count** - Video history count
- **sm_backup_enabled** - Sync module backup enabled
- **arm_string** - Arm status string (e.g., "Disarmed", "Armed")
- **busy** - Whether the network is busy
- **camera_error** - Whether there are camera errors
- **sync_module_error** - Whether there are sync module errors

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request GET \
  --url "https://rest-{region}.immedia-semi.com/network/{NetworkID}" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" | jq
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
curl -s --request GET \
  --url "https://rest-${HOST}/network/${NETWORK_ID}" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" | jq
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.

### Example Response
`200 OK`

```javascript
{
  "network": {
    "id": 1234,
    "created_at": "2025-02-16T11:20:07+00:00",
    "updated_at": "2025-11-20T22:56:09+00:00",
    "deleted_at": null,
    "name": "Sync A",
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
    "sync_module_error": false
  }
}
```

