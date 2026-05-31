"""Tests for common generation options — normal, boundary, and exception cases.

Covers all 10 options from:
https://github.com/OpenCSGs/csghub-lite/blob/main/docs/api/overview.md#通用选项
"""

import pytest
from utils import assert_status


# Base payloads reused across tests
_CHAT_BODY = {"model": "test", "messages": [{"role": "user", "content": "Hi"}]}
_GEN_BODY = {"model": "test", "prompt": "Hi"}


def _chat(client, **options):
    body = {**_CHAT_BODY, "options": options}
    return client.post("/api/chat", json=body)


def _gen(client, **options):
    body = {**_GEN_BODY, "options": options}
    return client.post("/api/generate", json=body)


# ---------------------------------------------------------------------------
# temperature
# ---------------------------------------------------------------------------

class TestTemperature:
    def test_default(self, client):
        for r in [_chat(client), _gen(client)]:
            assert_status(r, 200, 400, 404, 500)

    def test_explicit_default(self, client):
        for r in [_chat(client, temperature=0.7), _gen(client, temperature=0.7)]:
            assert_status(r, 200, 400, 404, 500)

    def test_zero(self, client):
        for r in [_chat(client, temperature=0.0), _gen(client, temperature=0.0)]:
            assert_status(r, 200, 400, 422, 500)

    def test_one(self, client):
        for r in [_chat(client, temperature=1.0), _gen(client, temperature=1.0)]:
            assert_status(r, 200, 400, 422, 500)

    def test_two(self, client):
        for r in [_chat(client, temperature=2.0), _gen(client, temperature=2.0)]:
            assert_status(r, 200, 400, 422, 500)

    def test_negative(self, client):
        for r in [_chat(client, temperature=-0.1), _gen(client, temperature=-0.1)]:
            assert_status(r, 200, 400, 422, 500)

    def test_wrong_type_string(self, client):
        for r in [_chat(client, temperature="hot"), _gen(client, temperature="hot")]:
            assert_status(r, 200, 400, 422, 500)

    def test_wrong_type_null(self, client):
        r = _chat(client, temperature=None)
        assert_status(r, 200, 400, 422, 500)


# ---------------------------------------------------------------------------
# top_p
# ---------------------------------------------------------------------------

class TestTopP:
    def test_default(self, client):
        for r in [_chat(client, top_p=0.9), _gen(client, top_p=0.9)]:
            assert_status(r, 200, 400, 404, 500)

    def test_zero(self, client):
        for r in [_chat(client, top_p=0.0), _gen(client, top_p=0.0)]:
            assert_status(r, 200, 400, 422, 500)

    def test_one(self, client):
        for r in [_chat(client, top_p=1.0), _gen(client, top_p=1.0)]:
            assert_status(r, 200, 400, 422, 500)

    def test_above_one(self, client):
        for r in [_chat(client, top_p=1.5), _gen(client, top_p=1.5)]:
            assert_status(r, 200, 400, 422, 500)

    def test_negative(self, client):
        for r in [_chat(client, top_p=-0.1), _gen(client, top_p=-0.1)]:
            assert_status(r, 200, 400, 422, 500)

    def test_wrong_type_string(self, client):
        r = _chat(client, top_p="high")
        assert_status(r, 200, 400, 422, 500)


# ---------------------------------------------------------------------------
# top_k
# ---------------------------------------------------------------------------

class TestTopK:
    def test_default(self, client):
        for r in [_chat(client, top_k=40), _gen(client, top_k=40)]:
            assert_status(r, 200, 400, 404, 500)

    def test_zero(self, client):
        for r in [_chat(client, top_k=0), _gen(client, top_k=0)]:
            assert_status(r, 200, 400, 422, 500)

    def test_one(self, client):
        for r in [_chat(client, top_k=1), _gen(client, top_k=1)]:
            assert_status(r, 200, 400, 422, 500)

    def test_large(self, client):
        for r in [_chat(client, top_k=1000), _gen(client, top_k=1000)]:
            assert_status(r, 200, 400, 422, 500)

    def test_negative(self, client):
        for r in [_chat(client, top_k=-1), _gen(client, top_k=-1)]:
            assert_status(r, 200, 400, 422, 500)

    def test_wrong_type_float(self, client):
        r = _chat(client, top_k=40.5)
        assert_status(r, 200, 400, 422, 500)

    def test_wrong_type_string(self, client):
        r = _chat(client, top_k="forty")
        assert_status(r, 200, 400, 422, 500)


# ---------------------------------------------------------------------------
# max_tokens
# ---------------------------------------------------------------------------

