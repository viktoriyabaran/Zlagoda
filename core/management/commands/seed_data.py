from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.db import transaction

from core.db import execute_insert_returning, execute_write


class Command(BaseCommand):
    help = "Populate the database with lean test data covering every feature."

    def handle(self, *args, **options):
        with transaction.atomic():
            self._wipe()
            categories = self._seed_categories()
            products = self._seed_products(categories)
            store_products = self._seed_store_products(products)
            employees = self._seed_employees()
            self._seed_users(employees)
            customers = self._seed_customers()
            self._seed_checks_and_sales(employees, customers, store_products)
        self.stdout.write(self.style.SUCCESS("Seed data loaded."))

    def _wipe(self):
        for table in (
            "sales_sale",
            "sales_check",
            "core_user",
            "products_storeproduct",
            "products_product",
            "products_category",
            "customers_customercard",
            "employees_employee",
        ):
            execute_write(f"DELETE FROM {table}")

    def _seed_categories(self) -> dict[str, int]:
        names = ["Dairy", "Bakery", "Beverages", "Snacks", "Household"]
        ids = {}
        for name in names:
            ids[name] = execute_insert_returning(
                "INSERT INTO products_category (category_name) VALUES (%s) RETURNING id",
                [name],
            )
        return ids

    def _seed_products(self, categories: dict[str, int]) -> dict[str, int]:
        rows = [
            ("Milk 1L", "Pasteurized whole milk, 3.2% fat", "Molokiya", "Dairy"),
            ("Yogurt 200g", "Natural plain yogurt", "Danone", "Dairy"),
            ("Cheese 200g", "Mild gouda, sliced", "Blagovir", "Dairy"),
            ("White Bread", "Classic loaf, 500g", "Kyivkhlib", "Bakery"),
            ("Croissant", "Butter croissant, single", "Kyivkhlib", "Bakery"),
            ("Whole Wheat Bread", "Sliced loaf, 500g", "Kyivkhlib", "Bakery"),
            ("Cola 1.5L", "Carbonated soft drink", "Coca-Cola", "Beverages"),
            ("Orange Juice 1L", "Not-from-concentrate", "Sandora", "Beverages"),
            ("Mineral Water 1.5L", "Still spring water", "Morshynska", "Beverages"),
            ("Beer 0.5L", "Lager, 4.7% ABV", "Obolon", "Beverages"),
            ("Chips 100g", "Salted potato chips", "Lays", "Snacks"),
            ("Chocolate Bar", "Milk chocolate, 90g", "Roshen", "Snacks"),
            ("Crackers 200g", "Salted crackers", "Yarych", "Snacks"),
            ("Soap", "Bar soap, lavender", "Dove", "Household"),
            ("Toilet Paper 8pk", "2-ply, 8 rolls", "Zewa", "Household"),
        ]

        ids = {}
        for name, characteristics, manufacturer, category in rows:
            ids[name] = execute_insert_returning(
                """
                INSERT INTO products_product (product_name, characteristics, manufacturer, category_id)
                VALUES (%s, %s, %s, %s) RETURNING id
                """,
                [name, characteristics, manufacturer, categories[category]],
            )
        return ids

    def _seed_store_products(self, products: dict[str, int]) -> list[str]:
        rows = [
            ("Milk 1L", "100000000001", Decimal("32.00"), 120, 5, 40),
            ("Yogurt 200g", "100000000002", Decimal("18.00"), 80, 4, None),
            ("Cheese 200g", "100000000003", Decimal("95.00"), 30, 25, 10),
            ("White Bread", "100000000004", Decimal("25.00"), 60, 2, None),
            ("Croissant", "100000000005", Decimal("22.50"), 45, 3, 15),
            ("Whole Wheat Bread", "100000000006", Decimal("28.00"), 40, 6, None),
            ("Cola 1.5L", "100000000007", Decimal("40.00"), 100, 200, 30),
            ("Orange Juice 1L", "100000000008", Decimal("55.00"), 50, 45, None),
            ("Mineral Water 1.5L", "100000000009", Decimal("18.00"), 150, 365, None),
            ("Beer 0.5L", "100000000010", Decimal("35.00"), 90, 120, 25),
            ("Chips 100g", "100000000011", Decimal("30.00"), 70, 90, None),
            ("Chocolate Bar", "100000000012", Decimal("28.00"), 65, 150, 20),
            ("Crackers 200g", "100000000013", Decimal("32.50"), 55, 100, None),
            ("Soap", "100000000014", Decimal("15.00"), 80, 730, None),
            ("Toilet Paper 8pk", "100000000015", Decimal("120.00"), 35, 999, 10),
        ]
        today = date.today()
        all_upcs: list[str] = []
        for name, upc, price, qty, expires_in_days, promo_qty in rows:
            expiration = today + timedelta(days=expires_in_days)
            execute_write(
                """
                INSERT INTO products_storeproduct
                ("UPC", product_id, selling_price, products_number,
                 promotional_product, "UPC_prom_id", expiration_date)
                VALUES (%s, %s, %s, %s, FALSE, NULL, %s)
                """,
                [upc, products[name], price, qty, expiration],
            )
            all_upcs.append(upc)
            if promo_qty is not None:
                promo_upc = "2" + upc[1:]
                promo_price = (price * Decimal("0.8")).quantize(Decimal("0.0001"))
                execute_write(
                    """
                    INSERT INTO products_storeproduct
                    ("UPC", product_id, selling_price, products_number,
                     promotional_product, "UPC_prom_id", expiration_date)
                    VALUES (%s, %s, %s, %s, TRUE, %s, %s)
                    """,
                    [
                        promo_upc,
                        products[name],
                        promo_price,
                        promo_qty,
                        upc,
                        expiration,
                    ],
                )
                all_upcs.append(promo_upc)
        return all_upcs

    def _seed_employees(self) -> dict[str, int]:
        rows = [
            (
                "Manager",
                "Shevchenko",
                "Olena",
                "Petrivna",
                Decimal("45000.00"),
                date(1985, 4, 12),
                date(2018, 3, 1),
                "+380501112233",
                "Kyiv",
                "Khreshchatyk 1",
                "01001",
            ),
            (
                "Manager",
                "Kovalenko",
                "Andriy",
                "Vasylovych",
                Decimal("42000.00"),
                date(1980, 7, 23),
                date(2019, 6, 15),
                "+380502223344",
                "Kyiv",
                "Sahaidachnoho 5",
                "04070",
            ),
            (
                "Cashier",
                "Bondar",
                "Iryna",
                "Mykolaivna",
                Decimal("18000.00"),
                date(1995, 2, 5),
                date(2022, 9, 1),
                "+380503334455",
                "Kyiv",
                "Velyka Vasylkivska 30",
                "01004",
            ),
            (
                "Cashier",
                "Tkachenko",
                "Yulia",
                None,
                Decimal("17500.00"),
                date(1998, 11, 18),
                date(2023, 1, 10),
                "+380504445566",
                "Kyiv",
                "Lva Tolstoho 9",
                "01032",
            ),
            (
                "Cashier",
                "Melnyk",
                "Dmytro",
                "Ivanovych",
                Decimal("18500.00"),
                date(1992, 9, 30),
                date(2021, 4, 20),
                "+380505556677",
                "Kyiv",
                "Antonovycha 50",
                "01033",
            ),
            (
                "Cashier",
                "Sydorenko",
                "Kateryna",
                "Olehivna",
                Decimal("17800.00"),
                date(2000, 6, 14),
                date(2024, 2, 1),
                "+380506667788",
                "Kyiv",
                "Velyka Zhytomyrska 22",
                "01025",
            ),
        ]
        ids: dict[str, int] = {}
        for (
            role,
            surname,
            name,
            patronymic,
            salary,
            dob,
            dos,
            phone,
            city,
            street,
            zip_code,
        ) in rows:
            emp_id = execute_insert_returning(
                """
                INSERT INTO employees_employee
                (empl_role, empl_surname, empl_name, empl_patronymic, salary,
                 date_of_birth, date_of_start, phone_number, city, street, zip_code)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                [
                    role,
                    surname,
                    name,
                    patronymic,
                    salary,
                    dob,
                    dos,
                    phone,
                    city,
                    street,
                    zip_code,
                ],
            )
            assert emp_id is not None
            ids[surname] = emp_id
        return ids

    def _seed_users(self, employees: dict[str, int]) -> None:
        # username, password, employee surname
        rows = [
            ("olena", "password", "Shevchenko"),  # manager
            ("iryna", "password", "Bondar"),  # cashier
        ]
        for username, password, surname in rows:
            execute_write(
                "INSERT INTO core_user (username, password, employee_id) VALUES (%s, %s, %s)",
                [username, make_password(password), employees[surname]],
            )

    def _seed_customers(self) -> list[int]:
        rows = [
            (
                "Petrenko",
                "Olha",
                "Stepanivna",
                "+380671234567",
                "Kyiv",
                "Shevchenka 12",
                "01001",
                5,
            ),
            (
                "Ivanov",
                "Maksym",
                "Yurievich",
                "+380672345678",
                "Kyiv",
                "Franka 4",
                "01030",
                2,
            ),
            ("Yakovenko", "Nina", None, "+380673456789", None, None, None, 15),
            (
                "Hryhoriev",
                "Roman",
                "Petrovich",
                "+380674567890",
                "Lviv",
                "Rynok 7",
                "79008",
                5,
            ),
            (
                "Symonenko",
                "Anna",
                "Andriivna",
                "+380675678901",
                "Kyiv",
                "Pushkinska 18",
                "01004",
                1,
            ),
            (
                "Lysenko",
                "Vasyl",
                "Mykolayovych",
                "+380676789012",
                "Odesa",
                "Derybasivska 3",
                "65000",
                3,
            ),
            (
                "Hrytsenko",
                "Tamara",
                "Ivanivna",
                "+380677890123",
                "Kyiv",
                "Saksahanskoho 9",
                "01032",
                0,
            ),
            (
                "Marchenko",
                "Yevhen",
                "Borysovych",
                "+380678901234",
                "Kyiv",
                "Reitarska 35",
                "01054",
                1,
            ),
        ]
        ids: list[int] = []
        for surname, name, patronymic, phone, city, street, zip_code, percent in rows:
            cust_id = execute_insert_returning(
                """
                INSERT INTO customers_customercard
                (cust_surname, cust_name, cust_patronymic, phone_number, city, street, zip_code, percent)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                [surname, name, patronymic, phone, city, street, zip_code, percent],
            )
            assert cust_id is not None
            ids.append(cust_id)
        return ids

    def _seed_checks_and_sales(
        self,
        employees: dict[str, int],
        customers: list[int],
        upcs: list[str],
    ) -> None:
        cashier_surnames = ["Bondar", "Tkachenko", "Melnyk", "Sydorenko"]
        now = datetime.now(tz=timezone.utc).replace(microsecond=0)

        # (offset_days, cashier_surname, customer_index or None, [(upc_index, qty), ...])
        plan = [
            (0, "Bondar", 0, [(0, 2), (4, 1), (10, 3)]),
            (0, "Bondar", None, [(2, 1), (8, 4)]),
            (1, "Tkachenko", 1, [(6, 2), (11, 2), (13, 1)]),
            (1, "Melnyk", None, [(7, 1), (12, 1)]),
            (2, "Melnyk", 2, [(0, 1), (3, 2), (8, 2)]),
            (3, "Sydorenko", 4, [(14, 1), (10, 1)]),
            (4, "Bondar", None, [(1, 3), (5, 2), (9, 1)]),
            (5, "Tkachenko", 5, [(0, 1), (2, 1), (11, 2)]),
            (7, "Sydorenko", 7, [(4, 2), (6, 1), (12, 2)]),
            (10, "Melnyk", None, [(8, 1), (9, 2), (13, 3)]),
        ]

        for offset, surname, cust_idx, line_items in plan:
            print_date = now - timedelta(days=offset, hours=offset % 6)
            sum_total = Decimal("0")
            sales_payload = []
            for upc_idx, qty in line_items:
                upc = upcs[upc_idx]
                price = self._get_store_product_price(upc)
                sales_payload.append((upc, qty, price))
                sum_total += price * qty

            card_id = customers[cust_idx] if cust_idx is not None else None
            vat = (sum_total * Decimal("0.2")).quantize(Decimal("0.0001"))

            check_id = execute_insert_returning(
                """
                INSERT INTO sales_check
                (employee_id, card_id, print_date, sum_total, vat)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                [
                    employees[surname],
                    card_id,
                    print_date,
                    sum_total.quantize(Decimal("0.0001")),
                    vat,
                ],
            )

            for upc, qty, price in sales_payload:
                execute_write(
                    """
                    INSERT INTO sales_sale ("UPC", check_number_id, product_number, selling_price)
                    VALUES (%s, %s, %s, %s)
                    """,
                    [upc, check_id, qty, price],
                )
                execute_write(
                    'UPDATE products_storeproduct SET products_number = products_number - %s WHERE "UPC" = %s',
                    [qty, upc],
                )

    def _get_store_product_price(self, upc: str) -> Decimal:
        from core.db import execute_single

        row = execute_single(
            'SELECT selling_price FROM products_storeproduct WHERE "UPC" = %s',
            [upc],
        )
        assert row is not None
        return row["selling_price"]
