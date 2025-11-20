## Get Clip

Download a clip by filename. The filename is obtained from the [Get Clip Events](get-clip-events.md) API response.

`GET /api/v2/accounts/{AccountID}/media/clip/{mp4_Filename}`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Response
`content-type: video/mp4`

The response is a binary MP4 clip file stream.

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request GET \
  --url "https://rest-{region}.immedia-semi.com/api/v2/accounts/{AccountID}/media/clip/{mp4_Filename}" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" \
  --output clip.mp4
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
CLIP_EVENTS=$(curl -s --request GET \
  --url "https://rest-${HOST}/api/v1/accounts/${ACCOUNT_ID}/media/changed?since=1970-01-01T00:00:00+0000&page=1" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json") && \
CLIP_PATH=$(echo "$CLIP_EVENTS" | grep -o '"media":"[^"]*' | head -1 | cut -d'"' -f4) && \
if [ -z "$CLIP_PATH" ]; then \
  echo "Warning: No clip found in clip events."; \
else \
  CLIP_FILE=$(basename "$CLIP_PATH") && \
  curl --request GET \
    --url "https://rest-${HOST}${CLIP_PATH}" \
    --header "Authorization: Bearer $NEW_TOKEN" \
    --header "Content-Type: application/json" \
    --output "$CLIP_FILE"; \
fi
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.

### Example Response
`200 OK`

Binary MP4 clip file stream.

**Note:** The clip filename is obtained from the `media` field in the response from [Get Clip Events](get-clip-events.md). The path format is typically `/api/v2/accounts/{AccountID}/media/clip/{filename}.mp4`.

