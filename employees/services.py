from typing import Protocol

from employees.repository import (
    create_employee,
)


class IEmployeeService(Protocol):
    def create_employee(self, data: dict) -> None: ...


class EmployeeService:
    def create_employee(self, data: dict) -> None:
        create_employee(data)
