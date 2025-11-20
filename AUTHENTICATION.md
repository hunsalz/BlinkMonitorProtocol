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

## Initial Login

If you don't have tokens yet, you need to perform an initial login with your username and password to obtain both an `access_token` and `refresh_token`.

### Initial Login Request

```sh
# Initial login to get tokens
TOKEN_RESPONSE=$(curl -s --request POST \
  --url "https://api.oauth.blink.com/oauth/token" \
  --header "Content-Type: application/x-www-form-urlencoded" \
  --header "User-Agent: Blink" \
  --data-urlencode "grant_type=password" \
  --data-urlencode "username=your_email@example.com" \
  --data-urlencode "password=your_password" \
  --data-urlencode "client_id=android" \
  --data-urlencode "scope=client")

# Extract tokens from response
ACCESS_TOKEN=$(echo "$TOKEN_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
REFRESH_TOKEN=$(echo "$TOKEN_RESPONSE" | grep -o '"refresh_token":"[^"]*' | cut -d'"' -f4)
CLIENT_ID=$(echo "$TOKEN_RESPONSE" | grep -o '"client_id":"[^"]*' | cut -d'"' -f4)
ACCOUNT_ID=$(echo "$TOKEN_RESPONSE" | grep -o '"account_id":[0-9]*' | grep -o '[0-9]*$')
USER_ID=$(echo "$TOKEN_RESPONSE" | grep -o '"user_id":[0-9]*' | grep -o '[0-9]*$')
```

### Storing Tokens

