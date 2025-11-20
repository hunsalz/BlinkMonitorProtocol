## Command Status

Return the status of the given command.

Most Camera and System/Module APIs make a call from the Blink Server to your local Synch Module.  These calls are asynchronous and return a command object.  Use the returned command id in these calls to poll for completion of the command using this API until the `complete` flag is true in the response.

The mobile clients poll for completion approximately once a second.

`GET /network/{NetworkID}/command/{CommandID}`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Response
A command status object. See example.

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request GET \
  --url "https://rest-{region}.immedia-semi.com/network/{NetworkID}/command/{CommandID}" \
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
COMMAND_ID=123456789 && \
curl --request GET \
  --url "https://rest-${HOST}/network/${NETWORK_ID}/command/${COMMAND_ID}" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json"
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.


### Example Response
`200 OK`

```javascript
{
  "complete": true,
  "status": 0,
  "status_msg": "Command succeeded",
  "status_code": 908,
  "commands": [
    {
      "id": 123456789,
      "created_at": "2025-11-20T21:21:06+00:00",
      "updated_at": "2025-11-20T21:21:09+00:00",
      "deleted_at": null,
      "execute_time": "2025-11-20T21:21:06+00:00",
      "command": "thumbnail",
      "state_stage": "vs",
      "stage_rest": "2025-11-20T21:21:06+00:00",
      "stage_cs_db": "2025-11-20T21:21:06+00:00",
      "stage_cs_sent": "2025-11-20T21:21:06+00:00",
      "stage_sm": "2025-11-20T21:21:06+00:00",
      "stage_dev": "2025-11-20T21:21:07+00:00",
      "state_condition": "done",
      "network_id": 1234,
      "account_id": 1234
    }
  ],
  "media_id": null
}
```