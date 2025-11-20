## Update Schedule

Update an existing schedule

`POST /api/v1/networks/{NetworkID}/programs/{ProgramID}/update`

### Headers
See [Authentication Guide](../../AUTHENTICATION.md) for required headers.
- **Content-Type** - `application/json` - Required for request body

### Authentication
This endpoint requires OAuth 2.0 Bearer token authentication. See [Authentication Guide](../../AUTHENTICATION.md) for details.

### Request Body
- **schedule object** - see example request

### Response
A program object with updated schedule. See example.

**Note:** This example automatically fetches the first available program ID from your network. If no programs exist, it will skip the request with a warning message.

### Example Request

**Simple example:**
```sh
# First refresh your token (see Authentication Guide)
curl --request POST \
  --url "https://rest-{region}.immedia-semi.com/api/v1/networks/{NetworkID}/programs/{ProgramID}/update" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{"id":123,"schedule":[{"dow":["mon","tue","wed","thu","fri"],"devices":[],"time":"2020-08-09 14:45:00 +0000","action":"arm"},{"dow":["mon","tue","wed","thu","fri"],"devices":[],"time":"2016-06-02 21:00:00 +0000","action":"disarm"}],"name":"schedulename","format":"v1"}'
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
PROGRAMS=$(curl -s --request GET \
  --url "https://rest-${HOST}/api/v1/networks/${NETWORK_ID}/programs" \
  --header "Authorization: Bearer $NEW_TOKEN" \
  --header "Content-Type: application/json") && \
PROGRAM_ID=$(echo "$PROGRAMS" | grep -o '"id":[0-9]*' | head -1 | grep -o '[0-9]*$') && \
if [ -z "$PROGRAM_ID" ]; then \
  echo "Warning: No programs found. Your network has no schedules configured."; \
  echo "This endpoint requires at least one program to be created first."; \
  echo "Skipping program update request."; \
else \
  curl --request POST \
    --url "https://rest-${HOST}/api/v1/networks/${NETWORK_ID}/programs/${PROGRAM_ID}/update" \
    --header "Authorization: Bearer $NEW_TOKEN" \
    --header "Content-Type: application/json" \
    --data '{"id":'$PROGRAM_ID',"schedule":[{"dow":["mon","tue","wed","thu","fri"],"devices":[],"time":"2020-08-09 14:45:00 +0000","action":"arm"},{"dow":["mon","tue","wed","thu","fri"],"devices":[],"time":"2016-06-02 21:00:00 +0000","action":"disarm"}],"name":"schedulename","format":"v1"}'; \
fi
```

See [Authentication Guide](../../AUTHENTICATION.md) for detailed authentication information and token management.


### Example Response
`200 OK`

```javascript
{
  "program": {
    "id": 123,
    "created_at": "2016-06-02T11:49:54+00:00",
    "updated_at": "2020-08-22T12:59:41+00:00",
    "name": "schedulename",
    "data": "{\"name\":\"schedulename\",\"schedule\":[{\"dow\":[\"mon\",\"tue\",\"wed\",\"thu\",\"fri\"],\"devices\":[],\"time\":\"2020-08-09 14:45:00 +0000\",\"action\":\"arm\"},{\"dow\":[\"mon\",\"tue\",\"wed\",\"thu\",\"fri\"],\"devices\":[],\"time\":\"2016-06-02 21:00:00 +0000\",\"action\":\"disarm\"}],\"format\":\"v1\"}",
    "status": "disabled",
    "network_id": 1234,
    "user_id": 1234,
    "account_id": 1234
  },
  "actions": [
    {
      "id": 123456789,
      "created_at": "2020-08-22T12:59:41+00:00",
      "updated_at": "2020-08-22T12:59:41+00:00",
      "time": "14:45",
      "dow": "mon",
      "alt_when": null,
      "action": "arm",
      "devices": "[]",
      "status": "active",
      "last_execution": null,
      "program_id": 123,
      "network_id": 1234,
      "user_id": 1234,
      "account_id": 1234
    },
  **additional action objects corresponding to each schedule point day, action, etc**
  ]
}
```
