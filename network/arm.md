## Arm the System

Arm the given network - that is, start recording/reporting motion events for enabled cameras.

When this call returns, it does not mean the arm request is complete,  the client must gather the command ID from the response and poll for the status of the command.
 

`POST /api/v1/accounts/{AccountID}/networks/{NetworkID}/state/arm`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Response
- A command object or error response. See example. This call is asynchronous and is monitored by the [Command Status](command.md) API call using the returned Command Id.

**Error Responses:**
- `{"message":"No Cameras Enabled for Motion","code":304}` - At least one camera must have motion detection enabled before the system can be armed. Use [Enable Motion Detection](../camera/enable.md) first.

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request POST \
  --url "https://rest-{region}.immedia-semi.com/api/v1/accounts/{AccountID}/networks/{NetworkID}/state/arm" \
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
HOMESCREEN=$(curl -s --request GET \
  --url "https://rest-${HOST}/api/v3/accounts/${ACCOUNT_ID}/homescreen" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json") && \
NETWORK_ID=$(echo "$HOMESCREEN" | grep -o '"networks":\[{"id":[0-9]*' | grep -o '[0-9]*$' | head -1) && \
curl --request POST \
  --url "https://rest-${HOST}/api/v1/accounts/${ACCOUNT_ID}/networks/${NETWORK_ID}/state/arm" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json"
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.

### Example Response

**Success Response:**
`200 OK`

```javascript
{
  "id": 123456789,
  "network_id": 1234,
  "command": "arm",
  "state": "new",
  "commands": [
    {
      "id": 123456780,
      "network_id": 1234,
      "command": "config_lfr",
      "state": "running"
    },
    {
      "id": 123456781,
      "network_id": 1234,
      "command": "config_lfr",
      "state": "running"
    }
  ]
}
```

**Error Response:**
`200 OK` (with error in body)

```javascript
{
  "message": "No Cameras Enabled for Motion",
  "code": 304
}
```



