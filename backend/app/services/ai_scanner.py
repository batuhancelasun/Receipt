"""
Gemini 2.0 Flash AI service for receipt scanning
"""
import google.generativeai as genai
from PIL import Image
import json
from typing import Optional, Dict, Any
import os
import logging

logger = logging.getLogger(__name__)


class GeminiReceiptScanner:
    """
    AI-powered receipt scanner using Gemini 2.0 Flash
    
    Extracts structured data from receipt images:
    - Merchant name
    - Transaction date
    - Total amount
    - Currency
    - Individual items with prices
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini with API key"""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
        else:
            self.model = None
    
    def set_api_key(self, api_key: str):
        """Update API key dynamically"""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
    
    async def scan_receipt(self, image_path: str) -> Dict[str, Any]:
        """
        Scan receipt image and extract structured data
        
        Args:
            image_path: Path to the receipt image
            
        Returns:
            Dictionary with extracted data and confidence score
        """
        if not self.model:
            raise ValueError("Gemini API key not configured. Please set it in settings.")
        
        try:
            # Load image
            img = Image.open(image_path)
            
            # Prompt for structured extraction
            prompt = """
Analyze this receipt image and extract the following information in JSON format:

{
  "merchant_name": "Store or restaurant name",
  "date": "YYYY-MM-DD format",
  "total_amount": 0.00,
  "currency": "€ or $ or other symbol",
  "items": [
    {
      "name": "Item name",
      "quantity": 1.0,
      "unit_price": 0.00,
      "total_price": 0.00
    }
  ],
  "tax_amount": 0.00,
  "payment_method": "cash/card/other",
  "confidence": 0.95
}

Important:
- Return ONLY valid JSON, no markdown or extra text
- If you cannot read something clearly, use null
- Set confidence between 0.0 and 1.0 based on image quality
- Extract ALL items from the receipt
- Preserve original currency symbol
"""
            
            # Generate response
            response = self.model.generate_content([prompt, img])
            
            # Parse JSON response
            text = response.text.strip()
            
            # Remove markdown code blocks if present
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            # Parse JSON
            extracted_data = json.loads(text)
            
            logger.info(f"Successfully scanned receipt: {extracted_data.get('merchant_name')}")
            return extracted_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response as JSON: {e}")
            logger.error(f"Response text: {response.text}")
            return {
                "error": "Failed to parse AI response",
                "raw_response": response.text,
                "confidence": 0.0
            }
        except Exception as e:
            logger.error(f"Error scanning receipt: {e}")
            return {
                "error": str(e),
                "confidence": 0.0
            }


# Global scanner instance (will be updated when user sets API key)
scanner = GeminiReceiptScanner()


def get_scanner() -> GeminiReceiptScanner:
    """Get the global scanner instance"""
    return scanner
