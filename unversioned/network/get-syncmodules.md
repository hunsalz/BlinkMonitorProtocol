## Get Network Sync Modules

Get detailed information about sync modules in a network.

`GET /network/{NetworkID}/syncmodules`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Response
A sync module object containing detailed information:
- **id** - Sync module ID
- **created_at** - Creation timestamp
- **updated_at** - Last update timestamp
- **last_activity** - Last activity timestamp
- **name** - Sync module name
- **fw_version** - Firmware version
- **mac_address** - MAC address (may be null)
- **ip_address** - IP address
- **lfr_frequency** - LFR frequency (may be null)
- **serial** - Serial number
- **status** - Status (e.g., "online", "offline")
- **onboarded** - Whether the sync module is onboarded
- **server** - Server identifier
- **last_hb** - Last heartbeat timestamp
- **os_version** - OS version
- **last_wifi_alert** - Last WiFi alert timestamp (may be null)
- **wifi_alert_count** - WiFi alert count
- **last_offline_alert** - Last offline alert timestamp (may be null)
- **offline_alert_count** - Offline alert count
- **table_update_sequence** - Table update sequence number
- **local_storage_enabled** - Whether local storage is enabled
- **last_backup_started** - Last backup start timestamp
- **last_backup_completed** - Last backup completion timestamp
- **last_backfill_completed** - Last backfill completion timestamp
- **backfill_in_progress** - Backfill in progress status (may be null)
- **ring_device_id** - Ring device ID (may be null)
- **first_boot** - First boot timestamp
- **feature_plan_id** - Feature plan ID (may be null)
- **account_id** - Account ID
- **network_id** - Network ID
- **country_id** - Country ID
- **vo9_channel** - VO9 channel number
- **wifi_strength** - WiFi signal strength (0-5)

**Note:** This endpoint returns a single sync module object, not an array. If multiple sync modules exist, you may need to call this endpoint multiple times or use the homescreen endpoint to get all sync modules.

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request GET \
  --url "https://rest-{region}.immedia-semi.com/network/{NetworkID}/syncmodules" \
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
  --url "https://rest-${HOST}/network/${NETWORK_ID}/syncmodules" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" | jq
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.

### Example Response
`200 OK`

```javascript
{
  "syncmodule": {
    "id": 123456,
    "created_at": "2025-02-16T11:20:20+00:00",
    "updated_at": "2025-11-20T21:13:59+00:00",
    "last_activity": "1970-01-01",
    "name": "My Blink Sync Module",
    "fw_version": "16.0.32",
    "mac_address": null,
    "ip_address": "91.45.243.11",
    "lfr_frequency": null,
    "serial": "SERIAL123456789",
    "status": "online",
    "onboarded": true,
    "server": "i-0c03ace7c527ee1f1",
    "last_hb": "2025-11-21T00:31:00+00:00",
    "os_version": "6.16.3",
    "last_wifi_alert": null,
    "wifi_alert_count": 0,
    "last_offline_alert": "2025-11-20T07:57:44+00:00",
    "offline_alert_count": 4,
    "table_update_sequence": 1763673239,
    "local_storage_enabled": false,
    "last_backup_started": "2025-11-20T01:41:15+00:00",
    "last_backup_completed": "2025-11-20T01:41:15+00:00",
    "last_backfill_completed": "2025-11-19T07:01:12+00:00",
    "backfill_in_progress": null,
    "ring_device_id": null,
    "first_boot": "2025-02-16T11:20:20+00:00",
    "feature_plan_id": null,
    "account_id": 123456,
    "network_id": 1234,
    "country_id": "DE",
    "vo9_channel": 0,
    "wifi_strength": 5
  }
}
```

