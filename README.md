![logo](https://yk-website-images.s3.eu-west-1.amazonaws.com/LogoV4_TRANSPARENT.png?)

# Flask + Youverse Hosted Login

This example shows you how to use Flask to log in to your application with a Youverse Hosted Login page (OIDC protocol).

The login is achieved through the authorization code flow, where the user is redirected to the Youverse-Hosted login page.
After the user authenticates, he is redirected back to the application with an access code that is then exchanged for access and id tokens.

> Requires Python version 3.6.0 or higher.

## Running This Example

To run this application, you first need to clone this repo:

```bash
git clone https://github.com/dev-yoonik/yoonik-oidc-example-python.git
cd yoonik-oidc-example-python
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

Copy the [`client_secrets.json.dist`](client_secrets.json.dist) to `client_secrets.json`:

```bash
cp client_secrets.json.dist client_secrets.json
```

You now need to contact [Youverse support](mailto:support@youverse.id) to request the following information:

- **Client ID** and **Client Secret**.
- **Youverse Server Domain** - This is the URL of the authorization server that will perform authentication.

Fill in the information that you gathered in the `client_secrets.json` file.

```json
{
  "auth_uri": "https://{YouverseServerDomain}/oauth/authorize",
  "client_id": "{yourClientId}",
  "client_secret": "{yourClientSecret}",
  "token_uri": "https://{YouverseServerDomain}/oauth/token",
  "userinfo_uri": "https://{YouverseServerDomain}/oauth/userinfo"
}
```

Start the app server:

```
python main.py
```

Now navigate to http://localhost:8080 in your browser.

If you see a home page that prompts you to log in, then things are working! Clicking the **Log in** button will redirect you to the Youverse hosted sign-in page.
