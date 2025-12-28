from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

app = Flask(__name__)

# Словник для відповідності таблиць та їх первинних ключів (ID)
TABLE_KEYS = {
    'categories': 'category_id',
    'customers': 'customer_id',
    'employees': 'employee_id',
    'orders': 'order_id',
    'order_items': 'order_item_id',
    'products': 'product_id',
    'suppliers': 'supplier_id',
    'warehouse': 'warehouse_id'
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Помилка підключення до бази даних: {e}")
        return None
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/categories')
def categories():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categories")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('categories.html', categories=data)

@app.route('/customers')
def customers():
    # Отримуємо дані з URL
    last_name = request.args.get('last_name')
    phone = request.args.get('phone')

    # Отримуємо стан галочок
    use_last_name = request.args.get('use_last_name')
    use_phone = request.args.get('use_phone')

    query = "SELECT * FROM customers WHERE 1=1"
    params = []

    # Фільтрація за прізвищем (пошук по частині слова)
    if use_last_name and last_name:
        query += " AND last_name LIKE %s"
        params.append(f"%{last_name}%")

    # Фільтрація за номером телефону
    if use_phone and phone:
        query += " AND phone LIKE %s"
        params.append(f"%{phone}%")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute(query, params)
    data = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('customers.html', customers=data)

@app.route('/employees')
def employees():
    # Отримуємо значення з URL
    last_name = request.args.get('last_name')
    position = request.args.get('position')
    phone = request.args.get('phone')

    # Отримуємо стан галочок
    use_last_name = request.args.get('use_last_name')
    use_pos = request.args.get('use_pos')
    use_phone = request.args.get('use_phone')

    query = "SELECT * FROM employees WHERE 1=1"
    params = []

    if use_last_name and last_name:
        query += " AND last_name LIKE %s"
        params.append(f"%{last_name}%")

    if use_pos and position:
        query += " AND position LIKE %s"
        params.append(f"%{position}%")

    if use_phone and phone:
        query += " AND phone LIKE %s"
        params.append(f"%{phone}%")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('employees.html', employees=data)

@app.route('/orders')
def orders():
    # значення з форми
    order_id = request.args.get('order_id')
    customer_id = request.args.get('customer_id')
    employee_id = request.args.get('employee_id')
    status = request.args.get('status')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    # галочки
    use_order = request.args.get('use_order')
    use_customer = request.args.get('use_customer')
    use_employee = request.args.get('use_employee')
    use_status = request.args.get('use_status')
    use_date_from = request.args.get('use_date_from')
    use_date_to = request.args.get('use_date_to')

    query = "SELECT * FROM orders WHERE 1=1"
    params = []

    if use_order and order_id:
        query += " AND order_id = %s"
        params.append(order_id)

    if use_customer and customer_id:
        query += " AND customer_id = %s"
        params.append(customer_id)

    if use_employee and employee_id:
        query += " AND employee_id = %s"
        params.append(employee_id)

    if use_status and status:
        query += " AND status = %s"
        params.append(status)

    if use_date_from and date_from:
        query += " AND order_date >= %s"
        params.append(date_from)

    if use_date_to and date_to:
        query += " AND order_date <= %s"
        params.append(date_to)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('orders.html', orders=data)

@app.route('/orders/<int:order_id>')
def order_details(order_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Отримуємо саме замовлення
    cursor.execute("""
        SELECT 
            o.order_id,
            o.order_date,
            o.status,
            CONCAT(c.last_name, ' ', c.first_name, ' ') AS customer_name,
            CONCAT(e.last_name, ' ', e.first_name, ' ') AS employee_name
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            JOIN employees e ON o.employee_id = e.employee_id
            WHERE o.order_id = %s
        """, (order_id,)
    )
    order = cursor.fetchone()

    # Отримуємо позиції цього замовлення
    cursor.execute(
        "SELECT * FROM order_items WHERE order_id = %s",
        (order_id,)
    )
    items = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'order_items.html',
        order=order,
        order_items=items
    )

@app.route('/products')
def products():

    # ---------- Фільтрація даних -------------
    product_name = request.args.get('product_name')
    category_id = request.args.get('category_id')
    supplier_id = request.args.get('supplier_id')
    price_min = request.args.get('price_min')
    price_max = request.args.get('price_max')

# Отримуємо стани галочок (якщо галочка не стоїть, прийде None)
    use_name = request.args.get('use_name')
    use_cat = request.args.get('use_cat')
    use_sup = request.args.get('use_sup')
    use_pmin = request.args.get('use_pmin')
    use_pmax = request.args.get('use_pmax')

    query = "SELECT * FROM products WHERE 1=1"
    params = []

    # Фільтруємо ТІЛЬКИ якщо стоїть відповідна галочка
    if use_name and product_name:
        query += " AND product_name LIKE %s"
        params.append(f"%{product_name}%")
        
    if use_cat and category_id:
        query += " AND category_id = %s"
        params.append(category_id)
        
    if use_sup and supplier_id:
        query += " AND supplier_id = %s"
        params.append(supplier_id)
        
    if use_pmin and price_min:
        query += " AND price >= %s"
        params.append(price_min)
        
    if use_pmax and price_max:
        query += " AND price <= %s"
        params.append(price_max)
    # ------------


    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('products.html', products=data)

@app.route('/suppliers')
def suppliers():
    # ---------- Фільтрація даних -------------
    # Отримуємо значення текстових полів
    supplier_name = request.args.get('supplier_name')
    phone = request.args.get('phone')

    # Отримуємо стани галочок (checkbox)
    use_name = request.args.get('use_name')
    use_phone = request.args.get('use_phone')

    # Базовий SQL запит
    query = "SELECT * FROM suppliers WHERE 1=1"
    params = []

    # Додаємо умови, якщо стоять галочки
    if use_name and supplier_name:
        query += " AND supplier_name LIKE %s"
        params.append(f"%{supplier_name}%")
        
    if use_phone and phone:
        query += " AND phone LIKE %s"
        params.append(f"%{phone}%")
    # -----------------------------------------

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Виконуємо запит із параметрами фільтрації
    cursor.execute(query, params)
    data = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('suppliers.html', suppliers=data)

@app.route('/warehouse')
def warehouse():
    # ---------- Фільтрація даних для складу -------------
    # Отримуємо значення з форми
    product_id = request.args.get('product_id')
    max_qty = request.args.get('max_qty')

    # Отримуємо стани галочок
    use_prod = request.args.get('use_prod')
    use_qty = request.args.get('use_qty')

    # Базовий запит
    query = "SELECT * FROM warehouse WHERE 1=1"
    params = []

    # Фільтр за ID товару
    if use_prod and product_id:
        query += " AND product_id = %s"
        params.append(product_id)
        
    # Фільтр за залишками (менше або дорівнює вказаному числу)
    if use_qty and max_qty:
        query += " AND quantity_in_stock <= %s"
        params.append(max_qty)
    # ----------------------------------------------------

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Виконуємо запит з урахуванням фільтрів
    cursor.execute(query, params)
    data = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('warehouse.html', warehouse=data)

@app.route('/report/orders')
def report():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 🔹 Загальна статистика
    cursor.execute("""
        SELECT 
            COUNT(DISTINCT o.order_id) AS total_orders,
            COALESCE(SUM(oi.quantity * p.price), 0) AS total_sum
        FROM orders o
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        LEFT JOIN products p ON oi.product_id = p.product_id
    """)
    summary = cursor.fetchone()

    # 🔹 Статистика по статусах
    cursor.execute("""
        SELECT 
            o.status,
            COUNT(DISTINCT o.order_id) AS orders_count,
            COALESCE(SUM(oi.quantity * p.price), 0) AS orders_sum
        FROM orders o
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        LEFT JOIN products p ON oi.product_id = p.product_id
        GROUP BY o.status
    """)
    by_status = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'report.html',
        summary=summary,
        by_status=by_status
    )


