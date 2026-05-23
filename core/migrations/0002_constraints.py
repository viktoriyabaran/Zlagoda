from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE core_user
                    DROP CONSTRAINT core_user_employee_id_aa241a94_fk_employees_employee_id;

                ALTER TABLE core_user
                    ADD CONSTRAINT core_user_employee_fk_employees_employee
                    FOREIGN KEY (employee_id)
                    REFERENCES employees_employee(id)
                    ON UPDATE CASCADE ON DELETE SET NULL
                    DEFERRABLE INITIALLY DEFERRED;
            """,
            reverse_sql="""
                ALTER TABLE core_user
                    DROP CONSTRAINT core_user_employee_fk_employees_employee;

                ALTER TABLE core_user
                    ADD CONSTRAINT core_user_employee_id_aa241a94_fk_employees_employee_id
                    FOREIGN KEY (employee_id)
                    REFERENCES employees_employee(id)
                    DEFERRABLE INITIALLY DEFERRED;
            """,
        ),
    ]
