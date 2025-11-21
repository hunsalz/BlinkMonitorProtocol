## Request Local Storage Clip Upload

Request a clip stored in sync module local storage to be uploaded to the cloud.

`POST /api/v1/accounts/{AccountID}/networks/{NetworkID}/sync_modules/{SyncID}/local_storage/manifest/{ManifestID}/clip/request/{ClipID}`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Description
Requests that a specific clip stored in the sync module's local storage be uploaded to the cloud. After the upload is complete, the clip can be downloaded using the same URL with a GET request.

**Note:** This is the third step in the local storage workflow. You must first:
1. Request manifest creation
2. Retrieve the manifest to get the manifest ID and clip ID
3. Request clip upload (this endpoint)
4. Download the clip

### Parameters
- **AccountID** - Account ID (from homescreen or OAuth token)
- **NetworkID** - Network ID (from homescreen)
- **SyncID** - Sync module ID (from homescreen)
- **ManifestID** - Manifest ID (from manifest response)
- **ClipID** - Clip ID (from manifest clips array)

### Response
Returns a command ID:
- **id** - Command ID (may need to poll for completion)
- **network_id** - Network ID

**Note:** The upload is asynchronous. You may need to poll the command status to ensure the upload is complete before downloading.

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request POST \
  --url "https://rest-{region}.immedia-semi.com/api/v1/accounts/{AccountID}/networks/{NetworkID}/sync_modules/{SyncID}/local_storage/manifest/{ManifestID}/clip/request/{ClipID}" \
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
MANIFEST=$(curl -s --request GET \
  --url "https://rest-${HOST}/api/v1/accounts/${ACCOUNT_ID}/networks/${NETWORK_ID}/sync_modules/${SYNC_ID}/local_storage/manifest/request/${MANIFEST_REQUEST_ID}" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json") && \
MANIFEST_ID=$(echo "$MANIFEST" | jq -r '.manifest_id') && \
CLIP_ID=$(echo "$MANIFEST" | jq -r '.clips[0].id') && \
curl -s --request POST \
  --url "https://rest-${HOST}/api/v1/accounts/${ACCOUNT_ID}/networks/${NETWORK_ID}/sync_modules/${SYNC_ID}/local_storage/manifest/${MANIFEST_ID}/clip/request/${CLIP_ID}" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" | jq
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.

### Example Response
`200 OK`

```javascript
{
  "id": 670557344,
  "network_id": 189117
}
```

### Next Steps
After requesting the upload, wait for it to complete, then download the clip:
- [Download Local Storage Clip](download-local-storage-clip.md) : `GET /api/v1/accounts/{AccountID}/networks/{NetworkID}/sync_modules/{SyncID}/local_storage/manifest/{ManifestID}/clip/request/{ClipID}`

### See Also
- [Request Local Storage Manifest](request-local-storage-manifest.md) - Request manifest creation
- [Get Local Storage Manifest](get-local-storage-manifest.md) - Retrieve manifest
- [Download Local Storage Clip](download-local-storage-clip.md) - Download clip
- [Command Status](../../unversioned/network/command.md) - Poll command status

