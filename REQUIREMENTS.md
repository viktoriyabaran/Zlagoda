# ZLAGODA — Grocery Mini-Supermarket AIS

## Requirements Specification

> **Automated Information System for managing the sales process at the "ZLAGODA" grocery mini-supermarket.**

---

## 1. Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django (Python) |
| Frontend interactivity | HTMX |
| Styling | Tailwind CSS |
| Database | PostgreSQL |
| Infrastructure | Docker Containers |

### Critical Constraint — Raw SQL Only

Django ORM **may only be used to define models and generate the database schema** (migrations). **All actual data queries — reads, inserts, updates, deletes — must be written as raw SQL** executed through Django's `connection.cursor()` or `django.db.connection` utilities. No `Model.objects.filter(...)`, no `QuerySet` chains, no ORM-level joins.

---

## 2. Purpose

The application handles data used in the sales process of the ZLAGODA grocery mini-supermarket. It enables convenient tracking of:

- Quantity and selling price of every product in the store.
- Complete sales history (receipts / checks).
- All product categories available in the supermarket.
- Key characteristics of each product.
- Information about all employees.
- Information about loyalty customers who hold a Customer Card.

The system provides role-appropriate access to managers and cashiers.

---

## 3. User Roles

There are exactly **two** user roles.

### 3.1 Manager

- Oversees all supermarket processes.
- Has full read/write access to all data (employees, products, categories, store products, customer cards, receipts).
- **Cannot** create receipts (that is a cashier-only action).

### 3.2 Cashier

- Responsible for selling products (creating receipts / checks).
- Has limited read access and can only create/edit customer cards (in addition to creating receipts).
- Can view their own personal information.

---

## 4. Authentication & Security

