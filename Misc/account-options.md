## Account Options
Retrieve account-specific feature flags and configuration options. This endpoint returns information about enabled features, subscription status, trial eligibility, and account limits.

`GET /api/v1/account/options`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Response
An account options object containing feature flags, subscription information, and account configuration. The response includes various boolean flags and configuration values.

**Response Field Categories:**
- **Feature Flags**: Boolean flags indicating enabled features (e.g., `catalina_app_enabled`, `owl_app_enabled`, `sm2_app_enabled`)
- **Subscription/Trial**: Trial eligibility and subscription status (e.g., `subs_eligible`, `trial_opt_in_eligible`, `trial_cancellation_enabled`)
- **Limits**: Account-specific limits (e.g., `c2s_clip_list_limit`)
- **Integrations**: Third-party integration status (e.g., `amazon_account_linking`, `amazon_account_linking_enabled`)
- **Power/Storage**: Power and storage features (e.g., `power_harvest_video`)

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request GET \
  --url "https://rest-{region}.immedia-semi.com/api/v1/account/options" \
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
curl --request GET \
  --url "https://rest-${HOST}/api/v1/account/options" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json"
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.


### Example Response
`200 OK`

```javascript
{
  "catalina_app_enabled": true,
  "power_harvest_video": true,
  "sm2_app_enabled": true,
  "snapshot_app_enabled": true,
  "seen_trial_carousel": true,
  "owl_app_enabled": true,
  "c2s_clip_list_limit": 1000,
  "trial_opt_in_length": 7,
  "amazon_account_linking": "available",
  "trial_cancellation_enabled": true,
  "subs_eligible": true,
  "amazon_account_linking_enabled": true,
  "breadcrumbs": [],
  "trial_opt_in_eligible": false,
  "trial_opt_in_eligible_v2": true
}
```

**Notes:**
- The response includes various account feature flags and configuration options
- **Common fields** (typically present): Feature flags, subscription status, trial eligibility
- **Variable fields** (may vary based on):
  - **Account type**: Free vs paid subscription accounts have different feature sets
  - **Subscription tier**: Different subscription levels enable different features
  - **Regional availability**: Some features may only be available in certain regions
  - **Device ownership**: Fields like `catalina_app_enabled`, `owl_app_enabled` depend on owned device types
  - **Trial status**: Trial-related fields (`trial_opt_in_eligible`, `trial_cancellation_enabled`) vary based on trial participation
- The exact fields present will reflect your account's specific configuration and available features