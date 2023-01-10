from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from utilities.validations import Validations
from utilities import converters


class State(Enum):
    MODIFY = "modify"
    DELETE = "delete"
    REAL_DELETE = "real_delete"
    UPLOAD = "upload"


@dataclass
class GeneralBase(Validations):
    ci_market_separation: str = ""
    ci_progress: str = ""
    ci_name: str = ""
    ci_code: str = ci_name
    ci_logo: str = ""
    ci_logo_name: str = ""
    ci_keyword1: str = ""
    ci_keyword2: str = ""
    ci_keyword3: str = ""
    ci_keyword4: str = ""
    ci_list_type: str = ci_market_separation
    ci_review_c_date: str = ""
    ci_review_a_date: str = ""
    ci_face_value: int = 0
    ci_ceo: str = ""
    ci_tel: str = ""
    ci_homepage: str = ""
    ci_establishment_date: str = ""
    ci_company_separation: str = ""
    ci_brn: str = ""
    ci_settlement_month: int = 0  # 결산월
    ci_worker_cnt: int = 0
    ci_industries: str = ""
    ci_important_product: str = ""
    ci_stocks_separation: str = ""
    ci_lead_manager: str = ""
    ci_address: str = ""
    ci_turnover: float = 0.0
    ci_before_corporate_tax: float = 0.0
    ci_net_profit: float = 0.0
    ci_capital: float = 0.0
    ci_largest_shareholder: str = ""
    ci_largest_shareholder_rate: float = 0.0
    ci_po_expected_price: str = ""
    ci_po_expected_stocks: int = 0
    ci_po_expected_amount: str = ""
    ci_listing_expected_stocks: str = ""
    ci_before_po_capital: float = 0.0
    ci_before_po_stocks: int = 0.0
    ci_after_po_capital: float = 0.0
    ci_after_po_stocks: str = ""
    ci_most_subscription: str = ""
    ci_comment: str = ""
    ci_big_ir_plan: str = ""
    ci_demand_forecast_date: str = ""
    ci_public_subscription_date: str = ""
    ci_refund_date: str = ""
    ci_payment_date: str = ""
    ci_listing_date: str = ""
    ci_appraised_price: int = 0
    ci_hope_po_price: str = ""
    ci_hope_po_amount: str = ""
    ci_confirm_po_price: int = 0
    ci_confirm_po_amount: float = 0.0
    ci_subscription_warrant_money_rate: str = ""
    ci_subscription_competition_rate: str = ""
    ci_attractiveness: str = ""
    ci_attractiveness_name: str = ""
    ci_attractiveness_score: int = 0
    ci_public_offering_stocks: str = ""
    ci_professional_investor_stock: int = 0
    ci_professional_investor_rate: int = 0
    ci_esa_stock: int = 0
    ci_esa_rate: int = 0
    ci_general_subscriber_stock: int = 0
    ci_general_subscriber_rate: int = 0
    ci_overseas_investor_stock: int = 0
    ci_overseas_investor_rate: int = 0
    ci_noted_items: str = ""
    ci_noted_items_check: str = ""
    ci_guidelines: str = ""
    ci_guidelines_check: str = ""
    ci_small_ir_plan: str = ""
    ci_receipt_way: str = ""
    ci_receipt_place: str = ""
    ci_ask_tel: str = ""
    ci_organizer_homepage: str = ""
    ci_most_quantity: int = 0
    ci_unit: str = ""
    ci_competition_rate: str = ""
    ci_current_ratio: int = 0
    ci_promise_content: str = ""
    ci_promise_rate: float = 0.0
    ci_like: int = 0
    ci_dislike: int = 0
    ci_vitalization1: str = "Y"
    ci_vitalization2: str = "Y"
    ci_vitalization3: str = "Y"
    ci_vitalization4: str = "Y"
    ci_vitalization5: str = "Y"
    ci_vitalization6: str = "Y"
    ci_demand_schedule: str = "Y"
    ci_demand_schedule_state: str = State.UPLOAD.value
    ci_demand_schedule_datetime: datetime = datetime.now()
    ci_demand_result: str = "Y"
    ci_demand_result_state: str = State.UPLOAD.value
    ci_demand_result_datetime: datetime = datetime.now()
    ci_public_schedule: str = "Y"
    ci_public_schedule_state: str = State.UPLOAD.value
    ci_public_schedule_datetime: datetime = datetime.now()
    ci_datetime: datetime = datetime.now()


class GeneralCreateSchema(GeneralBase):
    # def validate_ci_name(self, value, **_):
    #     name, _ = converters.represent_ci_name_n_code(value)
    #     return name

    # def validate_ci_code(self, value, **_):
    #     _, code = converters.represent_ci_name_n_code(value)
    #     return code

    def validate_ci_market_separation(self, value, **_):
        return converters.extensions_to_string(value)

    def validate_ci_list_type(self, value, **_):
        return converters.ci_list_type(value)

    def validate_ci_review_c_date(self, value, **_):
        return converters.dot_dash_to_slash(value)

    def validate_ci_review_a_date(self, value, **_):
        return converters.dot_dash_to_slash(value)

    def validate_ci_establishment_date(self, value, **_):
        return converters.dot_dash_to_slash(value)

    def validate_ci_settlement_month(self, value, **_):
        return converters.month_to_int(value)

    def validate_ci_worker_cnt(self, value, **_):
        return converters.worker_to_int(value)

    def validate_ci_turnover(self, value, **_):
        return converters.one_millon_won_to_float(value)

    def validate_ci_before_corporate_tax(self, value, **_):
        return converters.one_millon_won_to_float(value)

    def validate_ci_net_profit(self, value, **_):
        return converters.one_millon_won_to_float(value)

    def validate_ci_capital(self, value, **_):
        return converters.one_millon_won_to_float(value)

    def validate_ci_largest_shareholder_rate(self, value, **_):
        return converters.string_rate_to_percentage(value)

    def validate_ci_promise_rate(self, value, **_):
        return converters.string_rate_to_float(value)

    def validate_ci_po_expected_amount(self, value, **_):
        return converters.ci_po_expected_amount(value)

    def validate_ci_listing_expected_stocks(self, value, **_):
        return converters.only_digits(value)

    def validate_ci_before_po_capital(self, value, **_):
        return converters.string_capital_to_float(value)

    def validate_ci_before_po_stocks(self, value, **_):
        return converters.string_stocks_to_int(value)

    def validate_ci_after_po_capital(self, value, **_):
        return converters.string_capital_to_float(value)

    def validate_ci_after_po_stocks(self, value, **_):
        return converters.string_stocks_to_int(value)

    def validate_ci_lead_manager(self, value, **_):
        return converters.none_to_empty_string(value)

    def validate_ci_homepage(self, value, **_):
        return converters.none_to_empty_string(value)


if __name__ == "__main__":
    g = GeneralCreateSchema(ci_name="hello")
    from pprint import pprint as pp

    pp(g)