- The system must distinguish between **identification** (who the user claims to be) and **authentication** (proof of identity).
- Passwords **must never be stored in plain text** in the database. Use hashing (e.g., Django's built-in `make_password` / `check_password` or `bcrypt`).
- Upon login, the system determines the user's role (`Manager` or `Cashier`) and restricts functionality accordingly.

---

## 5. Data Requirements

### 5.1 Employee

| Field | DB Column | Type | Constraints |
|---|---|---|---|
| Employee ID | `id_employee` | `VARCHAR(10)` | **PK**, NOT NULL |
| Surname | `empl_surname` | `VARCHAR(50)` | NOT NULL |
| Name | `empl_name` | `VARCHAR(50)` | NOT NULL |
| Patronymic | `empl_patronymic` | `VARCHAR(50)` | NULLABLE |
| Role / Position | `empl_role` | `VARCHAR(10)` | NOT NULL — either `'Manager'` or `'Cashier'` |
| Salary | `salary` | `DECIMAL(13,4)` | NOT NULL, ≥ 0 |
| Date of birth | `date_of_birth` | `DATE` | NOT NULL |
| Date of start | `date_of_start` | `DATE` | NOT NULL |
| Phone number | `phone_number` | `VARCHAR(13)` | NOT NULL |
| City | `city` | `VARCHAR(50)` | NOT NULL |
| Street | `street` | `VARCHAR(50)` | NOT NULL |
| Zip code | `zip_code` | `VARCHAR(9)` | NOT NULL |

**Integrity constraints:**

- Employee must be **at least 18 years old**: `current_date - INTERVAL '18 years' >= date_of_birth`.
- Phone number must be at most 13 characters (including `+` prefix).
- Salary must be non-negative.

### 5.2 Category

| Field | DB Column | Type | Constraints |
|---|---|---|---|
| Category number | `category_number` | `INT` | **PK**, NOT NULL |
| Category name | `category_name` | `VARCHAR(50)` | NOT NULL |

### 5.3 Product

| Field | DB Column | Type | Constraints |
|---|---|---|---|
| Product ID | `id_product` | `INT` | **PK**, NOT NULL |
| Category number | `category_number` | `INT` | **FK → Category**, NOT NULL, ON UPDATE CASCADE, ON DELETE NO ACTION |
| Product name | `product_name` | `VARCHAR(50)` | NOT NULL |
| Characteristics | `characteristics` | `VARCHAR(100)` | NOT NULL |

### 5.4 Store Product (Товар у магазині)

A **Store Product** represents a concrete sellable item on the shelf. Each Product may have **at most two** Store Product entries: one regular and one promotional.

| Field | DB Column | Type | Constraints |
|---|---|---|---|
| UPC | `UPC` | `VARCHAR(12)` | **PK**, NOT NULL |
| UPC of promotional counterpart | `UPC_prom` | `VARCHAR(12)` | **FK → Store_Product(UPC)**, NULLABLE, ON UPDATE SET NULL, ON DELETE SET NULL |
| Product ID | `id_product` | `INT` | **FK → Product**, NOT NULL, ON UPDATE CASCADE, ON DELETE NO ACTION |
| Selling price | `selling_price` | `DECIMAL(13,4)` | NOT NULL, ≥ 0 |
| Products number (quantity) | `products_number` | `INT` | NOT NULL, ≥ 0 |
| Promotional product | `promotional_product` | `BOOLEAN` | NOT NULL |

**Business rules:**

- **VAT is included** in `selling_price`. VAT = 20% of the price. All products are subject to VAT (no social-product exemptions in this store).
- **Promotional pricing**: When a product becomes promotional, its price is calculated as `regular_price × 0.8` (i.e., a fixed 20% discount applied to the regular product's selling price).
- A product becomes promotional when its expiry date is approaching **and** there is still a significant quantity in stock.
- **Price revaluation**: When a new batch of the same product arrives at a different purchase price, **all** existing units of that product (old and new batch) are re-priced to the new selling price.
- Each `Product` can have **at most 2** `Store_Product` rows — one where `promotional_product = FALSE` (regular) and one where `promotional_product = TRUE` (promotional).

### 5.5 Check (Receipt)

| Field | DB Column | Type | Constraints |
|---|---|---|---|
| Check number | `check_number` | `VARCHAR(10)` | **PK**, NOT NULL |
| Employee ID | `id_employee` | `VARCHAR(10)` | **FK → Employee**, NOT NULL, ON UPDATE CASCADE, ON DELETE NO ACTION |
| Card number | `card_number` | `VARCHAR(13)` | **FK → Customer_Card**, NULLABLE, ON UPDATE CASCADE, ON DELETE NO ACTION |
| Print date | `print_date` | `DATETIME` | NOT NULL |
| Sum total | `sum_total` | `DECIMAL(13,4)` | NOT NULL, ≥ 0 |
| VAT | `vat` | `DECIMAL(13,4)` | NOT NULL, ≥ 0 |

**Business rules:**

- `sum_total` = total amount the customer must pay for all products in the check (VAT included).
- `vat` = `sum_total × 0.2`.
- If a Customer Card is applied, the total may be reduced by the card's discount percentage. Only **one** card can be applied per check.
- Receipts are retained in the database for **3 years**.

### 5.6 Sale (Check detail / junction table)

| Field | DB Column | Type | Constraints |
|---|---|---|---|
| UPC | `UPC` | `VARCHAR(12)` | **PPK, FK → Store_Product**, NOT NULL, ON UPDATE CASCADE, ON DELETE NO ACTION |
| Check number | `check_number` | `VARCHAR(10)` | **PPK, FK → Check**, NOT NULL, ON UPDATE CASCADE, ON DELETE CASCADE |
| Product number (quantity) | `product_number` | `INT` | NOT NULL, ≥ 0 |
| Selling price | `selling_price` | `DECIMAL(13,4)` | NOT NULL, ≥ 0 |

**Business rules:**

- The `selling_price` is **snapshotted** at the time of sale, because the product's price may change later due to revaluation.
- One check can contain many products; one product can appear in many checks (many-to-many resolved by `Sale`).

### 5.7 Customer Card

| Field | DB Column | Type | Constraints |
|---|---|---|---|
| Card number | `card_number` | `VARCHAR(13)` | **PK**, NOT NULL |
| Surname | `cust_surname` | `VARCHAR(50)` | NOT NULL |
| Name | `cust_name` | `VARCHAR(50)` | NOT NULL |
| Patronymic | `cust_patronymic` | `VARCHAR(50)` | NULLABLE |
| Phone number | `phone_number` | `VARCHAR(13)` | NOT NULL |
| City | `city` | `VARCHAR(50)` | NULLABLE |
| Street | `street` | `VARCHAR(50)` | NULLABLE |
| Zip code | `zip_code` | `VARCHAR(9)` | NULLABLE |
| Percent (discount) | `percent` | `INT` | NOT NULL, ≥ 0 |

**Integrity constraints:**

- Phone number must be at most 13 characters (including `+`).
- Discount percent must be non-negative.
- Address fields (city, street, zip_code) are **optional**.

---

## 6. Relational Model — Foreign Key Actions Summary

| FK | ON UPDATE | ON DELETE |
|---|---|---|
| `Product.category_number → Category` | CASCADE | NO ACTION |
| `Store_Product.UPC_prom → Store_Product` | SET NULL | SET NULL |
| `Store_Product.id_product → Product` | CASCADE | NO ACTION |
| `Check.id_employee → Employee` | CASCADE | NO ACTION |
| `Check.card_number → Customer_Card` | CASCADE | NO ACTION |
| `Sale.UPC → Store_Product` | CASCADE | NO ACTION |
| `Sale.check_number → Check` | CASCADE | CASCADE |

---

## 7. Functional Requirements by Role

### 7.1 Manager

#### CRUD Operations

| Entity | Create | Read | Update | Delete |
|---|---|---|---|---|
| Employee | ✅ | ✅ | ✅ | ✅ |
| Category | ✅ | ✅ | ✅ | ✅ |
| Product | ✅ | ✅ | ✅ | ✅ |
| Store Product | ✅ | ✅ | ✅ | ✅ |
| Customer Card | ✅ | ✅ | ✅ | ✅ |
| Check (Receipt) | ❌ | ✅ | ❌ | ✅ |
| Sale | ❌ | ✅ | ❌ | (cascades with check) |

#### Query / Reporting Requirements (Manager)

1. **M-1.** View all employees, sorted by surname.
2. **M-2.** View all employees who hold the **Cashier** role, sorted by surname.
3. **M-3.** View all loyalty customers, sorted by surname.
4. **M-4.** View all categories, sorted by name.
5. **M-5.** View all products, sorted by name.
6. **M-6.** View all store products, sorted by quantity.
7. **M-7.** Search for an employee's phone number and address **by surname**.
8. **M-8.** View all loyalty customers with a **specific discount percentage**, sorted by surname.
9. **M-9.** Search all products **belonging to a specific category**, sorted by name.
10. **M-10.** By **UPC**, find the selling price, quantity in stock, product name, and product characteristics.
11. **M-11.** View all **promotional** store products, sorted by quantity **or** by name.
12. **M-12.** View all **non-promotional** store products, sorted by quantity **or** by name.
13. **M-13.** View all checks created by a **specific cashier** within a **given date range** (with the ability to drill down and see the purchased products in each check: name, quantity, price).
14. **M-14.** View all checks created by **all cashiers** within a **given date range** (with the same drill-down ability).
15. **M-15.** Determine the **total sales sum** from checks created by a **specific cashier** within a given date range.
16. **M-16.** Determine the **total sales sum** from checks created by **all cashiers** within a given date range.
17. **M-17.** Determine the **total quantity** of a specific product sold within a given date range.
18. **M-18.** Print reports containing information about all employees, loyalty customers, categories, products, store products, and checks.

### 7.2 Cashier

#### CRUD Operations

| Entity | Create | Read | Update | Delete |
|---|---|---|---|---|
| Employee | ❌ | Own info only | ❌ | ❌ |
| Category | ❌ | ✅ | ❌ | ❌ |
| Product | ❌ | ✅ | ❌ | ❌ |
| Store Product | ❌ | ✅ | ❌ | ❌ |
| Customer Card | ✅ | ✅ | ✅ | ❌ |
| Check (Receipt) | ✅ | Own checks only | ❌ | ❌ |
| Sale | ✅ (as part of check) | Own sales only | ❌ | ❌ |

#### Query / Reporting Requirements (Cashier)

1. **C-1.** View all products, sorted by name.
2. **C-2.** View all store products, sorted by name.
3. **C-3.** View all loyalty customers, sorted by surname.
4. **C-4.** Search products **by name**.
5. **C-5.** Search products **belonging to a specific category**, sorted by name.
6. **C-6.** Search loyalty customers **by surname**.
7. **C-7.** Create a new sale (add a check with line items). When creating a check:
   - Select products by UPC.
   - Specify quantity for each product.
   - Optionally apply a Customer Card.
   - The system must automatically calculate `sum_total` and `vat`.
   - The system must **decrement** `products_number` in `Store_Product` for each sold item.
8. **C-8.** Add / edit Customer Card information.
9. **C-9.** View all checks created by **this cashier today**.
10. **C-10.** View all checks created by **this cashier** within a **given date range**.
11. **C-11.** By **check number**, view full details of a check including: product names, quantities, and prices for all items in the check.
12. **C-12.** View all **promotional** store products, sorted by quantity **or** by name.
13. **C-13.** View all **non-promotional** store products, sorted by quantity **or** by name.
14. **C-14.** By **UPC**, find the selling price and quantity in stock.
15. **C-15.** View own employee information (all personal details).

---

## 8. UI / UX Requirements

### 8.1 General Principles

- The interface must be **user-friendly** and designed for **non-technical users** (not programmers).
- Raw database tables must **never** be displayed directly to the user.
- When editing data that involves foreign keys (e.g., selecting a category for a product), the UI must present a **dropdown list** showing human-readable values (e.g., category name), not raw IDs. The user should never need to manually type foreign key values.
- Navigation and button labels must be **functionally descriptive** (e.g., "Employees", "Products", "Sales History") — never generic labels like "Query 1", "Simple Queries", "Complex Queries", etc.

### 8.2 Reports / Printing

- A "Print Report" action must **not** immediately send to the printer. It must first show a **print preview**.
- Reports must include:
  - A **header** (top of each page).
  - A **footer** (bottom of each page).
  - Tables that span the **full width** of the page.
- Reports must **not** include the page URL/address.

### 8.3 HTMX Integration Notes

Since HTMX is used for frontend interactivity:

- Use `hx-get`, `hx-post`, `hx-put`, `hx-delete` for AJAX-style CRUD operations without full page reloads.
- Use `hx-trigger`, `hx-target`, and `hx-swap` for dynamic partial updates (e.g., filtering product lists, searching employees by surname, drill-down into check details).
- Forms for creating/editing records should submit via HTMX and return partial HTML fragments.
- Sorting and filtering operations (e.g., sort by name, sort by quantity, filter by category) should be handled with HTMX requests to server-side views that return updated table partials.

---

## 9. Database Access Layer — Implementation Notes

### 9.1 Django ORM Usage (Schema Only)

```python
# ALLOWED — Define models for schema generation / migrations
class Employee(models.Model):
    id_employee = models.CharField(max_length=10, primary_key=True)
    empl_surname = models.CharField(max_length=50)
    # ... etc.

# FORBIDDEN — Do not use ORM for queries
Employee.objects.filter(empl_role='Cashier')  # ❌ NOT ALLOWED
Employee.objects.all().order_by('empl_surname')  # ❌ NOT ALLOWED
```

### 9.2 Raw SQL Execution Pattern

```python
from django.db import connection

def get_cashiers_sorted_by_surname():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id_employee, empl_surname, empl_name, empl_patronymic,
                   salary, date_of_birth, date_of_start, phone_number,
                   city, street, zip_code
            FROM Employee
            WHERE empl_role = 'Cashier'
            ORDER BY empl_surname ASC;
        """)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
```

All views/services must follow this pattern. Parameterized queries must be used to prevent SQL injection:

```python
cursor.execute(
    "SELECT * FROM Employee WHERE id_employee = %s",
    [employee_id]
)
```

---

## 10. Business Logic Summary

| Rule | Formula / Detail |
|---|---|
| VAT rate | 20% included in selling price |
| VAT calculation on check | `vat = sum_total × 0.2` |
| Promotional discount | Fixed 20% off the regular price |
| Promotional price | `regular_selling_price × 0.8` |
| Max store products per product | 2 (one regular, one promotional) |
| Customer card discount | Applied to `sum_total` before finalizing the check |
| Check retention period | 3 years |
| Minimum employee age | 18 years |
| Phone number max length | 13 characters (including `+`) |
| Price revaluation | When a new batch arrives at a different price, **all** existing units are re-priced |

---

## 11. Docker Setup

The application should be containerized with at minimum:

| Container | Purpose |
|---|---|
| `web` | Django application server (with HTMX templates and Tailwind CSS) |
| `db` | PostgreSQL database |

A `docker-compose.yml` must orchestrate both services. The database should persist data via a Docker volume. Environment variables (DB credentials, secret key, etc.) should be managed via `.env` file.

---

## 12. Entity-Relationship Overview

```
Category (1) ──────< (N) Product (1) ──────< (N≤2) Store_Product
                                                        │
                                                        │ (M)
                                                        │
Employee (1) ──────< (N) Check (M) ─── Sale ───(N) Store_Product
                           │
                           │ (N)
                           │
                     Customer_Card (1) ──── (applied to, optional)
```

- **Category → Product**: One category has many products; each product belongs to exactly one category.
- **Product → Store_Product**: One product has at most 2 store products (regular + promotional).
- **Store_Product ↔ Check**: Many-to-many through `Sale` junction table.
- **Employee → Check**: One employee (cashier) creates many checks.
- **Customer_Card → Check**: One card can be applied to many checks; each check uses at most one card (optional).

---

## 13. Summary of All Database Tables

| # | Table | PK | Description |
|---|---|---|---|
| 1 | `Employee` | `id_employee` | All supermarket workers (managers and cashiers) |
| 2 | `Category` | `category_number` | Product categories |
| 3 | `Product` | `id_product` | Product catalog entries |
| 4 | `Store_Product` | `UPC` | Actual items on shelves with prices and quantities |
| 5 | `Check` | `check_number` | Sales receipts |
| 6 | `Sale` | `(UPC, check_number)` | Line items — which products in which check |
| 7 | `Customer_Card` | `card_number` | Loyalty program members |