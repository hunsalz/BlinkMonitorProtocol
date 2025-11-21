## Request Local Storage Manifest

Request creation of a manifest of video clips stored in sync module local storage.

`POST /api/v1/accounts/{AccountID}/networks/{NetworkID}/sync_modules/{SyncID}/local_storage/manifest/request`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Description
This endpoint initiates the creation of a manifest listing all video clips stored in the sync module's local storage. The response contains a manifest request ID that must be used to retrieve the actual manifest.

**Note:** This is the first step in the local storage workflow. After requesting the manifest, you must poll for it using the manifest request ID.

### Response
Returns a manifest request ID:
- **id** - Manifest request ID (use this to retrieve the manifest)
- **network_id** - Network ID

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request POST \
  --url "https://rest-{region}.immedia-semi.com/api/v1/accounts/{AccountID}/networks/{NetworkID}/sync_modules/{SyncID}/local_storage/manifest/request" \
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
curl -s --request POST \
  --url "https://rest-${HOST}/api/v1/accounts/${ACCOUNT_ID}/networks/${NETWORK_ID}/sync_modules/${SYNC_ID}/local_storage/manifest/request" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" | jq
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.

### Example Response
`200 OK`

```javascript
{
  "id": 670555852,
  "network_id": 189117
}
```

### Next Steps
After receiving the manifest request ID, use it to retrieve the manifest:
- [Get Local Storage Manifest](get-local-storage-manifest.md) : `GET /api/v1/accounts/{AccountID}/networks/{NetworkID}/sync_modules/{SyncID}/local_storage/manifest/request/{ManifestRequestID}`

### See Also
- [Get Local Storage Manifest](get-local-storage-manifest.md) - Retrieve the manifest
- [Request Local Storage Clip Upload](request-local-storage-clip-upload.md) - Request clip upload
- [Download Local Storage Clip](download-local-storage-clip.md) - Download clip

