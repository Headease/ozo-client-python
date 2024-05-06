#  Copyright (c) Stichting Koppeltaal 2021.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import uuid


def envget_str(key: str, dflt: str = '') -> str:
    """
    Gets a value from the os.environ, and defaults to the value of dflt if not set in the environment.
    :param key: environment variable name
    :param dflt: default value, if not present in the environment
    :return: either the value of the environment variable or the default value (dflt)
    """
    return os.environ[key] if key in os.environ else dflt


def envget_bool(key, dflt: bool = False) -> bool:
    """
    Gets a value from the os.environ, and defaults to the value of dflt if not set in the environment.
    :param key: environment variable name
    :param dflt: default value, if not present in the environment
    :return: either the value of the environment variable or the default value (dflt)
    """
    val = envget_str(key, 'True' if dflt else 'False')
    return val.lower() in ['true', 'yes', '1', 'y']


DEBUG = envget_bool('DEBUG', False)

SECRET_KEY = envget_str('APP_SECRET_KEY', str(uuid.uuid1()))
SESSION_TYPE = envget_str('APP_SESSION_TYPE', 'filesystem')

NUTS_BASE_URL = envget_str('NUTS_BASE_URL', 'https://nuts-node-client.ozo.headease.nl')
NUTS_BASE_URL_INT = envget_str('NUTS_BASE_URL_INT', 'https://nuts-node-client-int.ozo.headease.nl')
DID_DATA_SOURCE = envget_str('DID_DATA_SOURCE', 'did:web:nuts-node-ozo.ozo.headease.nl:iam:ozo')
DID_ISSUER = envget_str('DID_ISSUER', 'did:web:issuer.ozo.headease.nl')
