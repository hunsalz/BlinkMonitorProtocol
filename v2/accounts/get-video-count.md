## Get Video Count

Get the total count of videos stored for the account.

`GET /api/v2/videos/count`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Description
Returns the total count of videos (clips) stored for the account. This is a utility endpoint for getting quick statistics about video storage.

**Note:** This endpoint provides a simple count. For detailed video information, use [Get Clip Events](../v1/accounts/get-clip-events.md).

### Response
Returns video count information. The exact structure may vary, but typically includes:
- **count** - Total number of videos (or similar field)

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request GET \
  --url "https://rest-{region}.immedia-semi.com/api/v2/videos/count" \
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
  --url "https://rest-${HOST}/api/v2/videos/count" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" | jq
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.

### Example Response
`200 OK`

```javascript
{
  "count": 42
}
```

**Note:** The actual response structure may vary. Test with your account to see the exact format.

### See Also
- [Get Clip Events](../v1/accounts/get-clip-events.md) - Get detailed information about video clips
- [Get Camera Usage](../v1/camera/get-usage.md) - Get camera usage statistics

