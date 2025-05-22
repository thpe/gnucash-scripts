#!/usr/bin/env python3
import pysie_accounting.pysie as pysie
import pprint
from datetime import datetime
import sys
import numpy as np
from piecash import create_book, Account, Commodity, open_book, Transaction, Split
from piecash.core.factories import create_currency_from_ISO
from decimal import Decimal
from tqdm import tqdm


sie = pysie.PySIE ()
sie.open_trans (sys.argv[2])
sie.open (sys.argv[1])

sek = create_currency_from_ISO("SEK")
today = datetime.now()
with open_book(sys.argv[3], readonly=False) as book:

    SEK = book.currencies(mnemonic="SEK")
    for k,v in tqdm(sie.verifikat.items()):
        d1 = datetime.strptime(v[0], "%Y%m%d")
        d2 = datetime.strptime(v[2], "%Y%m%d")
        sp = []
        for ss in v[3]:
            a = book.accounts(code=ss[0])
            am = Decimal(ss[2])
            sp.append(Split(account=a, value=am))
        t=Transaction(post_date=d1.date(), enter_date=d2, currency=SEK, description = v[1], splits=sp, num=k)

    book.save()
