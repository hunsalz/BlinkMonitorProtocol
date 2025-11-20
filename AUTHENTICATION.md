# Blink API Authentication

All Blink API endpoints require OAuth 2.0 Bearer token authentication. This guide explains how to authenticate and use tokens with the Blink API.

## Headers

All API requests require the following headers:

- **Authorization** - `Bearer {OAuthToken}` - OAuth 2.0 access token obtained from `https://api.oauth.blink.com/oauth/token`
- **Content-Type** - `application/json` - Required for API requests

## How OAuth Bearer Tokens Work

1. Obtain an access token from `https://api.oauth.blink.com/oauth/token` using your credentials or refresh token
2. Include the token in the `Authorization` header as `Bearer {token}`
3. The token authenticates your request to the REST API endpoints

## Token Refresh

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

## How Bearer Token Authentication Works

### Bearer Token Format

- The token is a JWT (JSON Web Token) obtained from Blink's OAuth server
- It's included in the HTTP `Authorization` header with the format: `Authorization: Bearer {token}`
- The `Bearer` keyword indicates OAuth 2.0 token-based authentication

### Token Lifecycle

1. **Initial Login**: Authenticate with username/password to get both `access_token` and `refresh_token`
2. **Access Token**: Short-lived (4 hours), used for API requests
3. **Refresh Token**: Long-lived, used to obtain new access tokens without re-authenticating
4. **Token Refresh**: When access token expires, use refresh token to get a new one

### Error Handling

- If you receive `{"message":"Unauthorized Access","code":101}`, your access token has likely expired
- Refresh the token using your refresh token and retry the request
- The complete examples below automatically refresh the token before making requests

### Why Bearer Tokens?

- OAuth 2.0 standard for secure API authentication
- Tokens can be revoked server-side
- No need to send credentials with each request
- Supports token refresh without re-authentication

## Complete Example Template

### Step 1: Refresh Token

```sh
source .env && \
REFRESH_TOKEN=$(echo "$BLINK_TOKENS" | sed -n "s/.*refresh_token=\([^|]*\).*/\1/p") && \
CLIENT_ID=$(echo "$BLINK_TOKENS" | sed -n "s/.*client_id=\([^|]*\).*/\1/p") && \
TOKEN_RESPONSE=$(curl -s --request POST --url "https://api.oauth.blink.com/oauth/token" \
  --header "Content-Type: application/x-www-form-urlencoded" \
  --header "User-Agent: Blinkpy" \
  --data-urlencode "grant_type=refresh_token" \
  --data-urlencode "refresh_token=$REFRESH_TOKEN" \
  --data-urlencode "client_id=${CLIENT_ID:-android}" \
  --data-urlencode "scope=client") && \
NEW_TOKEN=$(echo "$TOKEN_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
```

### Step 2: Get Network and Camera IDs (if needed)

```sh
HOST=$(echo "$BLINK_TOKENS" | sed -n "s/.*host=\([^|]*\).*/\1/p") && \
ACCOUNT_ID=$(echo "$BLINK_TOKENS" | sed -n "s/.*account_id=\([^|]*\).*/\1/p") && \
HOMESCREEN=$(curl -s --request GET \
  --url "https://rest-${HOST}/api/v3/accounts/${ACCOUNT_ID}/homescreen" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json") && \
NETWORK_ID=$(echo "$HOMESCREEN" | grep -o '"networks":\[{"id":[0-9]*' | grep -o '[0-9]*$' | head -1) && \
CAMERA_ID=$(echo "$HOMESCREEN" | grep -o '"cameras":\[{"id":[0-9]*' | grep -o '[0-9]*$' | head -1)
```

### Step 3: Make API Request

```sh
# For GET requests:
curl --request GET \
  --url "https://rest-${HOST}/{ENDPOINT_PATH}" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json"

# For POST requests:
curl --request POST \
  --url "https://rest-${HOST}/{ENDPOINT_PATH}" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{JSON_BODY}'
```

## Complete Working Example

This example refreshes the token, gets NetworkID and CameraID, then makes an API call:

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
curl --request {METHOD} \
  --url "https://rest-${HOST}/{ENDPOINT_PATH}" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" \
  {OPTIONAL_BODY_OR_OUTPUT}
```

Replace `{METHOD}` and `{ENDPOINT_PATH}` with your specific endpoint details.

## Notes

- The REST API session token method (TOKEN_AUTH header) is deprecated and no longer works
- All endpoints now require OAuth Bearer token authentication
- Access tokens expire after 4 hours and must be refreshed
- The refresh token can be used repeatedly to get new access tokens without re-authenticating

