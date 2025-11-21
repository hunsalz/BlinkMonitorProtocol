## Get Camera Thumbnail (v3)

Get the thumbnail image for a camera using the v3 media endpoint.

`GET /api/v3/media/accounts/{AccountID}/networks/{NetworkID}/{CameraType}/{CameraID}/thumbnail/thumbnail.jpg`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Parameters
- **AccountID** - Account ID
- **NetworkID** - Network ID
- **CameraType** - Camera type (e.g., "catalina", "white", "xt", "sm2"). This must match the camera's type from the homescreen response.
- **CameraID** - Camera ID

### Query Parameters (Optional)
- **ts** - Timestamp parameter (may be used for cache busting)
- **ext** - Extension parameter

**Note:** The camera type must match exactly. Common camera types include:
- `catalina` - Catalina cameras
- `white` - White cameras
- `xt` - XT cameras
- `sm2` - Sync Module 2 cameras

### Response
Returns a JPEG image (binary data) with `Content-Type: image/jpeg`.

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request GET \
  --url "https://rest-{region}.immedia-semi.com/api/v3/media/accounts/{AccountID}/networks/{NetworkID}/{CameraType}/{CameraID}/thumbnail/thumbnail.jpg" \
  --header "Authorization: Bearer $NEW_TOKEN" \
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
CAMERA_ID=$(echo "$HOMESCREEN" | grep -o '"cameras":\[{"id":[0-9]*' | grep -o '[0-9]*$' | head -1) && \
CAMERA_TYPE=$(echo "$HOMESCREEN" | jq -r '.cameras[0].type' 2>/dev/null || echo "catalina") && \
curl -s --request GET \
  --url "https://rest-${HOST}/api/v3/media/accounts/${ACCOUNT_ID}/networks/${NETWORK_ID}/${CAMERA_TYPE}/${CAMERA_ID}/thumbnail/thumbnail.jpg" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --output "thumbnail_${CAMERA_ID}.jpg" && \
echo "Thumbnail saved to thumbnail_${CAMERA_ID}.jpg"
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.

### Example Response
`200 OK`

Returns a JPEG image file. The response has `Content-Type: image/jpeg`.

**Error Responses:**
- `{"code":1630,"message":"Invalid Device Type"}` - The camera type parameter doesn't match the actual camera type. Use the `type` field from the homescreen response.

### Notes

- This endpoint returns binary image data, not JSON
- The camera type must match the camera's actual type from the homescreen response
- The thumbnail URL is also available in the homescreen response under `cameras[].thumbnail`
- This is an alternative to the v2 thumbnail endpoint (`/api/v2/accounts/{AccountID}/media/thumb/{jpg_filename}`)

