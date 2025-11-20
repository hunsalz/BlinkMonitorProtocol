## Set Clip Options

Set clip-related options for the account.

`POST /api/v1/account/video_options`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.
- **Content-Type** - `application/json` - Required for request body

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Request Body
Clip options object. Exact fields may vary. See example.

### Response
A success message object or error response. See example.

**Error Responses:**
- `{"message":"Invalid auto purge days value","code":213}` - The `auto_delete_days` value must be valid. Check the allowed range for your account.

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request POST \
  --url "https://rest-{region}.immedia-semi.com/api/v1/account/video_options" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{"auto_delete_days": 7, "storage": 1}'
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
curl --request POST \
  --url "https://rest-${HOST}/api/v1/account/video_options" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{"auto_delete_days": 7, "storage": 1}'
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.


### Example Response

**Success Response:**
`200 OK`

```javascript
{
  "message": "Clip options updated successfully",
  "code": 200
}
```

**Error Response:**
`200 OK` (with error in body)

```javascript
{
  "message": "Invalid auto purge days value",
  "code": 213
}
```

**Note:** The exact request body structure and response format may vary. This endpoint is used to configure clip storage and deletion settings. The `auto_delete_days` value must be within the allowed range for your account.

