import requests
import json

# Replace with your actual ConnectLife credentials
USERNAME = "your-email@example.com"
PASSWORD = "your-password"

# Constants
API_KEY = "4_yhTWQmHFpZkQZDSV1uV-_A"
CLIENT_ID = "5065059336212"
CLIENT_SECRET = "07swfKgvJhC3ydOUS9YV_SwVz0i4LKqlOLGNUukYHVMsJRF1b-iWeUGcNlXyYCeK"
LOGIN_URL = "https://accounts.eu1.gigya.com/accounts.login"
JWT_URL = "https://accounts.eu1.gigya.com/accounts.getJWT"
AUTHORIZE_URL = "https://oauth.hijuconn.com/oauth/authorize"
TOKEN_URL = "https://oauth.hijuconn.com/oauth/token"
APPLIANCES_URL = "https://connectlife.bapi.ovh/appliances"


def login_gigya(username, password):
    print("[1] Logging in to Gigya...")
    payload = {
        "loginID": username,
        "password": password,
        "APIKey": API_KEY,
    }
    resp = requests.post(LOGIN_URL, data=payload)
    data = resp.json()
    if resp.status_code != 200 or "sessionInfo" not in data:
        raise Exception(f"Gigya login failed: {data}")
    return data["sessionInfo"]["cookieValue"], data.get("UID")


def get_jwt(login_token):
    print("[2] Getting JWT token...")
    payload = {
        "APIKey": API_KEY,
        "login_token": login_token,
    }
    resp = requests.post(JWT_URL, data=payload)
    data = resp.json()
    id_token = data.get("id_token")
    if not id_token:
        raise Exception(f"JWT retrieval failed: {data}")
    return id_token


def authorize_hijuconn(id_token, uid):
    print("[3] Authorizing with HiJuConn...")
    payload = {
        "client_id": CLIENT_ID,
        "redirect_uri": "https://api.connectlife.io/swagger/oauth2-redirect.html",
        "idToken": id_token,
        "response_type": "code",
        "thirdType": "CDC",
        "thirdClientId": uid,
    }
    resp = requests.post(AUTHORIZE_URL, json=payload)
    data = resp.json()
    code = data.get("code")
    if not code:
        raise Exception(f"Authorize failed: {data}")
    return code


def exchange_code_for_token(code):
    print("[4] Exchanging code for access token...")
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": "https://api.connectlife.io/swagger/oauth2-redirect.html",
        "grant_type": "authorization_code",
        "code": code,
    }
    resp = requests.post(TOKEN_URL, data=payload)
    data = resp.json()
    access_token = data.get("access_token")
    if not access_token:
        raise Exception(f"Token exchange failed: {data}")
    return access_token, data.get("expires_in")


def get_appliances(access_token):
    print("[5] Fetching appliances...")
    headers = {
        "User-Agent": "connectlife-api-connector 2.1.4",
        "X-Token": access_token,
    }
    resp = requests.get(APPLIANCES_URL, headers=headers)
    if resp.status_code != 200:
        raise Exception(f"Failed to fetch appliances: {resp.status_code}, {resp.text}")
    return resp.json()


def main():
    # Step 1: Gigya login
    login_token, uid = login_gigya(USERNAME, PASSWORD)

    # Step 2: Get JWT
    id_token = get_jwt(login_token)

    # Step 3: Authorize HiJuConn
    code = authorize_hijuconn(id_token, uid)

    # Step 4: Exchange code for token
    access_token, expires_in = exchange_code_for_token(code)
    print(f"Access token retrieved. Expires in {expires_in} seconds.")

    # Step 5: Fetch appliances
    appliances = get_appliances(access_token)
    print(json.dumps(appliances, indent=2))


if __name__ == "__main__":
    main()
