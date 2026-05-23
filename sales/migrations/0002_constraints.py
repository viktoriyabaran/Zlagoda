from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("sales", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE sales_check
                    DROP CONSTRAINT sales_check_employee_id_6f07d1d2_fk_employees_employee_id;

                ALTER TABLE sales_check
                    ADD CONSTRAINT sales_check_employee_fk_employees_employee
                    FOREIGN KEY (employee_id)
                    REFERENCES employees_employee(id)
                    ON UPDATE CASCADE ON DELETE NO ACTION
                    DEFERRABLE INITIALLY DEFERRED;

                ALTER TABLE sales_check
                    DROP CONSTRAINT sales_check_card_id_bef4d934_fk_customers_customercard_id;

                ALTER TABLE sales_check
                    ADD CONSTRAINT sales_check_card_fk_customers_customercard
                    FOREIGN KEY (card_id)
                    REFERENCES customers_customercard(id)
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
                    DROP CONSTRAINT sales_sale_check_number_id_e240bb29_fk_sales_check_id;

                ALTER TABLE sales_sale
                    ADD CONSTRAINT sales_sale_check_number_fk_sales_check
                    FOREIGN KEY (check_number_id)
                    REFERENCES sales_check(id)
                    ON UPDATE CASCADE ON DELETE CASCADE
                    DEFERRABLE INITIALLY DEFERRED;
            """,
            reverse_sql="""
                ALTER TABLE sales_check
                    DROP CONSTRAINT sales_check_employee_fk_employees_employee;

                ALTER TABLE sales_check
                    ADD CONSTRAINT sales_check_employee_id_6f07d1d2_fk_employees_employee_id
                    FOREIGN KEY (employee_id)
                    REFERENCES employees_employee(id)
                    DEFERRABLE INITIALLY DEFERRED;

                ALTER TABLE sales_check
                    DROP CONSTRAINT sales_check_card_fk_customers_customercard;

                ALTER TABLE sales_check
                    ADD CONSTRAINT sales_check_card_id_bef4d934_fk_customers_customercard_id
                    FOREIGN KEY (card_id)
                    REFERENCES customers_customercard(id)
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
                    ADD CONSTRAINT sales_sale_check_number_id_e240bb29_fk_sales_check_id
                    FOREIGN KEY (check_number_id)
                    REFERENCES sales_check(id)
                    DEFERRABLE INITIALLY DEFERRED;
            """,
        ),
    ]
