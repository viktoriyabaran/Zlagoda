from django.core.management.base import BaseCommand
from django.utils import timezone

from products.services import EXPIRY_PROMO_WINDOW_DAYS, apply_expiring_promotions


class Command(BaseCommand):
    help = (
        "Move soon-to-expire regular products onto their promotional variant "
        "and zero out promotional stock that has reached its expiration date. "
        "Intended to run nightly."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=EXPIRY_PROMO_WINDOW_DAYS,
            help="Days before expiration at which to start the promotion "
            f"(default: {EXPIRY_PROMO_WINDOW_DAYS}).",
        )

    def handle(self, *args, **options):
        result = apply_expiring_promotions(timezone.localdate(), options["days"])
        self.stdout.write(
            self.style.SUCCESS(
                f"Expiring promotions applied: {result['moved']} moved to promo, "
                f"{result['zeroed']} expired promo zeroed."
            )
        )
