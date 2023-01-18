# coding: utf-8
from sqlalchemy import Column, DateTime, Float, String, Text, text, ForeignKey, SMALLINT
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata


class CompanyInfoGeneral(Base):
    __tablename__ = "company_info_general"
    __table_args__ = {"comment": "기업정보 기본"}

    ci_idx = Column(INTEGER(11), primary_key=True, autoincrement=True)
    ci_market_separation = Column(String(255), comment="시장구분")
    ci_progress = Column(String(255), comment="진행단계")
    ci_name = Column(String(255), nullable=False, comment="기업명")
    ci_code = Column(String(255), nullable=False, comment="기업코드")
    ci_logo = Column(String(255), comment="로고이미지")
    ci_logo_name = Column(String(255), comment="로고이미지 파일명")
    ci_keyword1 = Column(String(255), comment="키워드1(앱)")
    ci_keyword2 = Column(String(255), comment="키워드2(앱)")
    ci_keyword3 = Column(String(255), comment="키워드3(앱)")
    ci_keyword4 = Column(String(255), comment="키워드4(앱)")
    ci_list_type = Column(String(255), comment="상장유형")
    ci_review_c_date = Column(String(50), comment="심사청구일(Y/m/d)")
    ci_review_a_date = Column(String(50), comment="심사승인일(Y/m/d)")
    ci_face_value = Column(INTEGER(11), comment="액면가")
    ci_ceo = Column(String(50), comment="대표이사")
    ci_tel = Column(String(50), comment="대표전화")
    ci_homepage = Column(String(255), comment="홈페이지")
    ci_establishment_date = Column(String(50), comment="설립일(Y/m/d)")
    ci_company_separation = Column(String(255), comment="기업구분")
    ci_brn = Column(String(255), comment="사업자등록번호")
    ci_settlement_month = Column(INTEGER(11), comment="결산월")
    ci_worker_cnt = Column(INTEGER(11), comment="종업원수")
    ci_industries = Column(String(255), comment="업종")
    ci_important_product = Column(String(255), comment="주요제품")
    ci_stocks_separation = Column(String(255), comment="주권구분")
    ci_lead_manager = Column(String(255), comment="주간사")
    ci_address = Column(String(255), comment="본점소재지")
    ci_turnover = Column(Float(asdecimal=True), comment="청구시 매출액 (단위 : 억원)")
    ci_before_corporate_tax = Column(Float(asdecimal=True), comment="법인세 차감전 순이익 (단위 : 억원)")
    ci_net_profit = Column(Float(asdecimal=True), comment="청구시 순이익 (단위 : 억원)")
    ci_capital = Column(Float(asdecimal=True), comment="청구시 자기자본 (단위 : 억원)")
    ci_largest_shareholder = Column(String(255), comment="청구시 최대주주")
    ci_largest_shareholder_rate = Column(Float(asdecimal=True), comment="최대 주주 비율")
    ci_po_expected_price = Column(String(50), comment="[[ 삭제요청 ]] 공모(예정) 발행가 (범위 : '~'로 자르기)")
    ci_po_expected_stocks = Column(INTEGER(11), nullable=False, comment="공모(예정) 주식수")
    ci_po_expected_amount = Column(String(50), comment="[[ 삭제요청 ]] 공모(예정) 금액 (범위 : '~'로 자르기)")
    ci_listing_expected_stocks = Column(INTEGER(11), comment="상장(예정) 주식수")
    ci_before_po_capital = Column(Float(asdecimal=True), comment="공모전 자본금 (단위 : 억원)")
    ci_before_po_stocks = Column(BIGINT(20), comment="공모전 발행주식주")
    ci_after_po_capital = Column(Float(asdecimal=True), comment="공모후 자본금 (단위 : 억원)")
    ci_after_po_stocks = Column(BIGINT(20), comment="공모후 발행주식주")
    ci_most_subscription = Column(String(50), comment="[[ 삭제요청 ]] 최대주주 (앱용)")
    ci_comment = Column(Text, comment="1~2줄 코멘트")
    ci_big_ir_plan = Column(String(50), comment="[[ 삭제요청 ]] 대규모 IR 일정")
    ci_demand_forecast_date = Column(String(50), comment="수요예측일 (범위 : '~'로 자르기)")
    ci_public_subscription_date = Column(String(50), comment="공모청약일 (범위 : '~'로 자르기)")
    ci_refund_date = Column(String(50), comment="환불일")
    ci_payment_date = Column(String(50), comment="납입일")
    ci_listing_date = Column(String(50), comment="상장일")
    ci_appraised_price = Column(INTEGER(11), comment="주당평가액")
    ci_hope_po_price = Column(String(50), comment="희망 공모 가격 (범위 : '~'로 자르기)")
    ci_hope_po_amount = Column(String(50), comment="희망 공모 금액 (단위 : 억원, 범위 : '~'로 자르기)")
    ci_confirm_po_price = Column(INTEGER(11), comment="확정 공모 가격")
    ci_confirm_po_amount = Column(Float(asdecimal=True), comment="확정 공모 금액  (단위 : 억원)")
    ci_subscription_warrant_money_rate = Column(String(50), comment="청약증거금율")
    ci_subscription_competition_rate = Column(String(50), comment="청약경쟁률")
    ci_attractiveness = Column(String(255))
    ci_attractiveness_name = Column(String(255))
    ci_attractiveness_score = Column(INTEGER(11))
    ci_public_offering_stocks = Column(String(255), comment="공모주식수 ( 주,모집률 : '/'로 자르기)")
    ci_professional_investor_stock = Column(INTEGER(11), comment="전문투자자 주")
    ci_professional_investor_rate = Column(INTEGER(11), comment="전문투자자 모집율")
    ci_esa_stock = Column(INTEGER(11), comment="우리사주조합 주")
    ci_esa_rate = Column(INTEGER(11), comment="우리사주조합 모집율")
    ci_general_subscriber_stock = Column(INTEGER(11), comment="일반청약자 주")
    ci_general_subscriber_rate = Column(INTEGER(11), comment="일반청약자 모집율")
    ci_overseas_investor_stock = Column(INTEGER(11), comment="해외투자자 주")
    ci_overseas_investor_rate = Column(INTEGER(11), comment="해외투자자 모집율")
    ci_noted_items = Column(Text, comment="참고사항")
    ci_noted_items_check = Column(String(50), comment="참고사항 활성화 (N:비활성화 , Y:활성화)")
    ci_guidelines = Column(Text, comment="안내사항")
    ci_guidelines_check = Column(String(50), comment="안내사항 활성화 (N:비활성화 , Y:활성화)")
    ci_small_ir_plan = Column(String(255), comment="[[ 삭제요청 ]] 소규모 IR 일정")
    ci_receipt_way = Column(String(255), comment="[[ 삭제요청 ]] 접수방법")
    ci_receipt_place = Column(String(255), comment="[[ 삭제요청 ]] 접수장소")
    ci_ask_tel = Column(String(255), comment="[[ 삭제요청 ]] 문의전화")
    ci_organizer_homepage = Column(String(255), comment="[[ 삭제요청 ]] 주관사 홈페이지")
    ci_most_quantity = Column(BIGINT(20), comment="[[ 삭제요청 ]] 최고신청수량")
    ci_unit = Column(String(255), comment="[[ 삭제요청 ]] 단위 ( 주,원 : '/'로 자르기)")
    ci_competition_rate = Column(String(255), comment="단순 기관 경쟁률")
    ci_current_ratio = Column(INTEGER(11), comment="유동비율")
    ci_promise_content = Column(Text, comment="의무보유확약내용")
    ci_promise_rate = Column(Float(asdecimal=True), comment="의무보유확약비율")
    ci_like = Column(INTEGER(11), server_default=text("0"), comment="좋아요")
    ci_dislike = Column(INTEGER(11), server_default=text("0"), comment="싫어요")
    ci_vitalization1 = Column(String(50), comment="탭 활성화 [기업정보] (Y/N)")
    ci_vitalization2 = Column(String(50), comment="탭 활성화 [회사개요] (Y/N)")
    ci_vitalization3 = Column(String(50), comment="탭 활성화 [주주구성] (Y/N)")
    ci_vitalization4 = Column(String(50), comment="탭 활성화 [재무정보] (Y/N)")
    ci_vitalization5 = Column(String(50), comment="탭 활성화 [공모정보] (Y/N)")
    ci_vitalization6 = Column(String(50), comment="탭 활성화 [수요예측] (Y/N)")
    ci_demand_schedule = Column(String(50), comment="IPO공모관리 수요예측일정 추가 (Y/N)")
    ci_demand_schedule_state = Column(
        String(50), comment="IPO공모관리 수요예측일정 상태 (upload/delete/modify/real_delete)"
    )
    ci_demand_schedule_datetime = Column(DateTime, comment="IPO공모관리 수요예측일정 업데이트 날짜")
    ci_demand_result = Column(String(50), comment="IPO공모관리 수요예측결과 추가 (Y/N)")
    ci_demand_result_state = Column(
        String(50), comment="IPO공모관리 수요예측결과 상태 (upload/delete/modify/real_delete)"
    )
    ci_demand_result_datetime = Column(DateTime, comment="IPO공모관리 수요예측결과 업데이트 날짜")
    ci_public_schedule = Column(String(50), comment="IPO공모관리 공모청약일정 추가 (Y/N)")
    ci_public_schedule_state = Column(
        String(50), comment="IPO공모관리 공모청약일정 상태 (upload/delete/modify/real_delete)"
    )
    ci_public_schedule_datetime = Column(DateTime, comment="IPO공모관리 공모청약일정 업데이트 날짜")
    ci_datetime = Column(DateTime, nullable=False)

    shareholders = relationship("CompanyInfoShareholder", back_populates="company")
    predictions = relationship("CompanyInfoPrediction", back_populates="company")
    subscribers = relationship("CompanyInfoSubscriber", back_populates="company")
    financials = relationship("CompanyInfoFinancial", back_populates="company")
    app_calendars = relationship("AppCalendar", back_populates="company")


