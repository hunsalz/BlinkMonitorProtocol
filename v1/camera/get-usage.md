## Get Camera Usage Statistics

Get camera usage statistics for the account, including liveview and clip recording time.

`GET /api/v1/camera/usage`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Response
A usage statistics object containing:
- **range_days** - Number of days covered by the statistics (typically 7)
- **reference** - Reference usage object:
  - **usage** - Total usage in seconds
- **networks** - Array of network usage objects:
  - **network_id** - Network ID
  - **name** - Network name
  - **cameras** - Array of camera usage objects:
    - **id** - Camera ID
    - **name** - Camera name
    - **usage** - Total usage in seconds
    - **lv_seconds** - Liveview seconds
    - **clip_seconds** - Clip recording seconds

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request GET \
  --url "https://rest-{region}.immedia-semi.com/api/v1/camera/usage" \
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
  --url "https://rest-${HOST}/api/v1/camera/usage" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" | jq
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.

### Example Response
`200 OK`

```javascript
{
  "range_days": 7,
  "reference": {
    "usage": 400
  },
  "networks": [
    {
      "network_id": 1234,
      "name": "Sync A",
      "cameras": [
        {
          "id": 5678,
          "name": "Camera Name",
          "usage": 88,
          "lv_seconds": 88,
          "clip_seconds": 0
        }
      ]
    }
  ]
}
```

