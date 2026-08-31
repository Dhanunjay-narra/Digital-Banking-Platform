"""Investment & Wealth Management Business Logic."""

from sqlalchemy.orm import Session
from finx_platform.common.exceptions import FinTechException, InsufficientFundsException
from services.investments.models import PortfolioHolding, SIPPlan, AssetClass
from services.investments.schemas import InvestmentOrderRequest, SIPCreateRequest, PortfolioSummaryResponse, HoldingResponse
from services.accounts.models import BankAccount


class InvestmentService:
    @staticmethod
    def initialize_sample_portfolio(db: Session, customer_id: str) -> None:
        existing = db.query(PortfolioHolding).filter(PortfolioHolding.customer_id == customer_id).first()
        if not existing:
            samples = [
                ("FINX-NIFTY50", "FinX Bluechip Equity Index Fund", AssetClass.MUTUAL_FUND.value, 250.0, 400.0, 480.0),
                ("FINX-TECH-ETF", "FinX Global Tech Leaders ETF", AssetClass.ETF.value, 120.0, 1000.0, 1150.0),
                ("GOV-BOND-2035", "Government Sovereign 7.26% Bond", AssetClass.BOND.value, 50.0, 1000.0, 1040.0),
                ("GOLD-999", "FinX Digital 24K Gold Vault", AssetClass.GOLD.value, 15.0, 6200.0, 7100.0)
            ]
            for sym, name, a_class, units, buy_p, curr_p in samples:
                invested = round(units * buy_p, 2)
                curr_val = round(units * curr_p, 2)
                pnl = round(curr_val - invested, 2)
                h = PortfolioHolding(
                    customer_id=customer_id,
                    asset_symbol=sym,
                    asset_name=name,
                    asset_class=a_class,
                    units=units,
                    average_buy_price=buy_p,
                    current_market_price=curr_p,
                    invested_amount=invested,
                    current_value=curr_val,
                    unrealized_pnl=pnl
                )
                db.add(h)
            db.commit()

    @staticmethod
    def buy_asset(db: Session, customer_id: str, req: InvestmentOrderRequest) -> PortfolioHolding:
        # Deduct from bank account
        acc = db.query(BankAccount).filter(BankAccount.account_number == req.source_account_number).first()
        if acc:
            if acc.available_balance < req.amount:
                raise InsufficientFundsException("Insufficient funds in bank account for investment purchase.")
            acc.available_balance -= req.amount

        holding = db.query(PortfolioHolding).filter(
            PortfolioHolding.customer_id == customer_id,
            PortfolioHolding.asset_symbol == req.asset_symbol
        ).first()

        unit_price = 500.0  # Simulated price
        bought_units = req.amount / unit_price

        if not holding:
            holding = PortfolioHolding(
                customer_id=customer_id,
                asset_symbol=req.asset_symbol,
                asset_name=req.asset_name,
                asset_class=req.asset_class,
                units=bought_units,
                average_buy_price=unit_price,
                current_market_price=unit_price * 1.05,
                invested_amount=req.amount,
                current_value=req.amount * 1.05,
                unrealized_pnl=req.amount * 0.05
            )
            db.add(holding)
        else:
            total_invested = holding.invested_amount + req.amount
            total_units = holding.units + bought_units
            holding.average_buy_price = total_invested / total_units
            holding.units = total_units
            holding.invested_amount = total_invested
            holding.current_value = total_units * holding.current_market_price
            holding.unrealized_pnl = holding.current_value - holding.invested_amount

        db.commit()
        db.refresh(holding)
        return holding

    @staticmethod
    def get_portfolio_summary(db: Session, customer_id: str) -> PortfolioSummaryResponse:
        InvestmentService.initialize_sample_portfolio(db, customer_id)
        holdings = db.query(PortfolioHolding).filter(PortfolioHolding.customer_id == customer_id).all()

        tot_inv = sum(h.invested_amount for h in holdings)
        tot_val = sum(h.current_value for h in holdings)
        tot_pnl = round(tot_val - tot_inv, 2)
        pnl_pct = round((tot_pnl / tot_inv * 100), 2) if tot_inv > 0 else 0.0

        return PortfolioSummaryResponse(
            total_invested=round(tot_inv, 2),
            current_value=round(tot_val, 2),
            total_pnl=tot_pnl,
            total_pnl_percentage=pnl_pct,
            holdings=[HoldingResponse.model_validate(h) for h in holdings]
        )


investment_service = InvestmentService()