class CompanyInfoShareholder(Base):
    __tablename__ = "company_info_shareholder"
    __table_args__ = {"comment": "주주구성 보호예수/유통가능"}

    cis_idx = Column(INTEGER(11), primary_key=True, autoincrement=True)
    ci_idx = Column(
        INTEGER(11),
        ForeignKey("company_info_general.ci_idx", ondelete="CASCADE"),
        comment="기업 idx",
        nullable=True,
    )
    ci_category = Column(SMALLINT(), comment="구분 (1:보호예수매도금지 , 2:유통가능)")
    ci_category_name = Column(String(50), comment="구분 이름")
    ci_normal_stocks = Column(BIGINT(20), comment="보유주식 보통주")
    ci_first_stocks = Column(INTEGER(11), comment="보유주식 우선주")
    ci_share_rate = Column(Float(asdecimal=True), comment="공모후 보통주 지분율")
    ci_protection_date = Column(String(50), comment="보호예수기간")
    ci_datetime = Column(DateTime, server_default=text("'0000-00-00 00:00:00'"))

    company = relationship("CompanyInfoGeneral", back_populates="shareholders")


class CompanyInfoPrediction(Base):
    __tablename__ = "company_info_prediction"
    __table_args__ = {"comment": "수요예측결과"}

    cip_idx = Column(INTEGER(11), primary_key=True)
    ci_idx = Column(
        INTEGER(11),
        ForeignKey("company_info_general.ci_idx", ondelete="CASCADE"),
        comment="기업 idx",
        nullable=True,
    )
    ci_price = Column(String(255), comment="가격")
    ci_incidence = Column(INTEGER(11), comment="건수")
    ci_incidence_specific_gravity = Column(Float(asdecimal=True), comment="건수비중")
    ci_participation = Column(INTEGER(11), comment="참여수량")
    ci_participation_specific_gravity = Column(Float(asdecimal=True), comment="참여수량비중")
    ci_datetime = Column(DateTime, server_default=text("'0000-00-00 00:00:00'"))

    company = relationship("CompanyInfoGeneral", back_populates="predictions")


