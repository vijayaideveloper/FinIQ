import os
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pandas as pd
from sqlalchemy import create_engine


BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'users.db'}"
IMAGE_FOLDER = BASE_DIR / "image_dashboards"

IMAGE_FOLDER.mkdir(exist_ok=True)

engine = create_engine(DATABASE_URL)


def load_data(email):
    income = pd.read_sql_query(
        "SELECT * FROM income WHERE email = :email",
        engine,
        params={"email": email},
    )
    expense = pd.read_sql_query(
        "SELECT * FROM expense WHERE email = :email",
        engine,
        params={"email": email},
    )
    return income, expense


def prepare_data(income_df, expense_df):

    income = income_df["amount"].reset_index(drop=True).copy()
    expense = expense_df["amount"].reset_index(drop=True).copy()

    max_len = max(len(income), len(expense))

    income = income.reindex(range(max_len), fill_value=0)
    expense = expense.reindex(range(max_len), fill_value=0)

    return income, expense


def create_dashboard(email):
    income_df, expense_df = load_data(email)


    if income_df.empty:
        income_df = pd.DataFrame({"title": ["No Income"], "amount": [0]})

    if expense_df.empty:
        expense_df = pd.DataFrame({"title": ["No Expense"], "amount": [0]})


    income_amount, expense_amount = prepare_data(income_df, expense_df)

    total_income = income_df["amount"].sum()
    total_expense = expense_df["amount"].sum()
    profit = total_income - total_expense
    savings = (profit / total_income * 100) if total_income else 0

    fig = plt.figure(figsize=(20, 14))
    grid = GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35)
    fig.suptitle("FINIQ FINANCIAL DASHBOARD", fontsize=22, fontweight="bold")

    # 1 Income vs Expense
    ax1 = fig.add_subplot(grid[0, 0])
    ax1.bar(["Income", "Expense"], [total_income, total_expense])
    ax1.set_title("Income vs Expense")

    # 2 Monthly Income (transaction order)
    ax2 = fig.add_subplot(grid[0, 1])
    ax2.plot(income_df.index + 1, income_df["amount"], marker="o")
    ax2.set_title("Monthly Income")
    ax2.grid(True)

    # 3 Expense Categorie
    ax3 = fig.add_subplot(grid[0, 2])
    if expense_df["amount"].sum() > 0:
        ax3.pie(
            expense_df["amount"],
            labels=expense_df["title"],
            autopct="%1.1f%%",
            startangle=90,
        )
    else:
        ax3.text(0.5, 0.5, "No Expense Data", ha="center", va="center")
    ax3.set_title("Expense Categories")

    # 4 Cash Flow
    ax4 = fig.add_subplot(grid[1, 0])
    cash = income_amount - expense_amount
    ax4.fill_between(range(1, len(cash) + 1), cash, alpha=0.4)
    ax4.plot(range(1, len(cash) + 1), cash)
    ax4.set_title("Cash Flow")

    # 5 Assets Distribution
    ax5 = fig.add_subplot(grid[1, 1])
    assets_values = [total_income, max(profit, 0)]
    if sum(assets_values) > 0:
        wedges, *_ = ax5.pie(
            assets_values,
            labels=["Income", "Profit"],
            autopct="%1.1f%%",
        )
        centre = plt.Circle((0, 0), 0.65, fc="white")
        ax5.add_artist(centre)
    else:
        ax5.text(0.5, 0.5, "No Data Available", ha="center", va="center")
    ax5.set_title("Assets Distribution")

    # 6 Net Worth
    ax6 = fig.add_subplot(grid[1, 2])
    nw = income_amount.cumsum() - expense_amount.cumsum()
    ax6.plot(nw.index + 1, nw, marker="o")
    ax6.grid(True)
    ax6.set_title("Net Worth")

    # 7 Monthly Comparison
    ax7 = fig.add_subplot(grid[2, 0])
    x = range(len(income_amount))
    w = 0.35

    ax7.bar([i - w / 2 for i in x], income_amount, w, label="Income")
    ax7.bar([i + w / 2 for i in x], expense_amount, w, label="Expense")
    ax7.legend()
    ax7.set_title("Monthly Comparison")

    # 8 Top Spending
    ax8 = fig.add_subplot(grid[2, 1])
    if not expense_df.empty:
        top = expense_df.sort_values("amount", ascending=True)
        ax8.barh(top["title"], top["amount"])
    else:
        ax8.text(0.5, 0.5, "No Expense Data", ha="center", va="center")
    ax8.set_title("Top Spending")

    # Report panel
    ax9 = fig.add_subplot(grid[2, 2])
    ax9.axis("off")
    ax9.text(
        0,
        1,
        f"""Financial Report

Income   : {total_income}
Expense  : {total_expense}
Profit   : {profit}
Savings  : {savings:.2f}%

Generated:
{datetime.now():%d-%m-%Y %H:%M:%S}
""",
        va="top",
    )

    filename = datetime.now().strftime("dashboard_%Y%m%d_%H%M%S.png")
    save_path = os.path.join(IMAGE_FOLDER, filename)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    return {
        "image": f"/image_dashboards/{filename}",
        "income": float(total_income),
        "expense": float(total_expense),
        "profit": float(profit),
        "savings": float(savings),
    }


if __name__ == "__main__":
    create_dashboard()