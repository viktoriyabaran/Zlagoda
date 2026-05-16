from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0006_alter_product_category_number_and_more"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE products_product
                ADD CONSTRAINT products_product_category_number_id_fk_products_category
                FOREIGN KEY (category_number_id)
                REFERENCES products_category(id)
                DEFERRABLE INITIALLY DEFERRED;
            """,
            reverse_sql="""
                ALTER TABLE products_product
                DROP CONSTRAINT products_product_category_number_id_fk_products_category;
            """,
        ),
    ]
