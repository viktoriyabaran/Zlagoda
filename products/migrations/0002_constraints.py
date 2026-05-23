from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE products_product
                    DROP CONSTRAINT products_product_category_id_9b594869_fk_products_category_id;

                ALTER TABLE products_product
                    ADD CONSTRAINT products_product_category_fk_products_category
                    FOREIGN KEY (category_id)
                    REFERENCES products_category(id)
                    ON UPDATE CASCADE ON DELETE NO ACTION
                    DEFERRABLE INITIALLY DEFERRED;

                ALTER TABLE products_storeproduct
                    DROP CONSTRAINT "products_storeproduc_UPC_prom_id_d00dfaac_fk_products_";

                ALTER TABLE products_storeproduct
                    ADD CONSTRAINT "products_storeproduct_UPC_prom_fk_products_storeproduct"
                    FOREIGN KEY ("UPC_prom_id")
                    REFERENCES products_storeproduct("UPC")
                    ON UPDATE SET NULL ON DELETE SET NULL
                    DEFERRABLE INITIALLY DEFERRED;

                ALTER TABLE products_storeproduct
                    DROP CONSTRAINT products_storeproduc_product_id_4ee05405_fk_products_;

                ALTER TABLE products_storeproduct
                    ADD CONSTRAINT products_storeproduct_product_fk_products_product
                    FOREIGN KEY (product_id)
                    REFERENCES products_product(id)
                    ON UPDATE CASCADE ON DELETE NO ACTION
                    DEFERRABLE INITIALLY DEFERRED;
            """,
            reverse_sql="""
                ALTER TABLE products_product
                    DROP CONSTRAINT products_product_category_fk_products_category;

                ALTER TABLE products_product
                    ADD CONSTRAINT products_product_category_id_9b594869_fk_products_category_id
                    FOREIGN KEY (category_id)
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
                    DROP CONSTRAINT products_storeproduct_product_fk_products_product;

                ALTER TABLE products_storeproduct
                    ADD CONSTRAINT products_storeproduc_product_id_4ee05405_fk_products_
                    FOREIGN KEY (product_id)
                    REFERENCES products_product(id)
                    DEFERRABLE INITIALLY DEFERRED;
            """,
        ),
    ]
