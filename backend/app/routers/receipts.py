"""
Receipt scanning router
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from datetime import datetime
from bson import ObjectId
import os
import aiofiles
from pathlib import Path

from ..schemas import ReceiptScanResponse
from ..services.auth import get_current_user_id
from ..services.database import get_collection
from ..services.ai_scanner import get_scanner

router = APIRouter()

# Upload directory
UPLOAD_DIR = Path("/app/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/scan", response_model=ReceiptScanResponse)
async def scan_receipt(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id)
):
    """
    Upload and scan a receipt image
    
    Uses Gemini 2.0 Flash to extract transaction data
    """
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Generate unique filename
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    file_ext = Path(file.filename).suffix
    filename = f"{user_id}_{timestamp}{file_ext}"
    file_path = UPLOAD_DIR / filename
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    
    # Create receipt record
    receipts_collection = await get_collection("receipts")
    receipt_doc = {
        "user_id": user_id,
        "filename": filename,
        "file_path": str(file_path),
        "scan_status": "processing",
        "scanned_at": datetime.utcnow()
    }
    
    result = await receipts_collection.insert_one(receipt_doc)
    receipt_id = str(result.inserted_id)
    
    # Scan with AI
    try:
        scanner = get_scanner()
        
        # Load user's API key from settings
        settings_collection = await get_collection("settings")
        user_settings = await settings_collection.find_one({"user_id": user_id})
        
        if user_settings and user_settings.get("gemini_api_key"):
            scanner.set_api_key(user_settings["gemini_api_key"])
        elif not scanner.api_key:
            # No API key in settings and no default key
            await receipts_collection.update_one(
                {"_id": ObjectId(receipt_id)},
                {"$set": {
                    "scan_status": "failed",
                    "error_message": "Gemini API key not configured. Please set it in settings."
                }}
            )
            return ReceiptScanResponse(
                id=receipt_id,
                filename=filename,
                scan_status="failed",
                error_message="Gemini API key not configured. Please set it in settings.",
                scanned_at=receipt_doc["scanned_at"]
            )
        
        extracted_data = await scanner.scan_receipt(str(file_path))
        
        # Check for errors
        if "error" in extracted_data:
            await receipts_collection.update_one(
                {"_id": ObjectId(receipt_id)},
                {"$set": {
                    "scan_status": "failed",
                    "error_message": extracted_data["error"],
                    "extracted_data": extracted_data
                }}
            )
            
            return ReceiptScanResponse(
                id=receipt_id,
                filename=filename,
                scan_status="failed",
                error_message=extracted_data["error"],
                scanned_at=receipt_doc["scanned_at"]
            )
        
        # Update receipt with extracted data
        confidence = extracted_data.get("confidence", 0.5)
        await receipts_collection.update_one(
            {"_id": ObjectId(receipt_id)},
            {"$set": {
                "scan_status": "completed",
                "ai_confidence": confidence,
                "extracted_data": extracted_data
            }}
        )
        
        return ReceiptScanResponse(
            id=receipt_id,
            filename=filename,
            scan_status="completed",
            ai_confidence=confidence,
            extracted_data=extracted_data,
            scanned_at=receipt_doc["scanned_at"]
        )
        
    except Exception as e:
        # Update status to failed
        error_msg = str(e)
        await receipts_collection.update_one(
            {"_id": ObjectId(receipt_id)},
            {"$set": {
                "scan_status": "failed",
                "error_message": error_msg
            }}
        )
        
        # Return failed status instead of raising 500 error
        return ReceiptScanResponse(
            id=receipt_id,
            filename=filename,
            scan_status="failed",
            error_message=f"Failed to scan receipt: {error_msg}",
            scanned_at=receipt_doc["scanned_at"]
        )


@router.get("/{receipt_id}", response_model=ReceiptScanResponse)
async def get_receipt(
    receipt_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Get receipt scan details"""
    receipts_collection = await get_collection("receipts")
    
    receipt = await receipts_collection.find_one({
        "_id": ObjectId(receipt_id),
        "user_id": user_id
    })
    
    if not receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receipt not found"
        )
    
    return ReceiptScanResponse(
        id=str(receipt["_id"]),
        filename=receipt["filename"],
        scan_status=receipt["scan_status"],
        ai_confidence=receipt.get("ai_confidence"),
        extracted_data=receipt.get("extracted_data"),
        transaction_id=receipt.get("transaction_id"),
        error_message=receipt.get("error_message"),
        scanned_at=receipt["scanned_at"]
    )


@router.get("/")
async def list_receipts(
    user_id: str = Depends(get_current_user_id),
    skip: int = 0,
    limit: int = 50
):
    """List all receipt scans for user"""
    receipts_collection = await get_collection("receipts")
    
    cursor = receipts_collection.find({"user_id": user_id}) \
        .sort("scanned_at", -1) \
        .skip(skip) \
        .limit(limit)
    
    receipts = []
    async for receipt in cursor:
        receipts.append({
            "id": str(receipt["_id"]),
            "filename": receipt["filename"],
            "scan_status": receipt["scan_status"],
            "ai_confidence": receipt.get("ai_confidence"),
            "scanned_at": receipt["scanned_at"].isoformat()
        })
    
    return receipts
