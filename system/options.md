## Client Options
Get client specific options.   Details unknown.

`GET /api/v1/accounts/{AccountID}/clients/{ClientID}/options`

### Headers
- **TOKEN_AUTH** -  session auth token


### Response
- **options** - specific meaning unknown

### Example Request
```sh
curl --request GET \
  --url https://rest-prod.immedia-semi.com/api/v1/accounts/1234/clients/1234567/options \
  --header 'TOKEN_AUTH: {AuthToken}'
```


### Example Response
`200 OK`

```javascript
{
  "options": "A_LONG_ALPHANUMERIC_STRING"
}
```