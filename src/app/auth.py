import os
import pyotp
import qrcode
import json


def create_auth_uri(username: str, app_name: str = "Slots App") -> str:
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(
        name=username,
        issuer_name=app_name
    )
    return uri


def make_qr_code(uri: str, filename: str) -> None:
    img = qrcode.make(uri)
    img.save(filename)


def verify_otp(otp_1: str, otp_2: str, known_secrets_json_path: str) -> bool:
    if not otp_1 or not otp_2 or otp_1 == otp_2:
        return False

    # Load secrets
    with open(known_secrets_json_path, "r") as f:
        secrets = json.load(f)

    valid_secrets = []
    # Check which secrets match the provided codes
    for name, secret in secrets.items():
        totp = pyotp.TOTP(secret)
        if totp.verify(otp_1, valid_window=1) or totp.verify(otp_2, valid_window=1):
            valid_secrets.append(name)

    # Must have at least 2 **different** secrets matched
    return len(set(valid_secrets)) >= 2


if __name__ == '__main__':
    save_path = "../../auth_codes"
    os.makedirs(save_path, exist_ok=True)

    users = ["user1", "user2", "devUser1", "devUser2"]
    uris = {}
    for user in users:
        uri = create_auth_uri(user)
        uris[user] = uri
        make_qr_code(uri, f"{save_path}/{user}.png")

    # Create json
    with open(f"{save_path}/secrets.json", "w") as f:
        json.dump(uris, f)

