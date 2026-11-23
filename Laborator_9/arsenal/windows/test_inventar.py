# -*- coding: utf-8 -*-
"""Verifica raportul pe capturile incluse in laborator."""
import os
import unittest

from arsenal.windows.inventar import raport


class TestInventar(unittest.TestCase):
    def test_raportul_capturilor(self):
        dosar = os.path.join(os.path.dirname(__file__), "start")
        rezultat = raport(dosar)
        self.assertEqual(rezultat["procese"], 7)
        self.assertEqual([p["nume"] for p in rezultat["suspecte"]],
                         ["update.exe", "svch0st.exe"])
        self.assertEqual(rezultat["evenimente"], 8)
        self.assertEqual([e["id"] for e in rezultat["alarma"]],
                         [4625, 4625, 7045, 6008, 1102])
