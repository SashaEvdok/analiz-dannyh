import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import scrolledtext

# Функция для показа окна с текстом
def show_text_window(title, text):
    root = tk.Tk()
    root.title(title)
    root.geometry("500x300")
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 11))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    text_area.insert(tk.INSERT, text)
    text_area.config(state=tk.DISABLED)
    root.mainloop()

# Задание 1. Подготовка данных:

# Загружаем файлы.
customers = pd.read_csv('customers.csv')
products = pd.read_csv('products.csv')
orders = pd.read_csv('orders.csv')
order_items = pd.read_csv('order_items.csv')

# Проверяем пропуски и дубликаты (вывод в консоль убран).
# Объединяем таблицы.
orders_items = order_items.merge(products, on='product_id')
orders_full = orders_items.merge(orders, on='order_id')
full_data = orders_full.merge(customers, on='customer_id')

# Преобразуем дату.
full_data['order_date'] = pd.to_datetime(full_data['order_date'])
full_data['month'] = full_data['order_date'].dt.to_period('M')



# Задание 2. Анализ продаж:

# 2.1 Количество заказов по месяцам.
monthly_orders = full_data.groupby('month').size()
monthly_orders.plot(kind='bar', title='Количество заказов по месяцам')
plt.xlabel('Месяц')
plt.ylabel('Количество заказов')
plt.show()

# 2.2 Средняя сумма заказа по месяцам.
monthly_avg = orders.groupby(pd.to_datetime(orders['order_date']).dt.to_period('M'))['total_amount'].mean()
monthly_avg.plot(kind='line', marker='o', title='Средняя сумма заказа по месяцам')
plt.xlabel('Месяц')
plt.ylabel('Средняя сумма')
plt.show()

# 2.3 Топ-5 продуктов по продажам.
top_products = full_data.groupby('product_name')['quantity'].sum().sort_values(ascending=False).head(5)
top_products.plot(kind='bar', title='Топ-5 продуктов по продажам')
plt.xlabel('Продукт')
plt.ylabel('Количество продаж')
plt.show()



# Задание 3. Анализ клиентов:

# 3.1 Уникальные клиенты.
unique_customers = full_data['customer_id'].nunique()
text = f'Уникальных клиентов с заказами: {unique_customers}'
show_text_window('Задание 3.1', text)

# 3.2 Распределение клиентов по числу заказов.
orders_per_customer = full_data.groupby('customer_id').size()
orders_per_customer.value_counts().sort_index().plot(kind='bar', title='Распределение клиентов по числу заказов')
plt.xlabel('Количество заказов')
plt.ylabel('Количество клиентов')
plt.show()

# 3.3 Топ-5 клиентов по сумме покупок.
top_customers = full_data.groupby('name')['total_amount'].sum().sort_values(ascending=False).head(5)
top_customers.plot(kind='bar', title='Топ-5 клиентов по сумме покупок')
plt.xlabel('Клиент')
plt.ylabel('Сумма покупок')
plt.show()



# Задание 4. Анализ категорий продаж:

# 4.1 Общая сумма продаж по категориям.
category_sales = full_data.groupby('category')['total_amount'].sum()
lines = ['Сумма продаж по категориям:\n']
for cat, val in category_sales.items():
    lines.append(f'{cat}: {val} руб.')
text = '\n'.join(lines)
show_text_window('Задание 4.1', text)

# 4.2 Круговая диаграмма.
category_sales.plot(kind='pie', autopct='%1.1f%%', title='Доля категорий в продажах')
plt.ylabel('')
plt.show()



# Задание 5. Сезонность продаж:
full_data['day_of_week'] = full_data['order_date'].dt.dayofweek
full_data['month_num'] = full_data['order_date'].dt.month

pivot = full_data.pivot_table(index='day_of_week', columns='month_num', values='order_id', aggfunc='count', fill_value=0)

days_map = {0: 'Пн', 1: 'Вт', 2: 'Ср', 3: 'Чт', 4: 'Пт', 5: 'Сб', 6: 'Вс'}
pivot.index = [days_map[i] for i in pivot.index]

plt.figure(figsize=(10, 6))
sns.heatmap(pivot, annot=True, fmt='d', cmap='YlOrRd', cbar_kws={'label': 'Количество заказов'})
plt.title('Тепловая карта сезонности заказов')
plt.xlabel('Месяц')
plt.ylabel('День недели')
plt.show()



# Задание 6. Дополнительный анализ:
repeat_customers = full_data.groupby('customer_id').size()
repeat = repeat_customers[repeat_customers > 1].count()
text = f'Клиентов с повторными заказами: {repeat}'
show_text_window('Задание 6', text)

repeat_customers.value_counts().sort_index().plot(kind='bar', title='Количество заказов на клиента')
plt.xlabel('Число заказов')
plt.ylabel('Клиентов')
plt.show()