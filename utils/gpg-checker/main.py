import logging
import sys

import gnupg
from faker import Faker

logging.basicConfig(level=logging.INFO)

gpg = gnupg.GPG(gnupghome="./gnupghome")
gpg.encoding = 'utf-8'


def remove_existing_gpg_keys() -> None:
    while len(gpg.list_keys()) > 0:
        logging.info("Remove already existed GPG keys")
        gpg.delete_keys(list(map(lambda key: key['fingerprint'], gpg.list_keys())))
        logging.info("Done")


def main() -> None:
    remove_existing_gpg_keys()

    input_public_key_filename = sys.argv[1]
    gpg.import_keys_file(input_public_key_filename)

    keys = gpg.list_keys()
    assert len(keys) == 1
    assert keys[0]['type'] == "pub"
    assert keys[0]['length'] == "4096"
    assert keys[0]['algo'] == "1"
    assert len(keys[0]['uids']) == 1

    uid = keys[0]['uids'][0]
    fingerprint = keys[0]['fingerprint']

    message = Faker().name()
    message_encrypted = gpg.encrypt(message, fingerprint, always_trust=True)

    print(uid)
    print(message)
    print(message_encrypted)

    remove_existing_gpg_keys()


if __name__ == "__main__":
    main()
