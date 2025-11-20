## Get Account Notification Flags

`GET /api/v1/accounts/{AccountID}/notifications/configuration`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Response
Flag status for various notifications. See example.

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request GET \
  --url "https://rest-{region}.immedia-semi.com/api/v1/accounts/{AccountID}/notifications/configuration" \
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
curl --request GET \
  --url "https://rest-${HOST}/api/v1/accounts/${ACCOUNT_ID}/notifications/configuration" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json"
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.


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
    "battery_dead": true,
    "local_storage": true,
    "accessory_connected": true,
    "accessory_disconnected": true,
    "accessory_low_battery": true,
    "general": true,
    "cv_motion": true
  }
}
```

**Notes:**
- The response includes various notification flags that control which events trigger push notifications
- **Common fields** (typically present): `motion`, `camera_offline`, `low_battery`, `sync_module_offline`, `general`
- **Feature-specific fields** (may vary): 
  - `doorbell` - Only present if doorbell devices are configured
  - `cv_motion` - Only present if computer vision features are enabled
  - `accessory_connected`, `accessory_disconnected`, `accessory_low_battery` - Only present if accessories are configured
  - `local_storage` - Only present if local storage features are available
- The exact fields may vary based on:
  - Account type and subscription tier
  - Available features and device types
  - Regional feature availability