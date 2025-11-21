## Download Local Storage Clip

Download a clip that has been uploaded from sync module local storage to the cloud.

`GET /api/v1/accounts/{AccountID}/networks/{NetworkID}/sync_modules/{SyncID}/local_storage/manifest/{ManifestID}/clip/request/{ClipID}`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Description
Downloads a video clip that has been uploaded from the sync module's local storage to the cloud. You must first request the clip upload using [Request Local Storage Clip Upload](request-local-storage-clip-upload.md).

**Note:** This is the final step in the local storage workflow. The clip must be uploaded first before it can be downloaded.

### Parameters
- **AccountID** - Account ID (from homescreen or OAuth token)
- **NetworkID** - Network ID (from homescreen)
- **SyncID** - Sync module ID (from homescreen)
- **ManifestID** - Manifest ID (from manifest response)
- **ClipID** - Clip ID (from manifest clips array)

### Response
Returns the video clip as binary data (MP4 format).

**Content-Type:** `video/mp4` or `application/octet-stream`

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request GET \
  --url "https://rest-{region}.immedia-semi.com/api/v1/accounts/{AccountID}/networks/{NetworkID}/sync_modules/{SyncID}/local_storage/manifest/{ManifestID}/clip/request/{ClipID}" \
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
MANIFEST=$(curl -s --request GET \
  --url "https://rest-${HOST}/api/v1/accounts/${ACCOUNT_ID}/networks/${NETWORK_ID}/sync_modules/${SYNC_ID}/local_storage/manifest/request/${MANIFEST_REQUEST_ID}" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json") && \
MANIFEST_ID=$(echo "$MANIFEST" | jq -r '.manifest_id') && \
CLIP_ID=$(echo "$MANIFEST" | jq -r '.clips[0].id') && \
curl -s --request POST \
  --url "https://rest-${HOST}/api/v1/accounts/${ACCOUNT_ID}/networks/${NETWORK_ID}/sync_modules/${SYNC_ID}/local_storage/manifest/${MANIFEST_ID}/clip/request/${CLIP_ID}" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" > /dev/null && \
sleep 5 && \
curl -s --request GET \
  --url "https://rest-${HOST}/api/v1/accounts/${ACCOUNT_ID}/networks/${NETWORK_ID}/sync_modules/${SYNC_ID}/local_storage/manifest/${MANIFEST_ID}/clip/request/${CLIP_ID}" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" \
  --output "local_storage_clip_${CLIP_ID}.mp4" && \
echo "Clip saved to: local_storage_clip_${CLIP_ID}.mp4"
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.

### Example Response
`200 OK`

Binary MP4 video file.

### Workflow Summary

The complete local storage workflow:

1. **Request manifest creation**
   - [Request Local Storage Manifest](request-local-storage-manifest.md)
   - Get manifest request ID

2. **Retrieve manifest**
   - [Get Local Storage Manifest](get-local-storage-manifest.md)
   - Get manifest ID and clip IDs

3. **Request clip upload**
   - [Request Local Storage Clip Upload](request-local-storage-clip-upload.md)
   - Wait for upload to complete

4. **Download clip**
   - [Download Local Storage Clip](download-local-storage-clip.md) (this endpoint)
   - Save as MP4 file

### See Also
- [Request Local Storage Manifest](request-local-storage-manifest.md) - Request manifest creation
- [Get Local Storage Manifest](get-local-storage-manifest.md) - Retrieve manifest
- [Request Local Storage Clip Upload](request-local-storage-clip-upload.md) - Request clip upload

