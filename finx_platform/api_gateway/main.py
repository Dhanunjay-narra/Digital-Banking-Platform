"""FinXCore Main FastAPI Application & API Gateway."""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from finx_platform.config.settings import settings
from finx_platform.common.database import Base, engine, SessionLocal
from finx_platform.api_gateway.middleware import CorrelationAndLoggingMiddleware
from finx_platform.security.password import hash_password
from finx_platform.security.rbac import Role

# Import all service routers
from services.identity.router import router as identity_router
from services.identity.models import User
from services.customer.router import router as customer_router
from services.customer.models import Customer
from services.kyc.router import router as kyc_router
from services.accounts.router import router as accounts_router
from services.accounts.models import BankAccount
from services.ledger.router import router as ledger_router
from services.ledger.service import ledger_service
from services.transactions.router import router as transactions_router
from services.transfers.router import router as transfers_router
from services.wallet.router import router as wallet_router
from services.wallet.models import DigitalWallet
from services.upi.router import router as upi_router
from services.payments.router import router as payments_router
from services.cards.router import router as cards_router
from services.merchants.router import router as merchants_router
from services.loans.router import router as loans_router
from services.credit.router import router as credit_router
from services.investments.router import router as investments_router
from services.insurance.router import router as insurance_router
from services.expenses.router import router as expenses_router
from services.bills.router import router as bills_router
from services.fraud.router import router as fraud_router
from services.compliance.router import router as compliance_router
from services.accounting.router import router as accounting_router
from services.pricing.router import router as pricing_router
from services.reconciliation.router import router as reconciliation_router
from services.disputes.router import router as disputes_router
from services.notifications.router import router as notifications_router
from services.recommendations.router import router as recommendations_router
from services.analytics.router import router as analytics_router
from services.reporting.router import router as reporting_router
from services.admin.router import router as admin_router


def seed_initial_platform_data():
    """Bootstraps default users, bank accounts, wallets, and ledger chart of accounts."""
    db = SessionLocal()
    try:
        ledger_service.initialize_chart_of_accounts(db)

        # Seed pre-configured demo users for 1-click role testing
        seed_users = [
            ("superadmin@finxcore.com", "+919900000001", "Super", "Admin", Role.SUPER_ADMIN.value),
            ("customer@finxcore.com", "+919900000002", "Dhanunjay", "Narra", Role.CUSTOMER.value),
            ("merchant@finxcore.com", "+919900000003", "NexGen", "Merchant", Role.MERCHANT_ADMIN.value),
            ("loan.officer@finxcore.com", "+919900000004", "Sarah", "Underwriter", Role.LOAN_OFFICER.value),
            ("compliance@finxcore.com", "+919900000005", "Michael", "Compliance", Role.COMPLIANCE_OFFICER.value),
            ("risk.analyst@finxcore.com", "+919900000006", "Vikram", "RiskAnalyst", Role.RISK_ANALYST.value),
        ]

        for email, phone, f_name, l_name, role_name in seed_users:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                user = User(
                    email=email,
                    phone_number=phone,
                    hashed_password=hash_password("FinX@2026"),
                    first_name=f_name,
                    last_name=l_name,
                    role=role_name,
                    is_active=True,
                    is_verified=True
                )
                db.add(user)
                db.flush()

                if role_name == Role.CUSTOMER.value:
                    cust = db.query(Customer).filter(Customer.user_id == user.id).first()
                    if not cust:
                        cust = Customer(
                            user_id=user.id,
                            customer_segment="PREMIUM",
                            customer_status="ACTIVE",
                            pan_number="ABCDE1234F",
                            annual_income=1800000.0,
                            risk_rating="LOW"
                        )
                        db.add(cust)
                        db.flush()

                        # Create Primary Savings Account
                        acc = BankAccount(
                            customer_id=cust.id,
                            account_number="100019283746",
                            account_type="SAVINGS",
                            currency="INR",
                            status="ACTIVE",
                            ledger_account_code="2000.192837",
                            available_balance=248500.00,
                            hold_balance=0.0,
                            minimum_balance=1000.0,
                            interest_rate_percent=4.0,
                            branch_ifsc="FINX0001001"
                        )
                        db.add(acc)

                        # Create Digital Wallet
                        wal = DigitalWallet(
                            customer_id=cust.id,
                            wallet_number="WAL9876543210",
                            balance=18500.00,
                            currency="INR",
                            status="ACTIVE",
                            daily_limit=50000.0,
                            monthly_limit=200000.0
                        )
                        db.add(wal)

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"[Seed Error] {e}")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables and seed default data
    Base.metadata.create_all(bind=engine)
    seed_initial_platform_data()
    yield
    # Shutdown logic if needed


