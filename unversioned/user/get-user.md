## Get User Information

Get information about the authenticated user.

`GET /user`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Description
Returns detailed information about the authenticated user, including account settings, preferences, and verification status.

**Note:** This endpoint uses an unversioned path structure. It provides user-specific information that may not be available in other endpoints.

### Response
Returns user information:
- **id** - User ID
- **created_at** - Account creation timestamp
- **updated_at** - Last update timestamp
- **email** - User email address
- **verified** - Whether email is verified
- **verification_required** - Whether verification is required
- **force_password_reset** - Whether password reset is forced
- **reset_expiration** - Password reset expiration (may be null)
- **time_zone** - User time zone
- **timezone_id** - Timezone ID
- **owner** - Whether user is account owner
- **name** - User name
- **user_access** - User access level (e.g., "write")
- **temp_units** - Temperature units preference ("f" or "c")
- **type** - User type (e.g., "regular")
- **pin_created_at** - PIN creation timestamp (may be null)
- **pin_failures** - Number of PIN failures
- **phone_number** - Phone number (may be null)
- **country_calling_code** - Country calling code (may be null)
- **locale** - User locale
- **country_id** - Country ID
- **verification_channel** - Email verification channel
- **phone_verified** - Whether phone is verified
- **phone_verification_required** - Whether phone verification is required
- **phone_verification_channel** - Phone verification channel
- **account_id** - Account ID
- **ring_idp_id** - Ring IDP ID (if integrated with Ring)

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request GET \
  --url "https://rest-{region}.immedia-semi.com/user" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" | jq
```

**Complete working example using .env file:**
```sh
source .env && \
REFRESH_TOKEN=$(echo "$BLINK_TOKENS" | sed -n "s/.*refresh_token=\([^|]*\).*/\1/p") && \
CLIENT_ID=$(echo "$BLINK_TOKENS" | sed -n "s/.*client_id=\([^|]*\).*/\1/p") && \
HOST=$(echo "$BLINK_TOKENS" | sed -n "s/.*host=\([^|]*\).*/\1/p") && \
TOKEN_RESPONSE=$(curl -s --request POST --url "https://api.oauth.blink.com/oauth/token" \
  --header "Content-Type: application/x-www-form-urlencoded" \
  --header "User-Agent: Blink" \
  --data-urlencode "grant_type=refresh_token" \
  --data-urlencode "refresh_token=$REFRESH_TOKEN" \
  --data-urlencode "client_id=${CLIENT_ID:-android}" \
  --data-urlencode "scope=client") && \
NEW_TOKEN=$(echo "$TOKEN_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4) && \
curl -s --request GET \
  --url "https://rest-${HOST}/user" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" | jq
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.

### Example Response
`200 OK`

```javascript
{
  "id": 199759,
  "created_at": "2025-02-15T21:13:04+00:00",
  "updated_at": "2025-02-15T21:14:26+00:00",
  "email": "user@example.com",
  "verified": true,
  "verification_required": true,
  "force_password_reset": false,
  "reset_expiration": null,
  "time_zone": "US/Eastern",
  "timezone_id": 432,
  "owner": true,
  "name": "",
  "user_access": "write",
  "temp_units": "f",
  "type": "regular",
  "pin_created_at": null,
  "pin_failures": 0,
  "phone_number": null,
  "country_calling_code": null,
  "locale": "de_DE",
  "country_id": "DE",
  "verification_channel": "email",
  "phone_verified": true,
  "phone_verification_required": true,
  "phone_verification_channel": "sms",
  "account_id": 123456,
  "ring_idp_id": 157534146
}
```

### See Also
- [Get Account Info](../v1/accounts/get-account-info.md) - Get account-level information
- [HomeScreen](../v3/accounts/homescreen.md) - Comprehensive account information