class CompanyInfoSubscriber(Base):
    __tablename__ = "company_info_subscriber"
    __table_args__ = {"comment": "공모정보 일반청약자 상세"}

    cis_idx = Column(INTEGER(11), primary_key=True)
    ci_idx = Column(
        INTEGER(11),
        ForeignKey("company_info_general.ci_idx", ondelete="CASCADE"),
        comment="기업 idx",
        nullable=True,
    )
    ci_stock_firm = Column(String(50), server_default=text("'0'"), comment="증권사")
    ci_assign_quantity = Column(INTEGER(11), server_default=text("0"), comment="배정수량")
    ci_limit = Column(INTEGER(11), server_default=text("0"), comment="청약한도")
    ci_note = Column(String(50), comment="비고")
    ci_datetime = Column(DateTime, server_default=text("'0000-00-00 00:00:00'"))

    company = relationship("CompanyInfoGeneral", back_populates="subscribers")


class CompanyInfoFinancial(Base):
    __tablename__ = "company_info_financial"
    __table_args__ = {"comment": "재무정보 (단위 : 억원 , 소수점 첫째자리(천만) 까지 표기)"}

    cif_idx = Column(INTEGER(11), primary_key=True)
    ci_idx = Column(
        INTEGER(11),
        ForeignKey("company_info_general.ci_idx", ondelete="CASCADE"),
        comment="기업 idx",
        nullable=True,
    )
    cif_order = Column(INTEGER(11), server_default=text("0"), comment="순서")
    ci_category1 = Column(String(50), comment="구분1")
    ci_category2 = Column(String(50), comment="구분2")
    ci_current_asset = Column(Float(asdecimal=True), comment="유동자산")
    ci_non_current_asset = Column(Float(asdecimal=True), comment="비유동자산")
    ci_current_liability = Column(Float(asdecimal=True), comment="유동부채")
    ci_non_current_liability = Column(Float(asdecimal=True), comment="비유동부채")
    ci_capital = Column(Float(asdecimal=True), comment="자본금")
    ci_capital_surplus = Column(Float(asdecimal=True), comment="자본잉여금")
    ci_earned_surplus = Column(Float(asdecimal=True), comment="이익잉여금")
    ci_other_capital_items = Column(Float(asdecimal=True), comment="기타 자본 항목")
    ci_turnover = Column(Float(asdecimal=True), comment="매출액")
    ci_business_profits = Column(Float(asdecimal=True), comment="영업이익")
    ci_net_income = Column(Float(asdecimal=True), comment="당기순이익")
    ci_eps = Column(Float(asdecimal=True), comment="기본주당이익")
    ci_datetime = Column(DateTime, server_default=text("'0000-00-00 00:00:00'"))

    company = relationship("CompanyInfoGeneral", back_populates="financials")


class AppCalendar(Base):
    __tablename__ = "app_calendar"
    __table_args__ = {"comment": "앱 캘린더 관리"}

    ac_idx = Column(INTEGER(11), primary_key=True)
    ci_idx = Column(
        INTEGER(11),
        ForeignKey("company_info_general.ci_idx", ondelete="CASCADE"),
        comment="기업 idx",
        nullable=True,
    )
    ac_sdate = Column(String(50), comment="일정 시작일자 (yyyy-mm-dd)")
    ac_edate = Column(String(50), comment="일정 종료일자 (yyyy-mm-dd)")
    ac_category = Column(INTEGER(11), comment="1:청약일, 2:상장일, 3:환불일, 4:수요예측")
    ac_category_name = Column(String(50), comment="구분명")
    ac_company_name = Column(String(50), comment="회사명")
    ac_vitalize = Column(String(50), comment="Y:활성화, N:비활성화")
    ac_datetime = Column(DateTime)

    company = relationship("CompanyInfoGeneral", back_populates="app_calendars")
