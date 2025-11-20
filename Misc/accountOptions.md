## Account Options
Some misc account specific flags

`GET /api/v1/account/options`

### Headers
- **TOKEN_AUTH** -  session auth token


### Response
see example

### Example Request
```sh
curl --request GET \
  --url https://rest-prod.immedia-semi.com/api/v1/account/options \
  --header 'TOKEN_AUTH: {AuthToken}'
```


### Example Response
`200 OK`

```javascript
{
  "owl_app_enabled": true,
  "legacy_account_mini": true
}
```