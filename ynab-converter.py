import sys
from pathlib import Path

import pandas as pd

if __name__ == "__main__":
    for file_name in sys.argv[1:]:

        tables = pd.read_html(file_name, header=0, thousands=" ", decimal=",")

        account_name = tables[0].columns[1]
        transactions = tables[3]

        ynab = pd.DataFrame(
            columns=["Date", "Payee", "Category", "Memo", "Outflow", "Inflow"]
        )

        ynab["Date"] = transactions["Transaktionsdatum"]
        ynab["Payee"] = transactions["Text"]
        ynab[["Category", "Memo", "Outflow", "Inflow"]] = ""

        amounts = transactions["Belopp"]

        ynab.loc[amounts < 0, "Outflow"] = -amounts[amounts < 0]
        ynab.loc[amounts >= 0, "Inflow"] = amounts[amounts >= 0]

        ynab.to_csv("ynab-{}.csv".format(account_name), index=False)

        Path(file_name).unlink()
