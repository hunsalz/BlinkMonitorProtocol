## List Networks

Get a list of all networks associated with the account.

`GET /networks`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Description
Returns a list of all networks (sync modules) associated with the account. This is an alternative to the homescreen endpoint and provides a simpler view of network information.

**Note:** This endpoint uses an unversioned path structure. For more comprehensive account information including cameras and sync modules, use the [HomeScreen](../v3/accounts/homescreen.md) endpoint.

### Response
Returns a summary and detailed network information:
- **summary** - Object with network IDs as keys, containing:
  - **name** - Network name
  - **onboarded** - Whether the network is onboarded
- **networks** - Array of network objects with detailed information:
  - **id** - Network ID
  - **created_at** - Creation timestamp
  - **updated_at** - Last update timestamp
  - **name** - Network name
  - **network_key** - Network key
  - **description** - Network description
  - **network_origin** - Network origin type
  - **locale** - Locale
  - **time_zone** - Time zone
  - **dst** - Daylight saving time enabled
  - **ping_interval** - Ping interval in seconds
  - **encryption_key** - Encryption key (may be null)
  - **armed** - Whether the network is armed
  - **autoarm_geo_enable** - Auto-arm based on geolocation enabled
  - **autoarm_time_enable** - Auto-arm based on time enabled
  - **lv_mode** - Liveview mode
  - **lfr_channel** - LFR channel number
  - **video_destination** - Video storage destination
  - **storage_used** - Storage used (bytes)
  - **storage_total** - Total storage (bytes)
  - **video_count** - Number of videos
  - **video_history_count** - Video history count
  - **sm_backup_enabled** - Sync module backup enabled
  - **arm_string** - Arm status string (may be null)
  - **busy** - Whether the network is busy
  - **camera_error** - Camera error flag
  - **sync_module_error** - Sync module error flag
  - **feature_plan_id** - Feature plan ID (may be null)
  - **location_id** - Location ID (may be null)
  - **account_id** - Account ID

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request GET \
  --url "https://rest-{region}.immedia-semi.com/networks" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" | jq
```

**Complete working example using .env file:**
```sh
source .env && \
REFRESH_TOKEN=$(echo "$BLINK_TOKENS" | sed -n "s/.*refresh_token=\([^|]*\).*/\1/p") && \
CLIENT_ID=$(echo "$BLINK_TOKENS" | sed -n "s/.*client_id=\([^|]*\).*/\1/p") && \
HOST=$(echo "$BLINK_TOKENS" | sed -n "s/.*host=\([^|]*\).*/\1/p") && \
TOKEN_RESPONSE=$(curl -s --request POST --url "https://api.oauth.blink.com/oauth/token" \
  --header "Content-Type: application/x-www-form-urlencoded" \
  --header "User-Agent: Blink" \
  --data-urlencode "grant_type=refresh_token" \
  --data-urlencode "refresh_token=$REFRESH_TOKEN" \
  --data-urlencode "client_id=${CLIENT_ID:-android}" \
  --data-urlencode "scope=client") && \
NEW_TOKEN=$(echo "$TOKEN_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4) && \
curl -s --request GET \
  --url "https://rest-${HOST}/networks" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" | jq
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.

### Example Response
`200 OK`

```javascript
{
  "summary": {
    "189117": {
      "name": "Test",
      "onboarded": true
    }
  },
  "networks": [
    {
      "id": 189117,
      "created_at": "2025-02-16T11:20:07+00:00",
      "updated_at": "2025-11-21T00:39:07+00:00",
      "name": "Test",
      "network_key": "LdSX83Dx232J-H-W",
      "description": "",
      "network_origin": "normal",
      "locale": "",
      "time_zone": "Europe/Berlin",
      "dst": true,
      "ping_interval": 60,
      "encryption_key": null,
      "armed": true,
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
      "arm_string": null,
      "busy": false,
      "camera_error": false,
      "sync_module_error": false,
      "feature_plan_id": null,
      "location_id": null,
      "account_id": 123456
    }
  ]
}
```

### See Also
- [HomeScreen](../v3/accounts/homescreen.md) - Comprehensive account information including cameras and sync modules
- [Get Network Info](get-network.md) - Get detailed information about a specific network

