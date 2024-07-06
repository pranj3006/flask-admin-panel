"""
Util for verifying JWT Token
"""

import os
import base64
import traceback
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import jwt
import requests

CLIENT_ID = os.environ.get("CLIENT_ID", "")
TENANT_ID = os.environ.get("TENANT_ID", "")


def ensure_bytes(key):
    """
    Ensures that key is in bytes format.
    If key is string then encodes to bytes using utf-8 encoding
    """
    if isinstance(key, str):
        key = key.encode("utf-8")
    return key


def decode_value(val):
    """
    Decodes base64 urlsafe encoded string and converts it to an integer
    """
    decoded = base64.urlsafe_b64decode(ensure_bytes(val) + b"==")
    return int.from_bytes(decoded, "big")


def rsa_pem_from_jwk(jwk):
    """
    Generates RSA public key in PEM format from a JSON Web Key
    """
    return (
        RSAPublicNumbers(n=decode_value(jwk["n"]), e=decode_value(jwk["e"]))
        .public_key(default_backend())
        .public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )


class InvalidAuthorizationToken(Exception):
    """
    Exception class for invalid JWT tokens
    """

    def __init__(self, details):
        super().__init__("Invalid authorization token: " + details)


def get_kid(token):
    """
    Get key id, to find which key was used to sign the token
    """
    headers = jwt.get_unverified_header(token)
    if not headers:
        raise InvalidAuthorizationToken("missing headers")
    try:
        return headers["kid"]
    except KeyError as e:
        raise InvalidAuthorizationToken("missing kid") from e


def get_jwk(jwks_response, kid):
    """
    Return JSON Web Key associated with key id
    """
    for jwk in jwks_response.get("keys"):
        if jwk.get("kid") == kid:
            return jwk
    raise InvalidAuthorizationToken("kid not recognized")


def get_public_key(jwks_response, token):
    """
    Return public key used in JWT
    """
    return rsa_pem_from_jwk(get_jwk(jwks_response, get_kid(token)))


def validate_jwt(jwks_response, jwt_to_validate):
    """
    Validate JWT signature
    """
    public_key = get_public_key(jwks_response, jwt_to_validate)
    valid_audiences = ["api://" + CLIENT_ID]
    decoded = jwt.decode(
        jwt_to_validate,
        public_key,
        verify=True,
        algorithms=["RS256"],
        audience=valid_audiences,
        issuer=f"https://sts.windows.net/{TENANT_ID}/",
    )
    # do what you wish with decoded token:
    # if we get here, the JWT is validated
    return decoded


def verify_token(token):
    """
    Verifies JWT token
    """
    open_id_metadata_url = (
        f"https://login.microsoftonline.com/{TENANT_ID}/"
        "/v2.0/.well-known/openid-configuration"
    )
    r = requests.get(open_id_metadata_url, timeout=3)
    metadata_response = r.json()
    response_error = metadata_response.get("error", None)
    if response_error:
        return None, response_error
    jwks_uri = metadata_response["jwks_uri"]
    r = requests.get(jwks_uri, timeout=3)
    jwks_response = r.json()
    # configuration, these can be seen in valid JWTs from Azure B2C:
    if not token:
        return None, "No token"
    try:
        decoded = validate_jwt(jwks_response, token)
    except jwt.exceptions.ExpiredSignatureError:
        return None, "TOKEN_EXPIRED"
    except jwt.exceptions.DecodeError as error:
        return None, f"TOKEN_DECODE_ERROR {error}"
    except Exception as e:
        traceback.print_exc()
        return None, str(e)
    # Access enabled for effem. If need access to other domain add it below
    if decoded["unique_name"].split("@")[1] == "effem.com":
        return decoded, None
    return None, "Only effem user allowed"