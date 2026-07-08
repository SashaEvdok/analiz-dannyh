import random
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import scrolledtext

# Параметры светофора
red_duration = 60
green_duration = 120
cycle_duration = red_duration + green_duration

# Симуляция поездок
num_weeks = 52  # 52 недели для точности
wait_times = []

for _ in range(num_weeks):
    arrival_time = random.uniform(0, cycle_duration)
    if arrival_time < red_duration:
        wait = red_duration - arrival_time
    else:
        wait = 0
    wait_times.append(wait)

# Расчёты
avg_wait = sum(wait_times) / len(wait_times)
month_wait = avg_wait * 4

# Вывод в окно
result_text = f"""
=== РЕЗУЛЬТАТ СИМУЛЯЦИИ ===

Среднее время ожидания за одну поездку: {avg_wait:.2f} секунд
За месяц (4 поездки): {month_wait:.2f} секунд

Аналитическое значение: 40 секунд
"""

root = tk.Tk()
root.title("Результат: светофор")
root.geometry("500x250")

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12))
text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
text_area.insert(tk.INSERT, result_text)
text_area.config(state=tk.DISABLED)

root.mainloop()

# График распределения
plt.hist(wait_times, bins=20, edgecolor='black')
plt.title('Распределение времени ожидания на светофоре')
plt.xlabel('Время ожидания (сек)')
plt.ylabel('Количество поездок')
plt.show()