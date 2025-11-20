## Disable Schedule

Disable an existing schedule (programs) defined for the given Network/Blink Module

`POST /api/v1/networks/{NetworkID}/programs/{ProgramID}/disable`

### Headers
- **TOKEN_AUTH** -  session auth token


### Response
see example


### Example Request
```sh
curl --request POST \
  --url https://rest-prod.immedia-semi.com/api/v1/networks/189117/programs/123/disable \
  --header 'TOKEN_AUTH: {AuthToken}'
```


### Example Response
`200 OK`

```javascript
{
  "message": "Successfully disabled program 123",
  "code": 803
}
```

