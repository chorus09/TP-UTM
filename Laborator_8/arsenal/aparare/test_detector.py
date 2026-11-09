# -*- coding: utf-8 -*-
"""Verifica detectorul pe jurnalul inclus si pragurile invalide."""
import os
import unittest

from arsenal.aparare.detector import raport_json, suspecti


class TestDetector(unittest.TestCase):
    def test_jurnalul_inclus(self):
        log = os.path.join(os.path.dirname(__file__), "start", "auth.log")
        raport = raport_json(log)
        self.assertEqual(raport["esecuri"], 15)
        self.assertEqual(raport["pe_ip"], {"203.0.113.9": 13,
                                           "198.51.100.7": 2})
        self.assertEqual(raport["suspecti"], [("203.0.113.9", 13)])

    def test_prag_invalid(self):
        with self.assertRaisesRegex(ValueError, "prag invalid"):
            suspecti({}, 0)
