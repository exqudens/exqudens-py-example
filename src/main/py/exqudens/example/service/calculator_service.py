from logging import LoggerAdapter
from logging import getLogger as logging_get_logger
import decimal
from decimal import Decimal

class CalculatorService:
    """
    CalculatorService class.
    """
    __logger: None | LoggerAdapter = None

    def __init__(
        self,
        logger: None | LoggerAdapter | object = None
    ) -> None:
        try:
            if isinstance(logger, LoggerAdapter):
                self.__logger = logger
            else:
                self.__logger = LoggerAdapter(logger=logging_get_logger(f"{self.__module__}.{self.__class__.__name__}"))
        except Exception as e:
            if isinstance(self.__logger, LoggerAdapter): self.__logger.error(e, exc_info=True)
            raise e

    def generate_amortization(
        self,
        principal,
        annual_rate,
        months,
        extra_monthly_principal=0
    ) -> list[dict[str, str]]:
        try:
            # Convert all inputs to Decimal objects
            principal = Decimal(str(principal))
            annual_rate = Decimal(str(annual_rate))
            extra_monthly_principal = Decimal(str(extra_monthly_principal))

            # Calculate monthly interest rate (r)
            monthly_rate = (annual_rate / Decimal("100")) / Decimal("12")

            # Quantization template for standard currency formatting ($0.01)
            cents = Decimal("0.01")

            # Calculate standard monthly base payment (EMI) using total months (n) directly
            if monthly_rate == 0:
                base_payment = principal / Decimal(str(months))
            else:
                # Formula: P * (R * (1 + R)^N) / ((1 + R)^N - 1)
                rate_factor = (Decimal("1") + monthly_rate) ** months
                base_payment = (
                    principal
                    * (monthly_rate * rate_factor)
                    / (rate_factor - Decimal("1"))
                )

            schedule = []
            balance = principal
            current_month = 0

            while balance > Decimal("0.01") and current_month < months:
                current_month += 1

                # Calculate interest based on the current period balance
                interest_paid = balance * monthly_rate
                scheduled_principal = base_payment - interest_paid
                total_principal_payment = scheduled_principal + extra_monthly_principal

                # Handle final payment constraints to prevent negative balances
                if balance <= total_principal_payment:
                    total_principal_payment = balance
                    actual_extra_paid = max(Decimal("0"), balance - scheduled_principal)
                    balance = Decimal("0")
                else:
                    balance -= total_principal_payment
                    actual_extra_paid = extra_monthly_principal

                # Append row elements with mathematically exact monetary rounding
                schedule.append(
                    {
                        "Month": str(current_month),
                        "Base Payment": str(base_payment.quantize(cents, rounding=decimal.ROUND_HALF_UP)),
                        "Extra Principal Paid": str(actual_extra_paid.quantize(cents, rounding=decimal.ROUND_HALF_UP)),
                        "Total Principal Paid": str(total_principal_payment.quantize(cents, rounding=decimal.ROUND_HALF_UP)),
                        "Interest Paid": str(interest_paid.quantize(cents, rounding=decimal.ROUND_HALF_UP)),
                        "Remaining Balance": str(balance.quantize(cents, rounding=decimal.ROUND_HALF_UP))
                    }
                )

            return schedule
        except Exception as e:
            if isinstance(self.__logger, LoggerAdapter): self.__logger.error(e, exc_info=True)
            raise e
