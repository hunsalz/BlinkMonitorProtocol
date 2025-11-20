## Update Client Options
Update client-specific configuration options for the authenticated client. This endpoint allows you to modify client-level settings, such as notification keys for push notifications or other client-specific preferences.

**📌 API Evolution Note:** This endpoint uses an unversioned path structure (`/client/...`). There is a related versioned endpoint for retrieving client options: [Get Client Options (v1)](../../v1/accounts/get-client-options.md) (`GET /api/v1/accounts/{AccountID}/clients/{ClientID}/options`). The unversioned path structure represents an earlier API design that evolved alongside the versioned structure.

**Note:** The exact purpose and parameters of this endpoint are not fully documented in the public API. The `notification_key` parameter appears to be used for push notification configuration, but the exact format and usage may vary.

`POST /client/{ClientID}/update`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.
- **Content-Type** - `application/json` - Required for request body

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Request Body
- **notification_key** - (Required) A notification key string used for push notification configuration. This is typically a device-specific token or identifier used to send push notifications to the client. The exact format and purpose are not fully documented in the public API, but it appears to be related to push notification service registration (e.g., FCM token for Android, APNs token for iOS).

### Response
A success message confirming the client options were updated. The response format may vary - some responses include the full client object with updated information, while others return a simple success message.

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request POST \
  --url "https://rest-{region}.immedia-semi.com/client/{ClientID}/update" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{"notification_key":"aNotificationKeyString"}'
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
CLIENT_ID_TO_USE=${CLIENT_ID} && \
curl --request POST \
  --url "https://rest-${HOST}/client/${CLIENT_ID_TO_USE}/update" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{"notification_key":"aNotificationKeyString"}'
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.


### Example Response
`200 OK`

```javascript
{
  "message": "Client successfully updated",
  "code": 241
}
```

**Notes:**
- **Response format variations:**
  - **Standard response**: Success message with code `241` (most common)
  - **Extended response**: Some responses may include the full client object with updated information
  - The variation appears to depend on server configuration or response type, not account type
- The `notification_key` parameter is used to register or update push notification tokens for the client
- This endpoint is primarily used by the official Blink mobile apps for push notification configuration
- **API Evolution:** Unversioned endpoints represent a different path structure that continues to be supported. They are not deprecated, but represent an alternative API design pattern.
- **Related endpoints:**
  - [Get Client Options (v1)](../../v1/accounts/get-client-options.md) - Versioned endpoint to retrieve client settings (`GET /api/v1/accounts/{AccountID}/clients/{ClientID}/options`)