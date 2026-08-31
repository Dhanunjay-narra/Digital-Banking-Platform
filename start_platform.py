"""FinXCore Digital Banking Super Platform Launcher."""

import sys
import os
import uvicorn

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    print("=" * 70)
    print("FinXCore -- Intelligent Digital Banking & Financial Super Platform")
    print("Author: Dhanunjay Narra")
    print("=" * 70)
    print("[+] Starting High-Performance API Gateway on http://localhost:8000")
    print("[+] Interactive Banking Portals: http://localhost:8000")
    print("[+] Interactive OpenAPI Swagger: http://localhost:8000/docs")
    print("[+] Pre-seeded 1-Click Role Logins: Customer, Merchant, Admin, Loan Officer")
    print("=" * 70)
    uvicorn.run("finx_platform.api_gateway.main:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()