# ----- Кнопки додавання/редагування та видалення записів ------
@app.route('/<table_name>/add', methods=['GET', 'POST'])
def add_record(table_name):
    if table_name not in TABLE_KEYS: return "Таблицю не знайдено", 404
    
    if request.method == 'POST':
        # Отримуємо всі дані з форми як словник (ключ: значення)
        data = request.form.to_dict()
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        values = tuple(data.values())

        conn = get_db_connection()
        cursor = conn.cursor()
        # Динамічно формуємо запит: INSERT INTO назва_таблиці (колонки) VALUES (%s, %s...)
        cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)
        conn.commit()
        cursor.close()
        conn.close()

        # ЛОГІКА ПЕРЕНАПРАВЛЕННЯ:
        # Якщо ми редагували/додавали позицію товару (order_items)
        if table_name == 'order_items':
            # Нам треба повернутися в "Деталі замовлення"
            # Беремо order_id з даних форми, які щойно зберегли
            # request.form містить дані, які прийшли з форми
            order_id = request.form.get('order_id')
            return redirect(url_for('order_details', order_id=order_id))

        return redirect(url_for(table_name)) # Повернення на сторінку списку

    return render_template(f'forms/{table_name}_form.html', title=f'Додати запис у {table_name}', item=None)

@app.route('/<table_name>/edit/<int:record_id>', methods=['GET', 'POST'])
def edit_record(table_name, record_id):
    pk = TABLE_KEYS.get(table_name)
    if not pk: return "Помилка", 404

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        data = request.form.to_dict()
        # Формуємо рядок SET для UPDATE: "col1=%s, col2=%s"
        set_clause = ", ".join([f"{k}=%s" for k in data.keys()])
        values = list(data.values()) + [record_id]

        cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {pk}=%s", values)
        conn.commit()
        cursor.close()
        conn.close()

        # ЛОГІКА ПЕРЕНАПРАВЛЕННЯ:
        # Якщо ми редагували/додавали позицію товару (order_items)
        if table_name == 'order_items':
            # Нам треба повернутися в "Деталі замовлення"
            # Беремо order_id з даних форми, які щойно зберегли
            # request.form містить дані, які прийшли з форми
            order_id = request.form.get('order_id')
            return redirect(url_for('order_details', order_id=order_id))

        return redirect(url_for(table_name))

    cursor.execute(f"SELECT * FROM {table_name} WHERE {pk}=%s", (record_id,))
    item = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template(f'forms/{table_name}_form.html', title='Редагувати', item=item)

@app.route('/<table_name>/delete/<int:record_id>')
def delete_record(table_name, record_id):
    pk = TABLE_KEYS.get(table_name)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    target_order_id = None
    if table_name == 'order_items':
        cursor.execute(f"SELECT order_id FROM order_items WHERE order_item_id=%s", (record_id,))
        row = cursor.fetchone()
        if row:
            target_order_id = row['order_id']

    cursor.execute(f"DELETE FROM {table_name} WHERE {pk}=%s", (record_id,))
    conn.commit()
    cursor.close()
    conn.close()

    if table_name == 'order_items' and target_order_id:
        return redirect(url_for('order_details', order_id=target_order_id))

    return redirect(url_for(table_name))

