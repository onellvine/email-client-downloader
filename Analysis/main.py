import pandas as pd
import matplotlib.pyplot as plt



data = pd.read_csv("C:\\Users\\Nel\\Pictures\\Python\\automate\\Analysis\\orders_final_with_dates.csv")

price = list(data['Price'])
total = price.pop()
price.append(total)
price.remove(total)


days = list(data['Date'])
last_day = days.pop()
days.append(last_day)
days.remove(last_day)

plt.figure(figsize=[10,4])

plt.bar(days, price, ec='red', width = 0.5, color='#0504aa',alpha=0.7)
plt.grid(axis='y', alpha=0.75)
plt.title("Earning per day in KES.")
plt.xlabel("Days")
plt.ylabel("Amount (in KES)")
plt.show()
