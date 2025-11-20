## Get Clip Events

Get Media events since the given timestamp in the query parm.

`GET /api/v1/accounts/{AccountID}/media/changed`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Parameters
- **since** - a timestamp to return events since.  e.g. 2020-08-03T16:50:24+0000. The official mobile client seems to use the epoch to return all available events - i.e. 1970-01-01T00:00:00+0000
- **page** - page number for multiple pages of results.

### Response
An object containing an array of media event objects. See example.

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request GET \
  --url "https://rest-{region}.immedia-semi.com/api/v1/accounts/{AccountID}/media/changed?since=2020-07-31T09%3A58%3A14%2B0000&page=1" \
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
curl --request GET \
  --url "https://rest-${HOST}/api/v1/accounts/${ACCOUNT_ID}/media/changed?since=1970-01-01T00:00:00+0000&page=1" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json"
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.


### Example Response
`200 OK`

```javascript
{
  "limit": 500,
  "purge_id": 1234567890,
  "refresh_count": 0,
  "media": [
    {
      "id": 1234567890,
      "created_at": "2020-08-06T01:30:59+00:00",
      "updated_at": "2020-08-06T01:37:12+00:00",
      "deleted": false,
      "device": "camera",
      "device_id": 1234567,
      "device_name": "The Device Name",
      "network_id": 1234,
      "network_name": "The Network Name",
      "type": "video",
      "source": "pir",
      "watched": true,
      "partial": false,
      "thumbnail": "/api/v2/accounts/1234/media/thumb/mediathumbnailname",
      "media": "/api/v2/accounts/1234/media/clip/mediavideoname.mp4",
      "additional_devices": [],
      "time_zone": "America/Chicago"
    }
  ]
}
```

**Note:** If no media events are available, the `media` array will be empty `[]`. The `limit` field indicates the maximum number of results per page (typically 500).

