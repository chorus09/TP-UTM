# -*- coding: utf-8 -*-
"""Verifica rezultatul diferentei pe capturile incluse in laborator."""
import os
import unittest

from arsenal.privesc.enum import suid_noi, periculoase_noi
from arsenal.privesc.diferenta import cai


class TestDiferenta(unittest.TestCase):
    def test_doar_ce_e_nou(self):
        dosar = os.path.join(os.path.dirname(__file__), "start")
        acum = cai(os.path.join(dosar, "suid.txt"))
        baza = cai(os.path.join(dosar, "baza_suid.txt"))
        noi = suid_noi(acum, baza)
        self.assertEqual(noi, {"/bin/cp", "/usr/bin/find", "/usr/bin/nmap",
                               "/usr/bin/vim.basic"})
        self.assertEqual(periculoase_noi(noi), sorted(noi))
