## Get Account Info

Retrieve account information including account ID, client ID, country, region, tier, and verification status.

**⚠️ Version Compatibility:** This endpoint is backward compatible with v2. The v2 version (`/api/v2/accounts/{AccountID}/info`) returns additional fields (phone, email, Ring integration). See [Version Response Variations](../../plan/VERSION_RESPONSE_VARIATIONS.md) for details.

`GET /api/v1/accounts/{AccountID}/info`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Response
An account info object containing account identification, region information, tier, and verification status.

**Response Fields:**
- **account_id** - The account ID
- **client_id** - The OAuth client ID
- **country** - Two-letter country code (e.g., "DE", "US")
- **new_account** - Boolean indicating if this is a new account
- **tier** - Account tier identifier (e.g., "e008")
- **region** - Region identifier (e.g., "eu", "us")
- **account_verification_required** - Boolean indicating if account verification is required
- **phone_verification_required** - Boolean indicating if phone verification is required
- **client_verification_required** - Boolean indicating if client verification is required
- **verification_channel** - Preferred verification channel (e.g., "phone")
- **country_required** - Boolean indicating if country is required
- **user** - User object containing:
  - **user_id** - The user ID
  - **country** - User's country code

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request GET \
  --url "https://rest-{region}.immedia-semi.com/api/v1/accounts/{AccountID}/info" \
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
curl -s --request GET \
  --url "https://rest-${HOST}/api/v1/accounts/${ACCOUNT_ID}/info" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" | jq
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.

### Example Response
`200 OK`

```javascript
{
  "account_id": 123456,
  "client_id": 1234567,
  "country": "US",
  "new_account": false,
  "tier": "e001",
  "region": "us",
  "account_verification_required": false,
  "phone_verification_required": false,
  "client_verification_required": false,
  "verification_channel": "phone",
  "country_required": false,
  "user": {
    "user_id": 123456,
    "country": "US"
  }
}
```

**Note:** Example values shown above are placeholders. Replace with your actual account data.

**Notes:**
- This endpoint provides account-level information including region, tier, and verification status
- The `tier` field corresponds to the regional server identifier (e.g., "e001" for US, "e008" for Europe)
- The `region` field indicates the geographic region (e.g., "eu", "us")
- Verification flags indicate what verification steps may be required for the account
- **Version Compatibility:** This endpoint also works with `/api/v2/accounts/{AccountID}/info` which returns additional fields. See [Version Compatibility Report](../../plan/COMPATIBILITY_REPORT.md) for testing details.

**See also:**
- [Version Response Variations](../../plan/VERSION_RESPONSE_VARIATIONS.md) - Detailed comparison of v1 vs v2 response differences
- [Version Compatibility Report](../../plan/COMPATIBILITY_REPORT.md) - Complete compatibility testing results

