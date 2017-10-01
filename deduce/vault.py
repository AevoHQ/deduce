"""Aevo Vault vectorized interface."""

import keras.utils
import numpy as np
import requests

from .config import ARGS

IP = ARGS.vault_ip


def _request(scope, endpoint=None):
    """Safely GET scoped data from a Vault endpoint."""

    path = "/scope/{scope}".format(scope=scope)
    if endpoint is not None:
        path += "/" + endpoint

    result = requests.get(IP + path)

    assert result.ok
    return result.json()


def vectorize(data, schema_field):
    """Vectorize a single schema field."""

    if schema_field == "number":
        return np.array([[d] for d in data])

    if isinstance(schema_field, list):
        indices = [schema_field.index(d) for d in data]
        one_hot = keras.utils.to_categorical(indices, len(schema_field))
        return one_hot

    raise Exception("invalid schema field: ", schema_field)


def vectorize_scope(data, schema):
    """Vectorize a single scope."""

    features = []

    for (field, schema_field) in sorted(schema.items()):
        feature = vectorize([d[field] for d in data], schema_field)
        features.append(feature)

    return np.hstack(features)


def vectorize_model(scope):
    """Vectorize the factors of a scope defined in its model."""

    factors = _request(scope, "model")["factors"]
    data = _request(scope, "data")

    features = []
    for factor in factors:
        feature = vectorize_scope(
            [d["factors"][factor] for d in data],
            _request(factor, "schema")
        )
        features.append(feature)

    labels = vectorize_scope(
        [d["label"] for d in data],
        _request(scope, "schema")
    )

    return np.hstack(features), labels
