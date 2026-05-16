from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0007_restore_product_category_fk"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE products_product
                    DROP CONSTRAINT products_product_category_number_id_fk_products_category;

                ALTER TABLE products_product
                    ADD CONSTRAINT products_product_category_number_id_fk_products_category
                    FOREIGN KEY (category_number_id)
                    REFERENCES products_category(id)
                    ON UPDATE CASCADE ON DELETE NO ACTION
                    DEFERRABLE INITIALLY DEFERRED;

                ALTER TABLE products_storeproduct
                    DROP CONSTRAINT "products_storeproduc_UPC_prom_id_d00dfaac_fk_products_";

                ALTER TABLE products_storeproduct
                    ADD CONSTRAINT "products_storeproduct_UPC_prom_fk_products_storeproduct"
                    FOREIGN KEY ("UPC_prom_id")
                    REFERENCES products_storeproduct("UPC")
                    ON UPDATE CASCADE ON DELETE SET NULL
                    DEFERRABLE INITIALLY DEFERRED;

                ALTER TABLE products_storeproduct
                    DROP CONSTRAINT products_storeproduc_id_product_id_a98d17c0_fk_products_;

                ALTER TABLE products_storeproduct
                    ADD CONSTRAINT products_storeproduct_id_product_fk_products_product
                    FOREIGN KEY (id_product_id)
                    REFERENCES products_product(id_product)
                    ON UPDATE CASCADE ON DELETE NO ACTION
                    DEFERRABLE INITIALLY DEFERRED;
            """,
            reverse_sql="""
                ALTER TABLE products_product
                    DROP CONSTRAINT products_product_category_number_id_fk_products_category;

                ALTER TABLE products_product
                    ADD CONSTRAINT products_product_category_number_id_fk_products_category
                    FOREIGN KEY (category_number_id)
                    REFERENCES products_category(id)
                    DEFERRABLE INITIALLY DEFERRED;

                ALTER TABLE products_storeproduct
                    DROP CONSTRAINT "products_storeproduct_UPC_prom_fk_products_storeproduct";

                ALTER TABLE products_storeproduct
                    ADD CONSTRAINT "products_storeproduc_UPC_prom_id_d00dfaac_fk_products_"
                    FOREIGN KEY ("UPC_prom_id")
                    REFERENCES products_storeproduct("UPC")
                    DEFERRABLE INITIALLY DEFERRED;

                ALTER TABLE products_storeproduct
                    DROP CONSTRAINT products_storeproduct_id_product_fk_products_product;

                ALTER TABLE products_storeproduct
                    ADD CONSTRAINT products_storeproduc_id_product_id_a98d17c0_fk_products_
                    FOREIGN KEY (id_product_id)
                    REFERENCES products_product(id_product)
                    DEFERRABLE INITIALLY DEFERRED;
            """,
        ),
    ]
