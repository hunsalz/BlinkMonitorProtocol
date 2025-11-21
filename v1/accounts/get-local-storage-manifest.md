## Get Local Storage Manifest

Retrieve the manifest of video clips stored in sync module local storage.

`GET /api/v1/accounts/{AccountID}/networks/{NetworkID}/sync_modules/{SyncID}/local_storage/manifest/request/{ManifestRequestID}`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Description
Retrieves the manifest of video clips stored in the sync module's local storage. You must first request manifest creation using [Request Local Storage Manifest](request-local-storage-manifest.md) to get the manifest request ID.

**Note:** This is the second step in the local storage workflow. The manifest request ID is obtained from the previous step.

### Parameters
- **AccountID** - Account ID (from homescreen or OAuth token)
- **NetworkID** - Network ID (from homescreen)
- **SyncID** - Sync module ID (from homescreen)
- **ManifestRequestID** - Manifest request ID (from request manifest endpoint)

### Response
Returns a manifest containing:
- **version** - Manifest version (e.g., "1.0")
- **manifest_id** - Manifest ID (use this for clip operations)
- **clips** - Array of clip objects:
  - **id** - Clip ID
  - **size** - Clip size in bytes
  - **camera_name** - Name of the camera that recorded the clip
  - **created_at** - Timestamp when the clip was created

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request GET \
  --url "https://rest-{region}.immedia-semi.com/api/v1/accounts/{AccountID}/networks/{NetworkID}/sync_modules/{SyncID}/local_storage/manifest/request/{ManifestRequestID}" \
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
SYNC_ID=$(echo "$HOMESCREEN" | grep -o '"sync_modules":\[{"id":[0-9]*' | grep -o '[0-9]*$' | head -1) && \
MANIFEST_REQUEST_ID=$(curl -s --request POST \
  --url "https://rest-${HOST}/api/v1/accounts/${ACCOUNT_ID}/networks/${NETWORK_ID}/sync_modules/${SYNC_ID}/local_storage/manifest/request" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" | jq -r '.id') && \
curl -s --request GET \
  --url "https://rest-${HOST}/api/v1/accounts/${ACCOUNT_ID}/networks/${NETWORK_ID}/sync_modules/${SYNC_ID}/local_storage/manifest/request/${MANIFEST_REQUEST_ID}" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" | jq
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.

### Example Response
`200 OK`

```javascript
{
  "version": "1.0",
  "manifest_id": "8977",
  "clips": [
    {
      "id": "2718594887",
      "size": "382",
      "camera_name": "UpdatedCameraName",
      "created_at": "2025-11-20T21:17:25+00:00"
    },
    {
      "id": "1282703322",
      "size": "188",
      "camera_name": "Camera",
      "created_at": "2025-11-19T15:53:02+00:00"
    },
    {
      "id": "3192005412",
      "size": "290",
      "camera_name": "Camera",
      "created_at": "2025-11-19T07:04:05+00:00"
    }
  ]
}
```

### Next Steps
After retrieving the manifest, you can:
1. Select a clip ID from the manifest
2. Request clip upload: [Request Local Storage Clip Upload](request-local-storage-clip-upload.md)
3. Download the clip: [Download Local Storage Clip](download-local-storage-clip.md)

### See Also
- [Request Local Storage Manifest](request-local-storage-manifest.md) - Request manifest creation
- [Request Local Storage Clip Upload](request-local-storage-clip-upload.md) - Request clip upload
- [Download Local Storage Clip](download-local-storage-clip.md) - Download clip

