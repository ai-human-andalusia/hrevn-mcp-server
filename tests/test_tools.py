from __future__ import annotations

import unittest

from hrevn_mcp_server.tools import ToolRegistry


class FakeClient:
    def baseline_check(self, arguments):
        return {"result": "BASELINE_CHECK_COMPLETE", "echo": arguments}

    def profile_validate(self, arguments):
        return {"result": "PROFILE_VALIDATION_COMPLETE", "echo": arguments}

    def generate_bundle(self, arguments):
        return {"result": "GENERATED", "echo": arguments}

    def verify_bundle(self, arguments):
        return {"valid": True, "echo": arguments}


class ToolRegistryTests(unittest.TestCase):
    def test_list_tools_contains_expected_names(self):
        registry = ToolRegistry(client=FakeClient())
        names = [tool["name"] for tool in registry.list_tools()]
        self.assertEqual(
            names,
            ["baseline_check", "profile_validate", "generate_bundle", "verify_bundle"],
        )

    def test_call_tool_returns_structured_content(self):
        registry = ToolRegistry(client=FakeClient())
        result = registry.call_tool("baseline_check", {"profile": "eu_readiness_profile"})
        self.assertFalse(result["isError"])
        self.assertEqual(result["structuredContent"]["result"], "BASELINE_CHECK_COMPLETE")


if __name__ == "__main__":
    unittest.main()