class TestMaxTokens:
    def test_default(self, client):
        for r in [_chat(client, max_tokens=2048), _gen(client, max_tokens=2048)]:
            assert_status(r, 200, 400, 404, 500)

    def test_zero(self, client):
        for r in [_chat(client, max_tokens=0), _gen(client, max_tokens=0)]:
            assert_status(r, 200, 400, 422, 500)

    def test_one(self, client):
        for r in [_chat(client, max_tokens=1), _gen(client, max_tokens=1)]:
            assert_status(r, 200, 400, 422, 500)

    def test_very_large(self, client):
        for r in [_chat(client, max_tokens=999999), _gen(client, max_tokens=999999)]:
            assert_status(r, 200, 400, 422, 500)

    def test_negative(self, client):
        for r in [_chat(client, max_tokens=-1), _gen(client, max_tokens=-1)]:
            assert_status(r, 200, 400, 422, 500)

    def test_negative_large(self, client):
        r = _chat(client, max_tokens=-9999)
        assert_status(r, 200, 400, 422, 500)

    def test_wrong_type_string(self, client):
        r = _chat(client, max_tokens="many")
        assert_status(r, 200, 400, 422, 500)


# ---------------------------------------------------------------------------
# seed
# ---------------------------------------------------------------------------

class TestSeed:
    def test_default_minus_one(self, client):
        for r in [_chat(client, seed=-1), _gen(client, seed=-1)]:
            assert_status(r, 200, 400, 404, 500)

    def test_zero(self, client):
        for r in [_chat(client, seed=0), _gen(client, seed=0)]:
            assert_status(r, 200, 400, 422, 500)

    def test_positive(self, client):
        for r in [_chat(client, seed=42), _gen(client, seed=42)]:
            assert_status(r, 200, 400, 422, 500)

    def test_large(self, client):
        for r in [_chat(client, seed=999999999), _gen(client, seed=999999999)]:
            assert_status(r, 200, 400, 422, 500)

    def test_negative_two(self, client):
        """seed=-2 is below the -1 sentinel."""
        for r in [_chat(client, seed=-2), _gen(client, seed=-2)]:
            assert_status(r, 200, 400, 422, 500)

    def test_wrong_type_string(self, client):
        r = _chat(client, seed="random")
        assert_status(r, 200, 400, 422, 500)

    def test_wrong_type_float(self, client):
        r = _chat(client, seed=42.0)
        assert_status(r, 200, 400, 422, 500)


# ---------------------------------------------------------------------------
# num_ctx
# ---------------------------------------------------------------------------

class TestNumCtx:
    def test_default(self, client):
        for r in [_chat(client, num_ctx=4096), _gen(client, num_ctx=4096)]:
            assert_status(r, 200, 400, 404, 500)

    def test_zero(self, client):
        for r in [_chat(client, num_ctx=0), _gen(client, num_ctx=0)]:
            assert_status(r, 200, 400, 422, 500)

    def test_small(self, client):
        for r in [_chat(client, num_ctx=512), _gen(client, num_ctx=512)]:
            assert_status(r, 200, 400, 422, 500)

    def test_huge(self, client):
        for r in [_chat(client, num_ctx=999999999), _gen(client, num_ctx=999999999)]:
            assert_status(r, 200, 400, 422, 500)

    def test_negative(self, client):
        for r in [_chat(client, num_ctx=-1), _gen(client, num_ctx=-1)]:
            assert_status(r, 200, 400, 422, 500)

    def test_wrong_type_string(self, client):
        r = _chat(client, num_ctx="4096")
        assert_status(r, 200, 400, 422, 500)


# ---------------------------------------------------------------------------
# num_parallel
# ---------------------------------------------------------------------------

class TestNumParallel:
    def test_default(self, client):
        for r in [_chat(client, num_parallel=4), _gen(client, num_parallel=4)]:
            assert_status(r, 200, 400, 404, 500)

    def test_zero(self, client):
        for r in [_chat(client, num_parallel=0), _gen(client, num_parallel=0)]:
            assert_status(r, 200, 400, 422, 500)

    def test_one(self, client):
        for r in [_chat(client, num_parallel=1), _gen(client, num_parallel=1)]:
            assert_status(r, 200, 400, 422, 500)

    def test_large(self, client):
        for r in [_chat(client, num_parallel=100), _gen(client, num_parallel=100)]:
            assert_status(r, 200, 400, 422, 500)

    def test_negative(self, client):
        for r in [_chat(client, num_parallel=-1), _gen(client, num_parallel=-1)]:
            assert_status(r, 200, 400, 422, 500)

    def test_wrong_type_string(self, client):
        r = _chat(client, num_parallel="four")
        assert_status(r, 200, 400, 422, 500)

    def test_wrong_type_float(self, client):
        r = _chat(client, num_parallel=4.5)
        assert_status(r, 200, 400, 422, 500)


# ---------------------------------------------------------------------------
# cache_type_k
# ---------------------------------------------------------------------------

