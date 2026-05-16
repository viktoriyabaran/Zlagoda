from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_user_employee"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE core_user
                    DROP CONSTRAINT core_user_id_employee_c781f3b7_fk_employees;

                ALTER TABLE core_user
                    ADD CONSTRAINT core_user_id_employee_fk_employees_employee
                    FOREIGN KEY (id_employee)
                    REFERENCES employees_employee(id_employee)
                    ON UPDATE CASCADE ON DELETE SET NULL
                    DEFERRABLE INITIALLY DEFERRED;
            """,
            reverse_sql="""
                ALTER TABLE core_user
                    DROP CONSTRAINT core_user_id_employee_fk_employees_employee;

                ALTER TABLE core_user
                    ADD CONSTRAINT core_user_id_employee_c781f3b7_fk_employees
                    FOREIGN KEY (id_employee)
                    REFERENCES employees_employee(id_employee)
                    DEFERRABLE INITIALLY DEFERRED;
            """,
        ),
    ]
