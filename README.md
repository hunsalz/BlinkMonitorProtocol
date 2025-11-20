# BlinkMonitorProtocol

Unofficial documentation for the Client API of the Blink Wire-Free HD Home Monitoring &amp; Alert System. I am not affiliated with the company in any way - this documentation is strictly **"AS-IS"**.

The Client API is a straightforward REST API using JSON and HTTPS.

## Table of Contents

- [Getting Started](#getting-started)
- [Overview](#overview)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
  - [System](#system)
  - [Network](#network)
  - [Cameras](#cameras)
  - [Clips](#clips)
- [Contributing](#contributing)

## Getting Started

1. **Set up authentication**: See the [Authentication Guide](AUTHENTICATION.md) for complete OAuth Bearer token setup instructions
2. **Configure environment**: Copy [`.env.template`](.env.template) to `.env` and fill in your credentials
3. **Make your first API call**: Start with the [HomeScreen](system/homescreen.md) endpoint to get your account information

**Prerequisites:**
- Blink account credentials
- `curl` command-line tool (or any HTTP client)
- Shell environment (bash/zsh)

## Overview

* **Initial server URL** - https://rest-prod.immedia-semi.com
* **Account** - An account corresponds to a single set of login credentials. The Account ID is returned in the homescreen call.
* **Client** - A unique client/app to the account. A single account may have many client apps. The Client ID is obtained from your OAuth token response.
* **Network** - A single account may have many networks. A network corresponds conceptually to a Blink Synch module. An account could have multiple networks/synch modules - e.g. multiple sites/homes. Network and Synch Module information associated with an account is returned in the homescreen call.
* **Camera** - A network (synch module) may have one or more cameras. Camera information is returned in the homescreen call.
* **Command** - Some operations reach out from the Blink Servers to your local Blink module.  These operations are asynchronous and return a Command ID to be polled for completion via the Command Status call.

## Authentication

**⚠️ Important**: All endpoints require OAuth 2.0 Bearer token authentication.

* **[Authentication Guide](AUTHENTICATION.md)** - **Start here** - Complete guide to OAuth Bearer token authentication, including initial login, token refresh, and troubleshooting
* **[`.env.template`](.env.template)** - Template for environment variables configuration

All endpoint documentation includes complete working examples with authentication.

## API Endpoints

### System

* [HomeScreen](system/homescreen.md) : `GET /api/v3/accounts/{AccountID}/homescreen`
* [Get Account Info](system/get-account-info.md) : `GET /api/v1/accounts/{AccountID}/info`
* [Get Account Notification Flags](system/get-notifications.md) : `GET /api/v1/accounts/{AccountID}/notifications/configuration`
* [Set Notification Flags](system/set-notifications.md) : `POST /api/v1/accounts/{AccountID}/notifications/configuration`
* [Get Client Options](system/options.md) : `GET /api/v1/accounts/{AccountID}/clients/{ClientID}/options`
* [Set Client Options](system/update-options.md) : `POST /client/{ClientID}/update`
* [Get Account Options](system/get-account-options.md) : `GET /api/v1/account/options`
* [App Version Check](system/version.md) : `GET /api/v1/version`
* [Get Regions](system/regions.md) : `GET /regions?locale={Two Character Country Locale}`
* [Upload Logs](system/upload-logs.md) : `POST /app/logs/upload`


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

## Contributing

PR's welcome! This is an unofficial documentation project maintained by the community.

When contributing:
- Follow the existing documentation structure and format
- Include complete working examples with authentication
- Test all examples before submitting
- Use kebab-case for file names
- Reference the [Authentication Guide](AUTHENTICATION.md) for authentication patterns
