## Get Regions
Get valid region info for a locale. Authentication is not required. This endpoint is typically used during account registration or setup to determine available regions and their DNS endpoints. The response includes region information that may be used to select the appropriate regional server.

`GET /regions`

### Parameter
- **locale** -  A Two Character country code e.g. `US`


### Response
see example

### Example Request
```sh
curl --request GET \
  --url 'https://rest-prod.immedia-semi.com/regions?locale=US' | jq
```


### Example Response
`200 OK`

```javascript
{
  "preferred": "usu019",
  "regions": {
    "usu019": {
      "display_order": 1,
      "dns": "u019",
      "friendly_name": "United States - CENTRAL",
      "registration": true
    },
    "usu023": {
      "display_order": 2,
      "dns": "u023",
      "friendly_name": "United States - EAST",
      "registration": true
    },
    "usu015": {
      "display_order": 3,
      "dns": "u015",
      "friendly_name": "United States - WEST",
      "registration": true
    },
    "e002": {
      "display_order": 4,
      "dns": "e002",
      "friendly_name": "Europe",
      "registration": true
    },
    "sg": {
      "display_order": 5,
      "dns": "prsg",
      "friendly_name": "Southeast Asia",
      "registration": true
    }
  }
}
```
