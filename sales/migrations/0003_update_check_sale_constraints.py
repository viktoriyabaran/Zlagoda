from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("sales", "0002_sale"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE sales_check
                    DROP CONSTRAINT sales_check_id_employee_ef643ddd_fk_employees;

                ALTER TABLE sales_check
                    ADD CONSTRAINT sales_check_id_employee_fk_employees_employee
                    FOREIGN KEY (id_employee)
                    REFERENCES employees_employee(id_employee)
                    ON UPDATE CASCADE ON DELETE NO ACTION
                    DEFERRABLE INITIALLY DEFERRED;

                ALTER TABLE sales_check
                    DROP CONSTRAINT sales_check_card_number_7ebc27d4_fk_customers;

                ALTER TABLE sales_check
                    ADD CONSTRAINT sales_check_card_number_fk_customers_customercard
                    FOREIGN KEY (card_number)
                    REFERENCES customers_customercard(card_number)
                    ON UPDATE CASCADE ON DELETE NO ACTION
                    DEFERRABLE INITIALLY DEFERRED;

                ALTER TABLE sales_sale
                    DROP CONSTRAINT "sales_sale_UPC_ffc92aea_fk_products_storeproduct_UPC";

                ALTER TABLE sales_sale
                    ADD CONSTRAINT "sales_sale_UPC_fk_products_storeproduct"
                    FOREIGN KEY ("UPC")
                    REFERENCES products_storeproduct("UPC")
                    ON UPDATE CASCADE ON DELETE NO ACTION
                    DEFERRABLE INITIALLY DEFERRED;

                ALTER TABLE sales_sale
                    DROP CONSTRAINT sales_sale_check_number_6c8d1882_fk_sales_check_check_number;

                ALTER TABLE sales_sale
                    ADD CONSTRAINT sales_sale_check_number_fk_sales_check
                    FOREIGN KEY (check_number)
                    REFERENCES sales_check(check_number)
                    ON UPDATE CASCADE ON DELETE CASCADE
                    DEFERRABLE INITIALLY DEFERRED;
            """,
            reverse_sql="""
                ALTER TABLE sales_check
                    DROP CONSTRAINT sales_check_id_employee_fk_employees_employee;

                ALTER TABLE sales_check
                    ADD CONSTRAINT sales_check_id_employee_ef643ddd_fk_employees
                    FOREIGN KEY (id_employee)
                    REFERENCES employees_employee(id_employee)
                    DEFERRABLE INITIALLY DEFERRED;

                ALTER TABLE sales_check
                    DROP CONSTRAINT sales_check_card_number_fk_customers_customercard;

                ALTER TABLE sales_check
                    ADD CONSTRAINT sales_check_card_number_7ebc27d4_fk_customers
                    FOREIGN KEY (card_number)
                    REFERENCES customers_customercard(card_number)
                    DEFERRABLE INITIALLY DEFERRED;

                ALTER TABLE sales_sale
                    DROP CONSTRAINT "sales_sale_UPC_fk_products_storeproduct";

                ALTER TABLE sales_sale
                    ADD CONSTRAINT "sales_sale_UPC_ffc92aea_fk_products_storeproduct_UPC"
                    FOREIGN KEY ("UPC")
                    REFERENCES products_storeproduct("UPC")
                    DEFERRABLE INITIALLY DEFERRED;

                ALTER TABLE sales_sale
                    DROP CONSTRAINT sales_sale_check_number_fk_sales_check;

                ALTER TABLE sales_sale
                    ADD CONSTRAINT sales_sale_check_number_6c8d1882_fk_sales_check_check_number
                    FOREIGN KEY (check_number)
                    REFERENCES sales_check(check_number)
                    DEFERRABLE INITIALLY DEFERRED;
            """,
        ),
    ]