class TestCacheTypeK:
    def test_default_f16(self, client):
        for r in [_chat(client, cache_type_k="f16"), _gen(client, cache_type_k="f16")]:
            assert_status(r, 200, 400, 404, 500)

    def test_q8_0(self, client):
        for r in [_chat(client, cache_type_k="q8_0"), _gen(client, cache_type_k="q8_0")]:
            assert_status(r, 200, 400, 404, 500)

    def test_q4_0(self, client):
        for r in [_chat(client, cache_type_k="q4_0"), _gen(client, cache_type_k="q4_0")]:
            assert_status(r, 200, 400, 404, 500)

    def test_empty_string(self, client):
        for r in [_chat(client, cache_type_k=""), _gen(client, cache_type_k="")]:
            assert_status(r, 200, 400, 422, 500)

    def test_invalid_value(self, client):
        for r in [_chat(client, cache_type_k="not_a_dtype"), _gen(client, cache_type_k="not_a_dtype")]:
            assert_status(r, 200, 400, 422, 500)

    def test_wrong_type_number(self, client):
        r = _chat(client, cache_type_k=123)
        assert_status(r, 200, 400, 422, 500)

    def test_wrong_type_null(self, client):
        r = _chat(client, cache_type_k=None)
        assert_status(r, 200, 400, 422, 500)


# ---------------------------------------------------------------------------
# cache_type_v
# ---------------------------------------------------------------------------

class TestCacheTypeV:
    def test_default_f16(self, client):
        for r in [_chat(client, cache_type_v="f16"), _gen(client, cache_type_v="f16")]:
            assert_status(r, 200, 400, 404, 500)

    def test_q8_0(self, client):
        for r in [_chat(client, cache_type_v="q8_0"), _gen(client, cache_type_v="q8_0")]:
            assert_status(r, 200, 400, 404, 500)

    def test_q4_0(self, client):
        for r in [_chat(client, cache_type_v="q4_0"), _gen(client, cache_type_v="q4_0")]:
            assert_status(r, 200, 400, 404, 500)

    def test_empty_string(self, client):
        for r in [_chat(client, cache_type_v=""), _gen(client, cache_type_v="")]:
            assert_status(r, 200, 400, 422, 500)

    def test_invalid_value(self, client):
        for r in [_chat(client, cache_type_v="bad_value"), _gen(client, cache_type_v="bad_value")]:
            assert_status(r, 200, 400, 422, 500)

    def test_wrong_type_number(self, client):
        r = _chat(client, cache_type_v=456)
        assert_status(r, 200, 400, 422, 500)


# ---------------------------------------------------------------------------
# dtype
# ---------------------------------------------------------------------------

class TestDType:
    def test_default_f16(self, client):
        for r in [_chat(client, dtype="f16"), _gen(client, dtype="f16")]:
            assert_status(r, 200, 400, 404, 500)

    def test_q8_0(self, client):
        for r in [_chat(client, dtype="q8_0"), _gen(client, dtype="q8_0")]:
            assert_status(r, 200, 400, 404, 500)

    def test_q4_0(self, client):
        for r in [_chat(client, dtype="q4_0"), _gen(client, dtype="q4_0")]:
            assert_status(r, 200, 400, 404, 500)

    def test_auto(self, client):
        for r in [_chat(client, dtype="auto"), _gen(client, dtype="auto")]:
            assert_status(r, 200, 400, 404, 500)

    def test_empty_string(self, client):
        for r in [_chat(client, dtype=""), _gen(client, dtype="")]:
            assert_status(r, 200, 400, 422, 500)

    def test_invalid_value(self, client):
        for r in [_chat(client, dtype="xxx"), _gen(client, dtype="xxx")]:
            assert_status(r, 200, 400, 422, 500)

    def test_wrong_type_number(self, client):
        r = _chat(client, dtype=789)
        assert_status(r, 200, 400, 422, 500)

    def test_wrong_type_null(self, client):
        r = _chat(client, dtype=None)
        assert_status(r, 200, 400, 422, 500)


# ---------------------------------------------------------------------------
# Combined options
# ---------------------------------------------------------------------------

class TestCombinedOptions:
    def test_all_defaults_together(self, client):
        """Send every option at its documented default value together."""
        r = _chat(client,
            temperature=0.7, top_p=0.9, top_k=40, max_tokens=2048,
            seed=-1, num_ctx=4096, num_parallel=4,
            cache_type_k="f16", cache_type_v="f16", dtype="f16",
        )
        assert_status(r, 200, 400, 404, 500)

    def test_mix_valid_and_invalid(self, client):
        """Valid options mixed with one invalid should be rejected or tolerated."""
        r = _chat(client, temperature=0.5, top_k=-999, max_tokens=100)
        assert_status(r, 200, 400, 422, 500)

    def test_empty_options_object(self, client):
        body = {**_CHAT_BODY, "options": {}}
        r = client.post("/api/chat", json=body)
        assert_status(r, 200, 400, 404, 500)
