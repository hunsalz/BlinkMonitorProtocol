## Set Thumbnail for Owl

Set the thumbnail by taking a snapshot of the current view of the camera.

`POST /api/v1/accounts/{AccountID}/networks/{NetworkID}/owls/{CameraID}/thumbnail`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.


### Response
A command object.  See example.  This call is asynchronous and is monitored by the [Command Status](../network/command.md) API call using the returned Command Id.

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request POST \
  --url "https://rest-{region}.immedia-semi.com/api/v1/accounts/{AccountID}/networks/{NetworkID}/owls/{CameraID}/thumbnail" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json"
```

**Complete working example using .env file:**

**Note:** This example assumes you have at least one OWL camera configured. If you get "Not Found" errors, check that your account has OWL cameras by inspecting the homescreen response.

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
HOMESCREEN=$(curl -s --request GET \
  --url "https://rest-${HOST}/api/v3/accounts/${ACCOUNT_ID}/homescreen" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json") && \
NETWORK_ID=$(echo "$HOMESCREEN" | grep -o '"networks":\[{"id":[0-9]*' | grep -o '[0-9]*$' | head -1) && \
CAMERA_ID=$(echo "$HOMESCREEN" | grep -o '"owls":\[{"id":[0-9]*' | grep -o '[0-9]*$' | head -1) && \
if [ -z "$CAMERA_ID" ]; then \
  echo "Error: No OWL cameras found. Your homescreen shows: $(echo "$HOMESCREEN" | grep -o '"owls":\[.*\]' | head -c 100)"; \
  echo "This endpoint requires at least one OWL camera to be configured in your account."; \
  exit 1; \
fi && \
curl --request POST \
  --url "https://rest-${HOST}/api/v1/accounts/${ACCOUNT_ID}/networks/${NETWORK_ID}/owls/${CAMERA_ID}/thumbnail" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json"
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.

### Example Response
`200 OK`

```javascript
{
  "id": 1678210511,
  "network_id": 158164,
  "command": "thumbnail",
  "state": "new"
}
