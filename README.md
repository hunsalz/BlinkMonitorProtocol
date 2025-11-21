# BlinkMonitorProtocol

Unofficial documentation for the Client API of the Blink Wire-Free HD Home Monitoring &amp; Alert System. I am not affiliated with the company in any way - this documentation is strictly **"AS-IS"**.

The Client API is a straightforward REST API using JSON and HTTPS.

## Table of Contents

- [Getting Started](#getting-started)
- [Overview](#overview)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
  - [API v1](#api-v1)
  - [API v2](#api-v2)
  - [API v3](#api-v3)
  - [API v5](#api-v5)
  - [Unversioned Endpoints](#unversioned-endpoints)
- [Version Compatibility & Evolution](#version-compatibility--evolution)
- [Contributing](#contributing)

## Getting Started

1. **Set up authentication**: See the [Authentication Guide](AUTHENTICATION.md) for complete OAuth Bearer token setup instructions
2. **Configure environment**: Copy [`.env.template`](.env.template) to `.env` and fill in your credentials
3. **Make your first API call**: Start with the [HomeScreen](v3/accounts/homescreen.md) endpoint to get your account information

**Prerequisites:**
- Blink account credentials
- `curl` command-line tool (or any HTTP client)
- `jq` command-line tool (for pretty-printing JSON responses) - [Installation guide](https://stedolan.github.io/jq/download/)
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

Endpoints are organized by API version and resource path.

**📚 Version Compatibility & Evolution:**
- [Version Response Variations](plan/VERSION_RESPONSE_VARIATIONS.md) - Detailed comparison of response differences between API versions
- [Version Compatibility Report](plan/COMPATIBILITY_REPORT.md) - Complete compatibility testing results across all versions
- **API Evolution:** The API has evolved over time with different path structures. Unversioned endpoints (`/network/...`, `/client/...`) represent an earlier design that continues to be supported alongside the versioned structure (`/api/v1/...`, `/api/v2/...`, etc.). See individual endpoint documentation for evolution notes.

### API v1

#### Accounts (`/api/v1/accounts/...`)

* [Get Account Info](v1/accounts/get-account-info.md) : `GET /api/v1/accounts/{AccountID}/info`
* [Get Account Notification Flags](v1/accounts/get-notifications.md) : `GET /api/v1/accounts/{AccountID}/notifications/configuration`
* [Set Notification Flags](v1/accounts/set-notifications.md) : `POST /api/v1/accounts/{AccountID}/notifications/configuration`
* [Get Client Options](v1/accounts/get-client-options.md) : `GET /api/v1/accounts/{AccountID}/clients/{ClientID}/options`
* [Arm System](v1/accounts/arm.md) : `POST /api/v1/accounts/{AccountID}/networks/{NetworkID}/state/arm`
* [Disarm System](v1/accounts/disarm.md) : `POST /api/v1/accounts/{AccountID}/networks/{NetworkID}/state/disarm`
* [Set OWL Thumbnail](v1/accounts/set-owl-thumbnail.md) : `POST /api/v1/accounts/{AccountID}/networks/{NetworkID}/owls/{CameraID}/thumbnail`
* [Snooze Camera](v1/accounts/snooze.md) : `POST /api/v1/accounts/{AccountID}/networks/{NetworkID}/cameras/{CameraID}/snooze`
* [Get Clip Events](v1/accounts/get-clip-events.md) : `GET /api/v1/accounts/{AccountID}/media/changed?since={timestamp}&page={PageNumber}`
* [Delete Clips](v1/accounts/delete-clip.md) : `POST /api/v1/accounts/{AccountID}/media/delete`

#### Networks (`/api/v1/networks/...`)

* [List Schedules](v1/networks/list-programs.md) : `GET /api/v1/networks/{NetworkID}/programs`
* [Enable Schedule](v1/networks/enable-program.md) : `POST /api/v1/networks/{NetworkID}/programs/{ProgramID}/enable`
* [Disable Schedule](v1/networks/disable-program.md) : `POST /api/v1/networks/{NetworkID}/programs/{ProgramID}/disable`
* [Update Schedule](v1/networks/update-program.md) : `POST /api/v1/networks/{NetworkID}/programs/{ProgramID}/update`

#### Account (`/api/v1/account/...`)

* [Get Account Options](v1/account/get-account-options.md) : `GET /api/v1/account/options`
* [Set Clip Options](v1/account/set-clip-options.md) : `POST /api/v1/account/video_options`

#### Users (`/api/v1/users/...`)

* [Get User Tier Info](v1/users/get-tier-info.md) : `GET /api/v1/users/tier_info`

#### Camera (`/api/v1/camera/...`)

* [Get Camera Usage](v1/camera/get-usage.md) : `GET /api/v1/camera/usage`

#### Version (`/api/v1/version`)

* [App Version Check](v1/version/version.md) : `GET /api/v1/version`

### API v2

#### Accounts (`/api/v2/accounts/...`)

* [Get Clip](v2/accounts/get-clip.md) : `GET /api/v2/accounts/{AccountID}/media/clip/{mp4_Filename}`
* [Get Clip Thumbnail](v2/accounts/get-clip-thumbnail.md) : `GET /api/v2/accounts/{AccountID}/media/thumb/{jpg_filename}`

### API v3

#### Accounts (`/api/v3/accounts/...`)

* [HomeScreen](v3/accounts/homescreen.md) : `GET /api/v3/accounts/{AccountID}/homescreen`

### API v5

#### Accounts (`/api/v5/accounts/...`)

* [Liveview](v5/accounts/liveview.md) : `POST /api/v5/accounts/{AccountID}/networks/{NetworkID}/cameras/{CameraID}/liveview`

### Unversioned Endpoints

Endpoints that use unversioned paths (no `/api/v1/`, `/api/v2/`, etc.). These represent a different path structure that evolved alongside the versioned API.

#### Network-Scoped (`/network/{NetworkID}/...`)

* [Network Info](unversioned/network/get-network.md) : `GET /network/{NetworkID}`
* [Command Status](unversioned/network/command.md) : `GET /network/{NetworkID}/command/{CommandID}`
* [Get Network Sync Modules](unversioned/network/get-syncmodules.md) : `GET /network/{NetworkID}/syncmodules`
* [Enable Motion Detection](unversioned/network/camera/enable.md) : `POST /network/{NetworkID}/camera/{CameraID}/enable`
* [Disable Motion Detection](unversioned/network/camera/disable.md) : `POST /network/{NetworkID}/camera/{CameraID}/disable`
* [Create New Thumbnail](unversioned/network/camera/set-thumbnail.md) : `POST /network/{NetworkID}/camera/{CameraID}/thumbnail`
* [Record Clip from Camera](unversioned/network/camera/record-clip.md) : `POST /network/{NetworkID}/camera/{CameraID}/clip`
* [Get Camera Config](unversioned/network/camera/get-config.md) : `GET /network/{NetworkID}/camera/{CameraID}/config`
* [Get Camera Signals](unversioned/network/camera/get-signals.md) : `GET /network/{NetworkID}/camera/{CameraID}/signals`
* [Update Camera Config](unversioned/network/camera/update-config.md) : `POST /network/{NetworkID}/camera/{CameraID}/update`

#### Client-Scoped (`/client/{ClientID}/...`)

* [Set Client Options](unversioned/client/update-options.md) : `POST /client/{ClientID}/update`

#### Application-Level (`/app/...`)

* [Upload Logs](unversioned/app/upload-logs.md) : `POST /app/logs/upload`

#### Public Endpoints (No Authentication)

* [Get Regions](unversioned/public/regions.md) : `GET /regions?locale={Two Character Country Locale}`

## Version Compatibility & Evolution

### Version Compatibility

The Blink API has evolved over time, and endpoints may be available in multiple versions with varying response structures:

- **Backward Compatible Endpoints:**
  - Account Info: Works with v1 and v2 (v2 adds additional fields)

- **Version-Specific Endpoints:**
  - Most endpoints are specific to their documented version
  - Unversioned endpoints work across all versions

See [Version Compatibility Report](plan/COMPATIBILITY_REPORT.md) for complete testing results.

### Response Variations

When an endpoint is available in multiple versions, the response structure may differ:

- **Account Info (v1 vs v2):** v2 adds phone, email, Ring integration fields

See [Version Response Variations](plan/VERSION_RESPONSE_VARIATIONS.md) for detailed field-by-field comparisons.

### API Evolution

The API uses two path structure patterns that evolved alongside each other:

1. **Versioned Structure** (`/api/v1/...`, `/api/v2/...`, etc.)
   - Explicit versioning in the path
   - Account-scoped operations
   - Modern design pattern

2. **Unversioned Structure** (`/network/...`, `/client/...`, `/app/...`)
   - No version prefix
   - Resource-scoped operations
   - Earlier design pattern, still fully supported

Both structures are actively supported. Unversioned endpoints are not deprecated - they represent an alternative API design that continues to work. Some operations may only be available in one structure (e.g., OWL camera thumbnails are versioned, regular camera thumbnails are unversioned).

## Contributing

PR's welcome! This is an unofficial documentation project maintained by the community.

When contributing:
- Follow the existing documentation structure and format
- Include complete working examples with authentication
- Test all examples before submitting
- Use kebab-case for file names
- Reference the [Authentication Guide](AUTHENTICATION.md) for authentication patterns
