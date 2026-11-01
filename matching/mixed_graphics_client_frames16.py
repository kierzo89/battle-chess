"""Exact retained-object client contracts; comparison only, no admission.

Contracts must be pinned by the production caller. Parsing is performed once;
each field still checks whole-object identity and exact source owner context.
"""
import dataclasses
import hashlib
import json


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def field_record(field, symbol):
    value = dataclasses.asdict(field)
    value['raw'] = value['raw'].hex()
    value['frame'] = list(value['frame'])
    value['target'] = list(value['target'])
    return {'symbol': symbol, 'fixup': value}


class ClosedClientFrames:
    def __init__(self, contract_bytes, expected_sha256):
        if sha(contract_bytes) != expected_sha256:
            raise ValueError('client contract digest changed')
        contract = json.loads(contract_bytes)
        if contract['schema'] != 'exact-mixed-BSS-client-fields-v1':
            raise ValueError('unsupported client contract')
        self._context = contract['context']
        self._raw_hash = contract['whole_object_sha256']
        rows = contract['fields']
        self._fields = {r['fixup']['offset']: r for r in rows}
        if len(self._fields) != len(rows) or not rows:
            raise ValueError('empty or duplicate client fields')

    def validate(self, row, raw, field, symbol):
        if type(raw) is not bytes or sha(raw) != self._raw_hash:
            raise ValueError('whole client object changed')
        if any(row.get(k) != v for k, v in self._context.items()):
            raise ValueError('client source/owner context changed')
        if field_record(field, symbol) != self._fields.get(field.offset):
            raise ValueError('unproved client field; no frame normalization')
        return 'proven_exact_mixed_external_PUBLIC_group1'
