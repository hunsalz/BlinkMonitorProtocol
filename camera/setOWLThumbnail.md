## Set Thumbnail for Owl

Set the thumbnail by taking a snapshot of the current view of the camera.

`POST /api/v1/accounts/{AccountID}/networks/{NetworkID}/owls/{CameraID}/thumbnail`

### Headers
- **TOKEN_AUTH** -  session auth token


### Response
A command object.  See example.  This call is asynchronous and is monitored by the [Command Status](../network/command.md) API call using the returned Command Id.

### Example Request
```sh
curl --request POST \
  --url https://rest-prod.immedia-semi.com/api/v1/accounts/11111/networks/22222/owls/44444/thumbnail \
  --header 'TOKEN_AUTH: {AuthToken}'
```

### Example Response
`200 OK`

```javascript
{
  "id": 1678210511,
  "network_id": 158164,
  "command": "thumbnail",
  "state": "new"
}
