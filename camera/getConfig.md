## Get Camera Config

Retrieve the configuration for the given camera.

`GET /network/{NetworkID}/camera/{CameraID}/config`

### Headers
- **Authorization** - `Bearer {OAuthToken}` - OAuth 2.0 access token obtained from `https://api.oauth.blink.com/oauth/token`
- **Content-Type** - `application/json` - Required for API requests


### Response
A camera configuration object. See example.


### Authentication

This endpoint requires OAuth 2.0 Bearer token authentication. The token is obtained from Blink's OAuth server and must be refreshed periodically (access tokens expire after 4 hours).

**How OAuth Bearer tokens work:**
1. Obtain an access token from `https://api.oauth.blink.com/oauth/token` using your credentials or refresh token
2. Include the token in the `Authorization` header as `Bearer {token}`
3. The token authenticates your request to the REST API endpoints

### Example Request

**Step 1: Refresh your OAuth token (if expired)**

OAuth access tokens expire after 4 hours. Use your refresh token to get a new access token:

```sh
# Refresh OAuth token
TOKEN_RESPONSE=$(curl -s --request POST \
  --url "https://api.oauth.blink.com/oauth/token" \
  --header "Content-Type: application/x-www-form-urlencoded" \
  --header "User-Agent: Blinkpy" \
  --data-urlencode "grant_type=refresh_token" \
  --data-urlencode "refresh_token={YourRefreshToken}" \
  --data-urlencode "client_id=android" \
  --data-urlencode "scope=client")

# Extract the new access token from the response
NEW_TOKEN=$(echo "$TOKEN_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
```

**Step 2: Make the API request with Bearer token**

Use the `Authorization: Bearer` header to authenticate:

```sh
curl --request GET \
  --url "https://rest-{region}.immedia-semi.com/network/{NetworkID}/camera/{CameraID}/config" \
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
HOMESCREEN=$(curl -s --request GET \
  --url "https://rest-${HOST}/api/v3/accounts/${ACCOUNT_ID}/homescreen" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json") && \
NETWORK_ID=$(echo "$HOMESCREEN" | grep -o '"networks":\[{"id":[0-9]*' | grep -o '[0-9]*$' | head -1) && \
CAMERA_ID=$(echo "$HOMESCREEN" | grep -o '"cameras":\[{"id":[0-9]*' | grep -o '[0-9]*$' | head -1) && \
curl --request GET \
  --url "https://rest-${HOST}/network/${NETWORK_ID}/camera/${CAMERA_ID}/config" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json"
```

### How Bearer Token Authentication Works

**Bearer Token Format:**
- The token is a JWT (JSON Web Token) obtained from Blink's OAuth server
- It's included in the HTTP `Authorization` header with the format: `Authorization: Bearer {token}`
- The `Bearer` keyword indicates OAuth 2.0 token-based authentication

**Token Lifecycle:**
1. **Initial Login**: Authenticate with username/password to get both `access_token` and `refresh_token`
2. **Access Token**: Short-lived (4 hours), used for API requests
3. **Refresh Token**: Long-lived, used to obtain new access tokens without re-authenticating
4. **Token Refresh**: When access token expires, use refresh token to get a new one

**Error Handling:**
- If you receive `{"message":"Unauthorized Access","code":101}`, your access token has likely expired
- Refresh the token using your refresh token and retry the request
- The complete example above automatically refreshes the token before making the request

**Why Bearer Tokens?**
- OAuth 2.0 standard for secure API authentication
- Tokens can be revoked server-side
- No need to send credentials with each request
- Supports token refresh without re-authentication


### Example Response
`200 OK`

```javascript
{
  "id": 193210,
  "name": "Camera",
  "serial": "SERIAL123456789",
  "fw_version": "10.72",
  "type": "catalina",
  "enabled": true,
  "thumbnail": "/media/production/account/1234/network/189117/camera/193210/clip_name",
  "status": "online",
  "battery": "ok",
  "usage_rate": true,
  "network_id": 189117,
  "issues": [],
  "signals": {
    "lfr": 3,
    "wifi": 5,
    "temp": 71,
    "battery": 3
  },
  "motion_enabled": true,
  "armed": true
}
```

