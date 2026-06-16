from . import repository


class StatisticsService:
    def get_customer_purchase_stats(self) -> list:
        return repository.get_customer_purchase_stats()

    def get_cashiers_served_all_customers(self, surname: str = None) -> list:
        return repository.get_cashiers_served_all_customers(surname)