After obtaining tokens, store them in your `.env` file. See [Token Storage Format](#token-storage-format) section below for details on the `BLINK_TOKENS` format.

**Important**: 
- Save the `refresh_token` securely - you'll need it to get new access tokens
- The `access_token` expires after 4 hours, but the `refresh_token` is long-lived
- Never commit your `.env` file to version control

## Token Refresh

OAuth access tokens expire after 4 hours. Use your refresh token to get a new access token:

```sh
# Refresh OAuth token
TOKEN_RESPONSE=$(curl -s --request POST \
  --url "https://api.oauth.blink.com/oauth/token" \
  --header "Content-Type: application/x-www-form-urlencoded" \
  --header "User-Agent: Blink" \
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

#### Common Authentication Errors

**Error 101 - Unauthorized Access**
```json
{"message":"Unauthorized Access","code":101}
```
- **Cause**: Access token has expired or is invalid
- **Solution**: Refresh the token using your refresh token and retry the request
- **Prevention**: The complete examples below automatically refresh the token before making requests

**Invalid Credentials**
```json
{"error":"invalid_grant","error_description":"Invalid username or password"}
```
- **Cause**: Incorrect username or password during initial login
- **Solution**: Verify your credentials and try again

**Invalid Refresh Token**
```json
{"error":"invalid_grant","error_description":"Invalid refresh token"}
```
- **Cause**: Refresh token has expired, been revoked, or is invalid
- **Solution**: Perform a new initial login to obtain fresh tokens

**Invalid Client ID**
```json
{"error":"invalid_client","error_description":"Invalid client_id"}
```
- **Cause**: The `client_id` parameter is incorrect or not recognized
- **Solution**: Use `client_id=android` (default) or the client_id from your token response

**Token Expiration Detection**
- Access tokens expire after 4 hours
- If you receive error 101, your token has likely expired
- Always refresh tokens before making API requests, or implement automatic refresh logic

### Why Bearer Tokens?

- OAuth 2.0 standard for secure API authentication
- Tokens can be revoked server-side
- No need to send credentials with each request
- Supports token refresh without re-authentication

## Token Storage Format

The `.env` file stores authentication tokens in a pipe-delimited format within the `BLINK_TOKENS` variable.

### Format Structure

```
BLINK_TOKENS='key1=value1|key2=value2|key3=value3|...'
```

### Available Fields

The `BLINK_TOKENS` variable can contain the following fields (URL-encoded):

- **username** - Your Blink account email address
- **password** - Your Blink account password (URL-encoded)
- **uid** - User identifier (e.g., `BlinkCamera_xxx`)
- **device_id** - Device identifier (e.g., `Blinkpy`)
- **token** - Access token (JWT)
- **expires_in** - Token expiration time in seconds (typically `14400` = 4 hours)
- **expiration_date** - Unix timestamp of token expiration
- **refresh_token** - Refresh token (JWT) for obtaining new access tokens
- **host** - Regional server hostname (e.g., `e008.immedia-semi.com`)
- **region_id** - Region identifier (e.g., `e008`)
- **client_id** - OAuth client identifier (e.g., `1234567` or `android`)
- **account_id** - Your Blink account ID
- **user_id** - Your user ID
- **2fa_code** - Two-factor authentication code (if applicable)

### Extracting Values

Use `sed` to extract individual values from `BLINK_TOKENS`:

```sh
# Extract refresh token
REFRESH_TOKEN=$(echo "$BLINK_TOKENS" | sed -n "s/.*refresh_token=\([^|]*\).*/\1/p")

# Extract client ID
CLIENT_ID=$(echo "$BLINK_TOKENS" | sed -n "s/.*client_id=\([^|]*\).*/\1/p")

# Extract host
HOST=$(echo "$BLINK_TOKENS" | sed -n "s/.*host=\([^|]*\).*/\1/p")

# Extract account ID
ACCOUNT_ID=$(echo "$BLINK_TOKENS" | sed -n "s/.*account_id=\([^|]*\).*/\1/p")
```

### Example BLINK_TOKENS Value

```
BLINK_TOKENS='username=user%40example.com|password=encoded%20password|uid=BlinkCamera_xxx|device_id=Blinkpy|token=eyJhbGc...|expires_in=14400|expiration_date=1234567890.123|refresh_token=eyJhbGc...|host=e008.immedia-semi.com|region_id=e008|client_id=1234567|account_id=123456|user_id=123456|2fa_code=123456'
```

**Note**: Values are URL-encoded, so special characters like `@` become `%40` and spaces become `%20`.

## Complete Example Template

### Step 1: Refresh Token

```sh
source .env && \
REFRESH_TOKEN=$(echo "$BLINK_TOKENS" | sed -n "s/.*refresh_token=\([^|]*\).*/\1/p") && \
CLIENT_ID=$(echo "$BLINK_TOKENS" | sed -n "s/.*client_id=\([^|]*\).*/\1/p") && \
TOKEN_RESPONSE=$(curl -s --request POST --url "https://api.oauth.blink.com/oauth/token" \
  --header "Content-Type: application/x-www-form-urlencoded" \
  --header "User-Agent: Blink" \
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
curl --request {METHOD} \
  --url "https://rest-${HOST}/{ENDPOINT_PATH}" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" \
  {OPTIONAL_BODY_OR_OUTPUT}
```

Replace `{METHOD}` and `{ENDPOINT_PATH}` with your specific endpoint details.

## Response Examples

### OAuth Token Response

When you successfully authenticate (initial login or token refresh), you'll receive a JSON response:

```json
{
  "account_id": 123456,
  "client_id": "1234567",
  "created_at": "2025-01-20T12:00:00+00:00",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 14400,
  "expires_at": 1737374400,
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "scope": "client",
  "user_id": 123456
}
```

**Key Fields:**
- **token** (or **access_token**) - The access token to use in API requests
- **refresh_token** - Long-lived token for obtaining new access tokens
- **expires_in** - Token lifetime in seconds (14400 = 4 hours)
- **account_id** - Your Blink account ID
- **client_id** - OAuth client identifier
- **user_id** - Your user ID

### Error Response Examples

**Expired Token:**
```json
{
  "message": "Unauthorized Access",
  "code": 101
}
```

**Invalid Credentials:**
```json
{
  "error": "invalid_grant",
  "error_description": "Invalid username or password"
}
```

**Invalid Refresh Token:**
```json
{
  "error": "invalid_grant",
  "error_description": "Invalid refresh token"
}
```

## Troubleshooting

### Common Problems and Solutions

#### Problem: "Unauthorized Access" (Error 101)

**Symptoms**: API requests return `{"message":"Unauthorized Access","code":101}`

**Possible Causes**:
1. Access token has expired (most common)
2. Access token is invalid or malformed
3. Token was revoked server-side

**Solutions**:
1. Refresh your access token using the refresh token
2. Verify your refresh token is still valid
3. If refresh fails, perform a new initial login

**Prevention**: Always refresh tokens before making API requests, or implement automatic token refresh logic.

---

#### Problem: Cannot Extract Token from Response

**Symptoms**: `NEW_TOKEN` variable is empty after token refresh

**Possible Causes**:
1. Token refresh request failed
2. Response format changed
3. `grep` pattern doesn't match response

**Solutions**:
1. Check the raw response: `echo "$TOKEN_RESPONSE"`
2. Verify the response contains `"access_token"` or `"token"` field
3. Adjust extraction pattern if needed:
   ```sh
   # Try alternative extraction
   NEW_TOKEN=$(echo "$TOKEN_RESPONSE" | grep -o '"token":"[^"]*' | cut -d'"' -f4)
   # Or if using "access_token" field
   NEW_TOKEN=$(echo "$TOKEN_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
   ```

---

#### Problem: Invalid Refresh Token

**Symptoms**: Token refresh returns `{"error":"invalid_grant","error_description":"Invalid refresh token"}`

**Possible Causes**:
1. Refresh token has expired
2. Refresh token was revoked
3. Refresh token is malformed or corrupted

**Solutions**:
1. Perform a new initial login to obtain fresh tokens
2. Verify your `.env` file contains the correct refresh token
3. Check if the refresh token was accidentally modified

---

#### Problem: Cannot Extract Values from BLINK_TOKENS

**Symptoms**: Variables are empty after extracting from `BLINK_TOKENS`

**Possible Causes**:
1. `.env` file not sourced correctly
2. `BLINK_TOKENS` format is incorrect
3. Field name doesn't match

**Solutions**:
1. Verify `.env` is sourced: `source .env && echo "$BLINK_TOKENS"`
2. Check field names match exactly (case-sensitive)
3. Verify pipe-delimited format is correct
4. Test extraction manually:
   ```sh
   source .env
   echo "$BLINK_TOKENS" | sed -n "s/.*refresh_token=\([^|]*\).*/\1/p"
   ```

---

#### Problem: Token Expires Too Quickly

**Symptoms**: Tokens stop working after a short time

**Possible Causes**:
1. System clock is incorrect
2. Token expiration time is shorter than expected

**Solutions**:
1. Verify system clock is synchronized
2. Check `expires_in` value in token response (should be 14400 seconds = 4 hours)
3. Implement token refresh before expiration

---

### Step-by-Step Debugging Guide

1. **Verify .env file exists and is readable**
   ```sh
   test -f .env && echo ".env exists" || echo ".env missing"
   ```

2. **Check BLINK_TOKENS is set**
   ```sh
   source .env && echo "BLINK_TOKENS length: ${#BLINK_TOKENS}"
   ```

3. **Test token refresh manually**
   ```sh
   source .env
   REFRESH_TOKEN=$(echo "$BLINK_TOKENS" | sed -n "s/.*refresh_token=\([^|]*\).*/\1/p")
   echo "Refresh token: ${REFRESH_TOKEN:0:20}..." # Show first 20 chars
   
   TOKEN_RESPONSE=$(curl -s --request POST --url "https://api.oauth.blink.com/oauth/token" \
     --header "Content-Type: application/x-www-form-urlencoded" \
     --header "User-Agent: Blink" \
     --data-urlencode "grant_type=refresh_token" \
     --data-urlencode "refresh_token=$REFRESH_TOKEN" \
     --data-urlencode "client_id=android" \
     --data-urlencode "scope=client")
   
   echo "Response: $TOKEN_RESPONSE"
   ```

4. **Verify token extraction**
   ```sh
   NEW_TOKEN=$(echo "$TOKEN_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
   echo "Token extracted: ${NEW_TOKEN:0:20}..." # Show first 20 chars
   ```

5. **Test API request with token**
   ```sh
   curl -v --request GET \
     --url "https://rest-{host}/api/v3/accounts/{account_id}/homescreen" \
     --header "Authorization: Bearer $NEW_TOKEN" \
     --header "Content-Type: application/json"
   ```

## Notes

- The REST API session token method (TOKEN_AUTH header) is deprecated and no longer works
- All endpoints now require OAuth Bearer token authentication
- Access tokens expire after 4 hours and must be refreshed
- The refresh token can be used repeatedly to get new access tokens without re-authenticating

