import unittest

import toolbelt


class ToolbeltTests(unittest.TestCase):
    def test_generate_password_length(self):
        pwd = toolbelt.generate_password(16)
        self.assertEqual(len(pwd), 16)

    def test_generate_password_no_symbols(self):
        pwd = toolbelt.generate_password(24, include_symbols=False)
        self.assertTrue(pwd.isalnum())

    def test_digest_bytes_sha256(self):
        digest = toolbelt.digest_bytes(b"hello", "sha256")
        self.assertEqual(
            digest,
            "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
        )


if __name__ == "__main__":
    unittest.main()
