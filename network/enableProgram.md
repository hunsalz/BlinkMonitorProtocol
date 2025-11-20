## Enable Schedule

Enable an existing schedule (programs) defined for the given Network/Blink Module

`POST /api/v1/networks/{NetworkID}/programs/{ProgramID}/enable`

### Headers
- **TOKEN_AUTH** -  session auth token


### Response
see example


### Example Request
```sh
curl --request POST \
  --url https://rest-prod.immedia-semi.com/api/v1/networks/1234/programs/123/enable \
  --header 'TOKEN_AUTH: {AuthToken}'
```


### Example Response
`200 OK`

```javascript
{
  "message": "Successfully enabled program 700",
  "code": 802
}
```
