import jwt
import warnings

from datetime import datetime

from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_get_secret_key
from .makejson import MakeJSON


def jwt_payload_handler(user):
    warnings.warn(
        'The following fields will be removed in the future: '
        '`email` and `user_id`. ',
        DeprecationWarning
    )

    payload = {
        "user_id": user.pk,
        "exp": datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }

    return payload


def jwt_encode_handler(payload):
    key = api_settings.JWT_PRIVATE_KEY or jwt_get_secret_key(payload)
    return jwt.encode(
        payload,
        key,
        api_settings.JWT_ALGORITHM
    ).decode("utf-8")


def jwt_decode_handler(token):
    options = {
        'verify_exp': api_settings.JWT_VERIFY_EXPIRATION,
    }
    # get user from token, BEFORE verification, to get user secret key
    unverified_payload = jwt.decode(token, None, False)
    secret_key = jwt_get_secret_key(unverified_payload)
    return jwt.decode(
        token,
        api_settings.JWT_PUBLIC_KEY or secret_key,
        api_settings.JWT_VERIFY,
        options=options,
        leeway=api_settings.JWT_LEEWAY,
        algorithms=[api_settings.JWT_ALGORITHM]
    )


def jwt_get_user_secret_key(user):
    return user.id


def jwt_response_payload_handler(token, user=None, request=None):
    makejson = MakeJSON()

    makejson.addResult(token=token)
    return makejson.getJson()