app = FastAPI(
    title="FinXCore — Intelligent Digital Banking & Financial Services Platform",
    version="1.0.0",
    description="Comprehensive 70K+ LOC Fintech Super Platform with Double-Entry Ledger, UPI Rails, Payment Gateway, Cards, Loans, Credit Engine, Fraud Detection, and AML Compliance.",
    lifespan=lifespan
)

# Add Middlewares
app.add_middleware(CorrelationAndLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health & System Status Endpoints
@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "HEALTHY",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "ledger_engine": "BALANCED_DOUBLE_ENTRY"
    }


@app.get("/api/v1/ping", tags=["System"])
def ping():
    return {"ping": "pong", "platform": "FinXCore"}


# Register All 20+ Financial Domain Routers
app.include_router(identity_router, prefix=settings.API_V1_STR)
app.include_router(customer_router, prefix=settings.API_V1_STR)
app.include_router(kyc_router, prefix=settings.API_V1_STR)
app.include_router(accounts_router, prefix=settings.API_V1_STR)
app.include_router(ledger_router, prefix=settings.API_V1_STR)
app.include_router(transactions_router, prefix=settings.API_V1_STR)
app.include_router(transfers_router, prefix=settings.API_V1_STR)
app.include_router(wallet_router, prefix=settings.API_V1_STR)
app.include_router(upi_router, prefix=settings.API_V1_STR)
app.include_router(payments_router, prefix=settings.API_V1_STR)
app.include_router(cards_router, prefix=settings.API_V1_STR)
app.include_router(merchants_router, prefix=settings.API_V1_STR)
app.include_router(loans_router, prefix=settings.API_V1_STR)
app.include_router(credit_router, prefix=settings.API_V1_STR)
app.include_router(investments_router, prefix=settings.API_V1_STR)
app.include_router(insurance_router, prefix=settings.API_V1_STR)
app.include_router(expenses_router, prefix=settings.API_V1_STR)
app.include_router(bills_router, prefix=settings.API_V1_STR)
app.include_router(fraud_router, prefix=settings.API_V1_STR)
app.include_router(compliance_router, prefix=settings.API_V1_STR)
app.include_router(accounting_router, prefix=settings.API_V1_STR)
app.include_router(pricing_router, prefix=settings.API_V1_STR)
app.include_router(reconciliation_router, prefix=settings.API_V1_STR)
app.include_router(disputes_router, prefix=settings.API_V1_STR)
app.include_router(notifications_router, prefix=settings.API_V1_STR)
app.include_router(recommendations_router, prefix=settings.API_V1_STR)
app.include_router(analytics_router, prefix=settings.API_V1_STR)
app.include_router(reporting_router, prefix=settings.API_V1_STR)
app.include_router(admin_router, prefix=settings.API_V1_STR)

# Serve Web Frontend if directory exists
web_dir = os.path.join(os.path.dirname(__file__), "..", "..", "apps", "web")
if os.path.exists(web_dir):
    app.mount("/static", StaticFiles(directory=web_dir), name="static")

    @app.get("/", include_in_schema=False)
    def serve_index():
        return FileResponse(os.path.join(web_dir, "index.html"))
