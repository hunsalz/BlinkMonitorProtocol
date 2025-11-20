# BlinkMonitorProtocol
Unofficial documentation for the Client API of the Blink Wire-Free HD Home Monitoring &amp; Alert System. I am not affiliated with the company in any way - this documentation is strictly **"AS-IS"**.

The Client API is a straightforward REST API using JSON and HTTPS.

When APIs no longer appear in the current versions of the mobile Apps, we assume they are deprecated and mark them as such in this doc.

When Blink obsoletes an API, they do not remove it, but return the message "An app update is required".  This presumably triggers logic in the mobile clients to users that they must update to a more current version of the client to restore functionality.

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
  - Used by the [blinkpy library](https://github.com/fronzbot/blinkpy) and is the recommended approach

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
    * see [Login](auth/login.md) for notes on possible redirection to a locale specific server after login.
* **Authentication** - ⚠️ **Important**: Blink now uses **OAuth 2.0 Bearer token** authentication. The REST API session token method (TOKEN_AUTH header) is deprecated and no longer works. See [Authentication Guide](AUTHENTICATION.md) for complete details on how to authenticate and use OAuth Bearer tokens.
* **Account** - An account corresponds to a single set of login credentials. The Account ID is returned in a successful login response.
* **Client** - A unique client/app to the account. A single account may have many client apps. Clients that the Blink servers believe are new will generate an out-of-band PIN OTP workflow.  The Client ID is returned in a successful login response.
* **Network** - A single account may have many networks. A network corresponds conceptually to a Blink Synch module. An account could have multiple networks/synch modules - e.g. multiple sites/homes. Network and Synch Module information associated with an account is returned in the homescreen call.
* **Camera** - A network (synch module) may have one or more cameras. Camera information is returned in the homescreen call.
* **Command** - Some operations reach out from the Blink Servers to your local Blink module.  These operations are asynchronous and return a Command ID to be polled for completion via the Command Status call.


### Authentication

**⚠️ Important**: All endpoints now require OAuth 2.0 Bearer token authentication. See [Authentication Guide](AUTHENTICATION.md) for complete documentation.

* [Authentication Guide](AUTHENTICATION.md) - **Start here** - Complete guide to OAuth Bearer token authentication
* [Login](auth/login.md) : `POST /api/v5/account/login` - ⚠️ **Deprecated** - Returns "An app update is required"
* [Logout](auth/logout.md) : `POST /api/v4/account/{AccountID}/client/{clientID}/logout`
* [Verify Pin](auth/verifyPin.md) : `POST /api/v4/account/{AccountID}/client/{ClientID}/pin/verify`


### System

* [HomeScreen](system/homescreen.md) : `GET /api/v3/accounts/{AccountID}/homescreen`
* [Get Account Notification Flags](system/getNotifications.md) : `GET /api/v1/accounts/{AccountID}/notifications/configuration`
* [Set Notification Flags](system/setNotifications.md) : `POST /api/v1/accounts/{AccountID}/notifications/configuration`
* [Get Client Options](system/options.md) : `GET /api/v1/accounts/{AccountID}/clients/{ClientID}/options`
* [Set Client Options](system/updateoptions.md) : `POST /api/v1/accounts/{AccountID}/clients/{ClientID}/update`


### Network

* [Command Status](network/command.md) : `GET /network/{NetworkID}/command/{CommandID}`
* [Arm System](network/arm.md) : `POST /api/v1/accounts/{AccountID}/networks/{NetworkID}/state/arm`
* [Disarm System](network/disarm.md) : `POST /api/v1/accounts/{AccountID}/networks/{NetworkID}/state/disarm`
* [List Schedules](network/listPrograms.md) : `GET /api/v1/networks/{NetworkID}/programs`
* [Enable Schedule](network/enableProgram.md) : `POST /api/v1/networks/{NetworkID}/programs/{ProgramID}/enable`
* [Disable Schedule](network/disableProgram.md) : `POST /api/v1/networks/{NetworkID}/programs/{ProgramID}/disable`
* [Update Schedule](network/updateProgram.md) : `POST /api/v1/networks/{NetworkID}/programs/{ProgramID}/update`
* ~~List Networks (obsolete): `GET /networks`~~
* ~~List Synch Modules (obsolete) `GET /network/{NetworkID}/syncmodules`~~


### Cameras

* [Enable Motion Detection](camera/enable.md) : `POST /network/{NetworkID}/camera/{CameraID}/enable`
* [Disable Motion Detection](camera/disable.md) : `POST /network/{NetworkID}/camera/{CameraID}/disable`
* [Get Current Thumbnail](camera/getThumbnail.md) : `GET /media/production/account/{AccountID}/network/{NetworkID}/camera/{CameraID}/{JPEG_File_Name}.jpg`
* [Create New Thumbnail](camera/setThumbnail.md) : `POST /network/{NetworkID}/camera/{CameraID}/thumbnail`
* [Liveview](camera/liveview.md) : `POST /api/v5/accounts/{AccountID}/networks/{NetworkID}/cameras/{CameraID}/liveview`
* [Record Video Clip from Camera](camera/recordClip.md) : `POST /network/{NetworkID}/camera/{CameraID}/clip`
* [Snooze Camera](camera/snooze.md) : `POST /api/v1/accounts/{AccountID}/networks/{NetworkID}/cameras/{CameraID}/snooze`
* [Get Camera Config](camera/getConfig.md) : `GET /network/{NetworkID}/camera/{CameraID}/config`
* [Update Camera Config](camera/updateConfig.md) : `POST /network/{NetworkID}/camera/{CameraID}/update`
* ~~Get Camera List (obsolete - replaced by HomeScreen) - `GET /network/{NetworkID}/cameras`~~
* Get Camera Info (deprecated? - replaced by HomeScreen) - `GET /network/{NetworkID}/camera/{CameraID}`
* Get Camera Sensor Info (deprecated? - replaced by HomeScreen) - `GET /network/{NetworkID}/camera/{CameraID}/signals`


### Videos

* [Get Video Events](video/getVideoEvents.md) : `GET /api/v1/accounts/{AccountID}/media/changed?since={timestamp}&page={PageNumber}`
* [Get Video](video/getVideo.md) : `GET /api/v2/accounts/{AccountID}/media/clip/{mp4_Filename}`
* [Get Video Thumbnail](video/getVideoThumbnail.md) : `GET /api/v2/accounts/{AccountID}/media/thumb/{jpg_filename}`
* [Set Video Options](video/setVideoOptions.md) : `POST /api/v1/account/video_options`
* [Delete Videos](video/deleteVideos.md) : `POST /api/v1/accounts/{AccountID}/media/delete`
* ~~Get Network events (obsolete replaced by Get Video Events) - `GET /events/network/{NetworkID}`~~
* ~~Get Video Count (obsolete) - `GET /api/v2/videos/count`~~
* ~~Get Video Info by Page (obsolete) - `GET /api/v2/videos/page/{PageNumber}`~~
* ~~Get Video by ID (obsolete) - `GET /api/v2/video/{VideoID}`~~
* ~~Get Unwatched Videos (obsolete) - `GET /api/v2/videos/unwatched`~~
* ~~Delete a Video (obsolete) - `POST /api/v2/video/{VideoID}/delete`~~


### Misc

* [App Version Check](Misc/version.md) : `GET /api/v1/version`
* [Get Regions](Misc/regions.md) : `GET /regions?locale={Two Character Country Locale}`
* [Upload Logs](Misc/uploadLogs.md) : `POST /app/logs/upload`
* [Account Options](Misc/accountOptions.md) : `GET /api/v1/account/options`
* System Health (deprecated?) :  `GET /health`
* ~~Clients (obsolete) : `GET /account/clients`~~


### Implementations

* [BlinkPy - A Python library for the Blink Camera system](https://github.com/fronzbot/blinkpy)
* [node-blink-security - A node.js implementation](https://github.com/madshall/node-blink-security)
