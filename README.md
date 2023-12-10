# cleveroauth
Proof-of-concept for utilizing Clever's OAuth2 API to authenticate users and retrieve data from Clever's API.

## Setup
1. Clone this repository
2. Install dependencies with `pip install -r requirements.txt`
3. Create a .env file with the content from .env.example, you will need to create a Clever Developer Account to be able to do this, and the Client ID and Client Secret can be found in the [Clever Developer Dashboard](https://dev.clever.com/information/getting_started) under the "OAuth" tab. The REDIRECT_URI should be set to `http://localhost:3000/oauth/clever`.
4. Run the server with `python main.py`

## Usage
1. Navigate to `http://localhost:3000/` in your browser
2. Click the "Login with Clever" button
3. Login with clever utilizing the mock data and the mock district
4. You should be redirected to a page that displays the user's name, email and district name
5. Done!

## Notes
- This is a proof-of-concept, so there is no database but there is a cookie utilizing JWT that expires after the session ends.
- The data is retrieved from Clever's API and then stored and signed with the JWT cookie, so if the user's data changes in Clever, it will not be reflected in the application until the user logs out and logs back in.

## Requirements
- Python 3.10+
- Clever Developer Account
- Clever Client ID and Client Secret
- Clever District Student Account
- Requests
- Flask
- Python-dotenv
- PyJWT

## License
MIT