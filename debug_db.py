
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

async def main():
    # Connect to MongoDB
    client = AsyncIOMotorClient("mongodb://receipt-db:27017")
    db = client.receipt_tracker
    
    print("\n--- All Transactions ---")
    cursor = db.transactions.find().sort("date", -1)
    async for txn in cursor:
        print(f"ID: {txn['_id']}")
        print(f"Merchant: {txn.get('merchant_name') or txn.get('description')}")
        print(f"Amount: {txn.get('amount')} {txn.get('currency')}")
        print(f"Date: {txn.get('date')} (Type: {type(txn.get('date'))})")
        print(f"Type: {txn.get('type')}")
        print(f"Category ID: {txn.get('category_id')}")
        print("-" * 30)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
