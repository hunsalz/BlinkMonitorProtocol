#!/usr/bin/env python3
"""
A simple example to demonstrate the Blink API protocol:
Download available videos from a Blink account.

Usage:
    python blinkVideoDownloader.py <email> <password> [since_timestamp]

Arguments:
    email: Blink account email
    password: Blink account password
    since_timestamp: (optional) ISO timestamp to fetch videos since.
                     Default: 1970-01-01T00:00:00+0000 (all videos)
                     Example: 2024-01-01T00:00:00+0000
"""

import requests
import shutil
import os
import sys
import json
import time
from datetime import datetime
import pytz

# Default timestamp (epoch) to fetch all available videos
DEFAULT_SINCE = "1970-01-01T00:00:00+0000"


def validate_email(email):
    """Basic email validation."""
    return '@' in email and '.' in email.split('@')[1]


def login(email, password):
    """Login to Blink API and return auth token, region, and account ID."""
    headers = {
        'Host': 'rest-prod.immedia-semi.com',
        'Content-Type': 'application/json',
    }
    
    # Use json.dumps to properly escape special characters
    data = json.dumps({
        "email": email,
        "password": password
    })
    
    try:
        # Use API v5 as documented in README
        res = requests.post(
            'https://rest-prod.immedia-semi.com/api/v5/account/login',
            headers=headers,
            data=data,
            timeout=30
        )
        res.raise_for_status()
        
        response_json = res.json()
        
        # Handle different response structures (v4 vs v5)
        if "auth" in response_json and "token" in response_json["auth"]:
            authToken = response_json["auth"]["token"]
        elif "authtoken" in response_json and "authtoken" in response_json["authtoken"]:
            authToken = response_json["authtoken"]["authtoken"]
        else:
            raise ValueError("Could not find auth token in response")
        
        # Handle different response structures for region/tier
        if "account" in response_json and "tier" in response_json["account"]:
            region = response_json["account"]["tier"]
        elif "region" in response_json and "tier" in response_json["region"]:
            region = response_json["region"]["tier"]
        else:
            raise ValueError("Could not find region/tier in response")
        
        if "account" in response_json:
            accountID = response_json["account"].get("account_id") or response_json["account"].get("id")
        else:
            raise ValueError("Could not find account ID in response")
        
        return authToken, region, accountID
    
    except requests.exceptions.RequestException as e:
        print(f"Error during login: {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except (KeyError, ValueError) as e:
        print(f"Error parsing login response: {e}", file=sys.stderr)
        print(f"Response: {res.text}", file=sys.stderr)
        sys.exit(1)


def get_homescreen(host, accountID, authToken):
    """Get homescreen data to retrieve network information."""
    headers = {
        'Host': host,
        'TOKEN_AUTH': authToken,
    }
    
    try:
        res = requests.get(
            f'https://{host}/api/v3/accounts/{accountID}/homescreen',
            headers=headers,
            timeout=30
        )
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting homescreen: {e}", file=sys.stderr)
        sys.exit(1)


def download_videos(host, accountID, authToken, since_timestamp):
    """Download all videos since the given timestamp."""
    headers = {
        'Host': host,
        'TOKEN_AUTH': authToken,
    }
    
    fileFormat = "%Y-%m-%d %H-%M-%S"
    pageNum = 1
    
    while True:
        time.sleep(0.25)  # Rate limiting
        
        pageNumUrl = (
            f'https://{host}/api/v1/accounts/{accountID}/media/changed'
            f'?since={since_timestamp}&page={pageNum}'
        )
        
        print(f"## Processing page - {pageNum} ##")
        
        try:
            res = requests.get(pageNumUrl, headers=headers, timeout=30)
            res.raise_for_status()
            response_json = res.json()
            videoListJson = response_json.get("media", [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching video list: {e}", file=sys.stderr)
            break
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error parsing response: {e}", file=sys.stderr)
            break
        
        if not videoListJson:
            print(" * ALL DONE !! *")
            break
        
        for videoJson in videoListJson:
            try:
                mp4Url = f'https://{host}{videoJson["media"]}'
                datetime_object = datetime.strptime(
                    videoJson["created_at"],
                    '%Y-%m-%dT%H:%M:%S+00:00'
                )
                utcmoment = datetime_object.replace(tzinfo=pytz.utc)
                localDatetime = utcmoment.astimezone(
                    pytz.timezone(videoJson["time_zone"])
                )
                fileName = (
                    localDatetime.strftime(fileFormat) + " - " +
                    videoJson["device_name"] + " - " +
                    videoJson["network_name"] + ".mp4"
                )
                
                if os.path.isfile(fileName):
                    print(f" * Skipping {fileName} *")
                else:
                    print(f"Saving - {fileName}")
                    try:
                        res = requests.get(
                            mp4Url,
                            headers=headers,
                            stream=True,
                            timeout=60
                        )
                        res.raise_for_status()
                        
                        with open("tmp-download", 'wb') as out_file:
                            shutil.copyfileobj(res.raw, out_file)
                        os.rename("tmp-download", fileName)
                    except requests.exceptions.RequestException as e:
                        print(f"Error downloading {fileName}: {e}", file=sys.stderr)
                        if os.path.exists("tmp-download"):
                            os.remove("tmp-download")
            except (KeyError, ValueError) as e:
                print(f"Error processing video: {e}", file=sys.stderr)
                continue
        
        pageNum += 1


def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    
    email = sys.argv[1]
    password = sys.argv[2]
    since_timestamp = sys.argv[3] if len(sys.argv) == 4 else DEFAULT_SINCE
    
    # Basic input validation
    if not validate_email(email):
        print("Error: Invalid email format", file=sys.stderr)
        sys.exit(1)
    
    if not password:
        print("Error: Password cannot be empty", file=sys.stderr)
        sys.exit(1)
    
    # Login
    print("Logging in...")
    authToken, region, accountID = login(email, password)
    print(f"Region: {region} AuthToken: {authToken[:20]}... Account ID: {accountID}")
    
    # Determine host based on region
    host = f'rest-{region}.immedia-semi.com'
    
    # Get homescreen to verify connection
    homescreen = get_homescreen(host, accountID, authToken)
    if "networks" in homescreen and homescreen["networks"]:
        networkID = homescreen["networks"][0]["id"]
        print(f"Network - {networkID}")
    else:
        print("Warning: No networks found", file=sys.stderr)
    
    # Download videos
    print(f"Fetching videos since {since_timestamp}...")
    download_videos(host, accountID, authToken, since_timestamp)


if __name__ == "__main__":
    main()
