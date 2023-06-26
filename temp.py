import pandas

# Načtení tabulky s plánem
df_plan = pandas.read_csv("sales_plan.csv")
# Kumulativní součet za rok
df_plan["sales_plan_cumsum"] = df_plan.groupby("year")["sales"].cumsum()
# Načtení tabulky se skutečnými tržbami
df_actual = pandas.read_csv("sales_actual.csv")
# Seřazení podle data
df_actual = df_actual.sort_values("date")
# Vytvoření sloupečku date - převedení řetězce na typ datum a čas
df_actual["date"] = pandas.to_datetime(df_actual["date"])
# Uložení měsíce do samostatného sloupce
df_actual["month"] = df_actual["date"].dt.month
# Uložení roku do samostatného sloupce
df_actual["year"] = df_actual["date"].dt.year
# Vytvoření tabulky se sečtenými tržbami po měsících
df_actual_grouped = df_actual.groupby(["year", "month"]).sum(numeric_only=True)
# Vytvoření kumulativního součtu pro skutečné tržby
df_actual_grouped["sales_actual_cumsum"] = df_actual_grouped.groupby("year")["contract_value"].cumsum()
# Propojení obou tabulek
df_merged = pandas.merge(df_plan, df_actual_grouped, on=["month", "year"])
# Vypsání výsledků
# print(df_merged.head())

year = 2022
# Výběr řádků, které mají ve sloupci year hodnotu 2022
# Výběr provedeme pomocí dotazu
df_merged_plot = df_merged[df_merged["year"] == year]
# Reset index
df_merged_plot = df_merged_plot.reset_index()

import matplotlib.pyplot as plt
df_merged_plot["period"] = df_merged_plot["month"].astype(str) + "/" + df_merged_plot["year"].astype(str)
df_merged_plot = df_merged_plot.set_index("period")
ax = df_merged_plot["sales_plan_cumsum"].plot(color="red", title ="skutečné versus plánované tržby")
df_merged_plot["sales_actual_cumsum"].plot(kind="bar", ax=ax)
print(df_merged_plot.head())
plt.legend(["Plán tržeb", "Skutečné tržby"])
plt.ylabel("Miliony EUR")
plt.xlabel("Období")
plt.show()