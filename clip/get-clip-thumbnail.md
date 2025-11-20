## Get Video Thumbnail

Retrieve the JPEG thumbnail for a video clip. The thumbnail filename is obtained from the [Get Clip Events](get-clip-events.md) API response.

`GET /api/v2/accounts/{AccountID}/media/thumb/{jpg_filename}`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Response
`content-type: image/jpeg`

The response is a binary JPEG image file stream.

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request GET \
  --url "https://rest-{region}.immedia-semi.com/api/v2/accounts/{AccountID}/media/thumb/{jpg_filename}" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" \
  --output thumbnail.jpg
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
CLIP_EVENTS=$(curl -s --request GET \
  --url "https://rest-${HOST}/api/v1/accounts/${ACCOUNT_ID}/media/changed?since=1970-01-01T00:00:00+0000&page=1" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json") && \
THUMBNAIL_PATH=$(echo "$CLIP_EVENTS" | grep -o '"thumbnail":"[^"]*' | head -1 | cut -d'"' -f4) && \
if [ -z "$THUMBNAIL_PATH" ]; then \
  echo "Warning: No thumbnail found in clip events."; \
else \
  THUMBNAIL_FILE=$(basename "$THUMBNAIL_PATH").jpg && \
  curl --request GET \
    --url "https://rest-${HOST}${THUMBNAIL_PATH}" \
    --header "Authorization: Bearer $NEW_TOKEN" \
    --header "Content-Type: application/json" \
    --output "$THUMBNAIL_FILE"; \
fi
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.

### Example Response
`200 OK`

Binary JPEG image file stream.

**Note:** The thumbnail filename is obtained from the `thumbnail` field in the response from [Get Clip Events](get-clip-events.md). The path format is typically `/api/v2/accounts/{AccountID}/media/thumb/{filename}.jpg`.

