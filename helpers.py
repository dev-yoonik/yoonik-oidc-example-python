import json
from jose import jwt
from six.moves.urllib.request import urlopen


def load_config(fname='./client_secrets.json'):
    config = None
    with open(fname) as f:
        config = json.load(f)
    return config


config = load_config()

ISSUER = "https://accounts.youverse.id"
jwks_json_url = urlopen(ISSUER + "/oauth/jwks")
JWKS = json.loads(jwks_json_url.read())


def decode_token(token):
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError as jwt_error:
        print(f"Invalid header. {str(jwt_error)}")
        return None
    if unverified_header["alg"] == "HS256":
        print("Invalid header. Use an RS256 signed JWT Access Token.")
        return None

    rsa_key = {}
    for key in JWKS["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if not rsa_key:
        print("Unable to find appropriate key.")
        return None

    payload = None
    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=config["client_id"],
            issuer=ISSUER
        )
    except jwt.ExpiredSignatureError as expired_sign_error:
        print(f"Token is expired: {str(expired_sign_error)}")
    except jwt.JWTClaimsError as jwt_claims_error:
        print(f"Incorrect claims: {str(jwt_claims_error)}")
    except Exception as exc:
        print(f"Unable to parse authentication token: {str(exc)}")

    return payload
