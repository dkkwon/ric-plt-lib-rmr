# ==================================================================================
#       Copyright (c) 2019 Nokia
#       Copyright (c) 2018-2019 AT&T Intellectual Property.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#          http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# ==================================================================================

"""
Provides mocks that are useful for end applications unit testing
"""

import json
import uuid


def rcv_mock_generator(msg_payload, msg_type, msg_state, jsonb, timeout=0):
    """
    generates a mock function that can be used to monkeypatch rmr_torcv_msg or rmr_rcv_msg
    """

    def f(_mrc, sbuf, _timeout=timeout):  # last param is needed for calls to rmr_torcv_msg, but not in rmr_rcv_msg
        sbuf.contents.mtype = msg_type
        payload = json.dumps(msg_payload).encode("utf-8") if jsonb else msg_payload
        sbuf.contents.payload = payload
        sbuf.contents.len = len(payload)
        sbuf.contents.state = msg_state
        return sbuf

    return f


def send_mock_generator(msg_state):
    """
    generates a mock function that can be used to monkeypatch rmr_send_msg
    usage example:
        monkeypatch.setattr('rmr.rmr.rmr_send_msg', rmr_mocks.send_mock_generator(0))
    """

    def f(_unused, sbuf):
        sbuf.contents.state = msg_state
        return sbuf

    return f


class _Sbuf_Contents:
    """fake version of how pointers work (ctype pointer access is done by accessing a magical attrivute called "contents"""

    def __init__(self):
        self.state = 0
        self.mtype = 0
        self.len = 0
        self.payload = ""
        self.xaction = uuid.uuid1().hex.encode("utf-8")
        self.sub_id = 0

    def __str__(self):
        return str(
            {
                "state": self.state,
                "mtype": self.mtype,
                "len": self.len,
                "payload": self.payload,
                "xaction": self.xaction,
                "sub_id": self.sub_id,
            }
        )


class Rmr_mbuf_t:
    """fake version of rmr.rmr_mbuf_t"""

    def __init__(self):
        self.contents = _Sbuf_Contents()


def patch_rmr(monkeypatch):
    """
    Patch rmr; requires a monkeypatch (pytest) object to be passed in
    """

    def fake_alloc(_unused, _alsounused):
        return Rmr_mbuf_t()

    def fake_set_payload_and_length(payload, sbuf):
        sbuf.contents.payload = payload
        sbuf.contents.len = len(payload)

    def fake_generate_and_set_transaction_id(sbuf):
        sbuf.contents.xaction = uuid.uuid1().hex.encode("utf-8")

    def fake_get_payload(sbuf):
        return sbuf.contents.payload

    def fake_get_meid(_sbuf):
        return None  # this is not a part of rmr_mbuf_t

    def fake_get_src(_sbuf):
        return "localtest:80"  # this is not a part of rmr_mbuf_t

    def fake_rmr_payload_size(_sbuf):
        return 4096

    monkeypatch.setattr("rmr.rmr.rmr_alloc_msg", fake_alloc)
    monkeypatch.setattr("rmr.rmr.set_payload_and_length", fake_set_payload_and_length)
    monkeypatch.setattr("rmr.rmr.generate_and_set_transaction_id", fake_generate_and_set_transaction_id)
    monkeypatch.setattr("rmr.rmr.get_payload", fake_get_payload)
    monkeypatch.setattr("rmr.rmr.get_src", fake_get_src)
    monkeypatch.setattr("rmr.rmr.get_meid", fake_get_meid)
    monkeypatch.setattr("rmr.rmr.rmr_payload_size", fake_rmr_payload_size)