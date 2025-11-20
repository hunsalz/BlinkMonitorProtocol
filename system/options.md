## Client Options
Retrieve client-specific configuration options for the authenticated client. This endpoint returns client-level settings that may be used for push notifications, device preferences, or other client-specific configurations.

**Note:** The exact structure and purpose of the `options` field is not fully documented in the public API. The response typically contains an `options` field that may be a JSON string or empty object, depending on the client configuration.

`GET /api/v1/accounts/{AccountID}/clients/{ClientID}/options`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Response
A client options object containing client-specific configuration. The response structure is minimal and typically contains only an `options` field.

**Response Fields:**
- **options** - A JSON string or empty object string (`"{}"`) containing client-specific configuration. The structure and content of this field are not fully documented in the public API and may vary based on client type and configuration.

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request GET \
  --url "https://rest-{region}.immedia-semi.com/api/v1/accounts/{AccountID}/clients/{ClientID}/options" \
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
  --header "User-Agent: Blink" \
  --data-urlencode "grant_type=refresh_token" \
  --data-urlencode "refresh_token=$REFRESH_TOKEN" \
  --data-urlencode "client_id=${CLIENT_ID:-android}" \
  --data-urlencode "scope=client") && \
NEW_TOKEN=$(echo "$TOKEN_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4) && \
CLIENT_ID_TO_USE=${CLIENT_ID} && \
curl --request GET \
  --url "https://rest-${HOST}/api/v1/accounts/${ACCOUNT_ID}/clients/${CLIENT_ID_TO_USE}/options" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json"
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.


### Example Response
`200 OK`

```javascript
{
  "options": "{}"
}
```

**Notes:**
- The `options` field is typically an empty object string (`"{}"`) for most clients
- When populated, the `options` field may contain client-specific configuration such as notification preferences or device settings
- The exact structure and purpose of the options field is not fully documented in the public API
- This endpoint is primarily used by the official Blink mobile apps for client configuration management
- Related endpoints: [Update Client Options](update-options.md) to modify these settings