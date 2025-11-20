## Upload Logs

Upload diagnostic logs to Blink servers. This endpoint is typically used for troubleshooting purposes.

`POST /app/logs/upload`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.
- **Content-Type** - `multipart/form-data` or `application/json` - Required for request body

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Request Body
Log data in either JSON or multipart/form-data format. The exact structure may vary depending on the client implementation.

**Common Formats:**
- **JSON format**: `{"logs": "log data here"}` - Simple text-based log data
- **Multipart/form-data**: File upload format, typically used by mobile apps for binary log files

**Note:** This endpoint is primarily used by the official Blink mobile apps. The exact request format and field names may vary between different client implementations.

### Response
A success message object. See example.

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request POST \
  --url "https://rest-{region}.immedia-semi.com/app/logs/upload" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{"logs": "log data here"}'
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
  --url "https://rest-${HOST}/app/logs/upload" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{"logs": "log data here"}'
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.


### Example Response
`200 OK`

```javascript
{
  "id": 116916853,
  "created_at": "2025-11-20T21:37:05+00:00",
  "updated_at": "2025-11-20T21:37:05+00:00",
  "deleted_at": null,
  "server": "rest",
  "server_instance": "i-0240457a29cea53a8",
  "severity": null,
  "error_code": 3,
  "text": "logs/account/123456/client/1234567/2025_11_20_21.37.05PM-jQhsCrU.log",
  "account_id": 123456
}
```

**Notes:**
- This endpoint is primarily used by the official Blink mobile apps for diagnostic and troubleshooting purposes
- **Response structure** is consistent and includes:
  - `id` - Log entry identifier
  - `server` and `server_instance` - Server information where logs are stored
  - `text` - Path to the uploaded log file
  - `account_id` - Account identifier
  - `created_at`, `updated_at` - Timestamps
- **Request format** may vary:
  - JSON format with text logs
  - Multipart/form-data for file uploads
  - Field names and structure may differ between client implementations
- The exact request format is not fully documented in the public API as it's primarily an internal diagnostic tool

