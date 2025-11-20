# BlinkMonitorProtocol

Unofficial documentation for the Client API of the Blink Wire-Free HD Home Monitoring &amp; Alert System. I am not affiliated with the company in any way - this documentation is strictly **"AS-IS"**.

The Client API is a straightforward REST API using JSON and HTTPS.

PR's welcome!

## Lessons Learned

### Authentication Method Change (2024-2025)

**Key Finding**: Blink has migrated from REST API session tokens to OAuth 2.0 Bearer token authentication.

**What Changed:**
- **Old Method (Deprecated)**: REST API session tokens via `TOKEN_AUTH` header from `/api/v5/account/login`
  - This endpoint now returns `{"message":"An app update is required"}` indicating it's obsolete
  - Session tokens are no longer issued or accepted
  
- **New Method (Current)**: OAuth 2.0 Bearer tokens via `Authorization: Bearer {token}` header
  - Tokens obtained from `https://api.oauth.blink.com/oauth/token`
  - Access tokens expire after 4 hours and must be refreshed using refresh tokens
  - This is the current and recommended authentication approach

**Impact:**
- All REST API endpoints still work, but now require OAuth Bearer tokens instead of session tokens
- The authentication flow is different but the endpoint URLs and request/response formats remain the same
- Token management is more robust with automatic refresh capabilities

**For Developers:**
- See [Authentication Guide](AUTHENTICATION.md) for complete OAuth Bearer token implementation details
- Use `.env.template` as a reference for required environment variables
- All endpoint documentation has been updated to reflect the new authentication method


## Overview

* **Initial server URL** - https://rest-prod.immedia-semi.com
* **Authentication** - ⚠️ **Important**: Blink uses **OAuth 2.0 Bearer token** authentication. See [Authentication Guide](AUTHENTICATION.md) for complete details on how to authenticate and use OAuth Bearer tokens.
* **Account** - An account corresponds to a single set of login credentials. The Account ID is returned in the homescreen call.
* **Client** - A unique client/app to the account. A single account may have many client apps. The Client ID is obtained from your OAuth token response.
* **Network** - A single account may have many networks. A network corresponds conceptually to a Blink Synch module. An account could have multiple networks/synch modules - e.g. multiple sites/homes. Network and Synch Module information associated with an account is returned in the homescreen call.
* **Camera** - A network (synch module) may have one or more cameras. Camera information is returned in the homescreen call.
* **Command** - Some operations reach out from the Blink Servers to your local Blink module.  These operations are asynchronous and return a Command ID to be polled for completion via the Command Status call.


### Authentication

**⚠️ Important**: All endpoints require OAuth 2.0 Bearer token authentication. See [Authentication Guide](AUTHENTICATION.md) for complete documentation.

* [Authentication Guide](AUTHENTICATION.md) - **Start here** - Complete guide to OAuth Bearer token authentication


### System

* [HomeScreen](system/homescreen.md) : `GET /api/v3/accounts/{AccountID}/homescreen`
* [Get Account Notification Flags](system/get-notifications.md) : `GET /api/v1/accounts/{AccountID}/notifications/configuration`
* [Set Notification Flags](system/set-notifications.md) : `POST /api/v1/accounts/{AccountID}/notifications/configuration`
* [Get Client Options](system/options.md) : `GET /api/v1/accounts/{AccountID}/clients/{ClientID}/options`
* [Set Client Options](system/update-options.md) : `POST /client/{ClientID}/update`


### Network

* [Command Status](network/command.md) : `GET /network/{NetworkID}/command/{CommandID}`
* [Arm System](network/arm.md) : `POST /api/v1/accounts/{AccountID}/networks/{NetworkID}/state/arm`
* [Disarm System](network/disarm.md) : `POST /api/v1/accounts/{AccountID}/networks/{NetworkID}/state/disarm`
* [List Schedules](network/list-programs.md) : `GET /api/v1/networks/{NetworkID}/programs`
* [Enable Schedule](network/enable-program.md) : `POST /api/v1/networks/{NetworkID}/programs/{ProgramID}/enable`
* [Disable Schedule](network/disable-program.md) : `POST /api/v1/networks/{NetworkID}/programs/{ProgramID}/disable`
* [Update Schedule](network/update-program.md) : `POST /api/v1/networks/{NetworkID}/programs/{ProgramID}/update`


### Cameras

* [Enable Motion Detection](camera/enable.md) : `POST /network/{NetworkID}/camera/{CameraID}/enable`
* [Disable Motion Detection](camera/disable.md) : `POST /network/{NetworkID}/camera/{CameraID}/disable`
* [Create New Thumbnail](camera/set-thumbnail.md) : `POST /network/{NetworkID}/camera/{CameraID}/thumbnail`
* [Set OWL Thumbnail](camera/set-owl-thumbnail.md) : `POST /api/v1/accounts/{AccountID}/networks/{NetworkID}/owls/{CameraID}/thumbnail`
* [Liveview](camera/liveview.md) : `POST /api/v5/accounts/{AccountID}/networks/{NetworkID}/cameras/{CameraID}/liveview`
* [Record Video Clip from Camera](camera/record-clip.md) : `POST /network/{NetworkID}/camera/{CameraID}/clip`
* [Snooze Camera](camera/snooze.md) : `POST /api/v1/accounts/{AccountID}/networks/{NetworkID}/cameras/{CameraID}/snooze`
* [Get Camera Config](camera/get-config.md) : `GET /network/{NetworkID}/camera/{CameraID}/config`
* [Update Camera Config](camera/update-config.md) : `POST /network/{NetworkID}/camera/{CameraID}/update`


### Clips

* [Get Clip Events](clip/get-clip-events.md) : `GET /api/v1/accounts/{AccountID}/media/changed?since={timestamp}&page={PageNumber}`
* [Get Clip](clip/get-clip.md) : `GET /api/v2/accounts/{AccountID}/media/clip/{mp4_Filename}`
* [Get Clip Thumbnail](clip/get-clip-thumbnail.md) : `GET /api/v2/accounts/{AccountID}/media/thumb/{jpg_filename}`
* [Set Clip Options](clip/set-clip-options.md) : `POST /api/v1/account/video_options`
* [Delete Clips](clip/delete-clip.md) : `POST /api/v1/accounts/{AccountID}/media/delete`


### Misc

* [App Version Check](misc/version.md) : `GET /api/v1/version`
* [Get Regions](misc/regions.md) : `GET /regions?locale={Two Character Country Locale}`
* [Upload Logs](misc/upload-logs.md) : `POST /app/logs/upload`
* [Account Options](misc/account-options.md) : `GET /api/v1/account/options`
