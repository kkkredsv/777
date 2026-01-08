"""
Robokassa Payment Integration

This module provides integration with Robokassa payment system.
Robokassa is a Russian payment aggregator that supports various payment methods.
"""

import hashlib
import requests
from typing import Optional, Dict, Any
from decimal import Decimal
from urllib.parse import urlencode


class RobokassaConfig:
    """Configuration for Robokassa integration"""
    
    def __init__(
        self,
        merchant_login: str,
        password1: str,
        password2: str,
        test_mode: bool = False
    ):
        """
        Initialize Robokassa configuration
        
        Args:
            merchant_login: Robokassa merchant login
            password1: First password (for payment signature)
            password2: Second password (for result notification)
            test_mode: Enable test mode (default: False)
        """
        self.merchant_login = merchant_login
        self.password1 = password1
        self.password2 = password2
        self.test_mode = test_mode
        
        self.base_url = "https://auth.robokassa.ru" if not test_mode else "https://test.robokassa.ru"
        self.api_url = "https://api.robokassa.ru"


class RobokassaPayment:
    """Robokassa payment processor"""
    
    def __init__(self, config: RobokassaConfig):
        """
        Initialize payment processor
        
        Args:
            config: RobokassaConfig instance
        """
        self.config = config
    
    def _generate_signature(
        self,
        merchant_login: str,
        sum_amount: Decimal,
        invoice_id: str,
        password: str,
        extra_params: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Generate MD5 signature for Robokassa request
        
        Args:
            merchant_login: Merchant login
            sum_amount: Payment amount
            invoice_id: Invoice ID
            password: Password for signature
            extra_params: Extra parameters to include in signature
            
        Returns:
            MD5 hash signature
        """
        # Format amount with 2 decimal places
        amount_str = f"{sum_amount:.2f}"
        
        # Build signature string: MerchantLogin:Sum:InvoiceID:Password1[:extra_params]
        signature_parts = [merchant_login, amount_str, invoice_id, password]
        
        # Add extra parameters if provided (in alphabetical order)
        if extra_params:
            sorted_params = sorted(extra_params.items())
            for key, value in sorted_params:
                signature_parts.append(f"{key}={value}")
        
        signature_string = ":".join(signature_parts)
        signature = hashlib.md5(signature_string.encode()).hexdigest()
        
        return signature
    
    def get_payment_url(
        self,
        invoice_id: str,
        amount: Decimal,
        description: str,
        email: Optional[str] = None,
        extra_params: Optional[Dict[str, str]] = None,
        return_url: Optional[str] = None
    ) -> str:
        """
        Generate Robokassa payment URL
        
        Args:
            invoice_id: Unique invoice ID
            amount: Payment amount in RUB
            description: Payment description
            email: Customer email
            extra_params: Additional parameters to pass
            return_url: URL to redirect after payment
            
        Returns:
            Full payment URL
        """
        # Generate signature
        signature = self._generate_signature(
            self.config.merchant_login,
            amount,
            invoice_id,
            self.config.password1,
            extra_params
        )
        
        # Build payment parameters
        params = {
            'MerchantLogin': self.config.merchant_login,
            'Sum': f"{amount:.2f}",
            'InvoiceID': invoice_id,
            'Description': description,
            'SignatureValue': signature,
            'IsTest': '1' if self.config.test_mode else '0',
        }
        
        if email:
            params['Email'] = email
        
        if return_url:
            params['ReturnURL'] = return_url
        
        # Add extra parameters
        if extra_params:
            params.update(extra_params)
        
        # Build URL
        payment_url = f"{self.config.base_url}/Merchant/Index?" + urlencode(params)
        
        return payment_url
    
    def verify_result_signature(
        self,
        sum_amount: Decimal,
        invoice_id: str,
        signature: str,
        extra_params: Optional[Dict[str, str]] = None
    ) -> bool:
        """
        Verify signature from Robokassa result notification
        
        Args:
            sum_amount: Payment amount
            invoice_id: Invoice ID
            signature: Signature from notification
            extra_params: Extra parameters from notification
            
        Returns:
            True if signature is valid, False otherwise
        """
        expected_signature = self._generate_signature(
            self.config.merchant_login,
            sum_amount,
            invoice_id,
            self.config.password2,
            extra_params
        )
        
        return signature.lower() == expected_signature.lower()
    
    def create_order(
        self,
        invoice_id: str,
        amount: Decimal,
        description: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        extra_params: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Create payment order via Robokassa API
        
        Args:
            invoice_id: Unique invoice ID
            amount: Payment amount in RUB
            description: Payment description
            email: Customer email
            phone: Customer phone
            extra_params: Additional parameters
            
        Returns:
            Order creation response
        """
        # This is a placeholder for API-based order creation
        # Actual implementation would depend on Robokassa API version
        
        payload = {
            'MerchantLogin': self.config.merchant_login,
            'Sum': float(amount),
            'InvoiceID': invoice_id,
            'Description': description,
        }
        
        if email:
            payload['Email'] = email
        if phone:
            payload['Phone'] = phone
        if extra_params:
            payload.update(extra_params)
        
        try:
            # Note: This would require proper API authentication
            # Implementation depends on current Robokassa API
            response = requests.post(
                f"{self.config.api_url}/CreateInvoice",
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def check_payment_status(self, invoice_id: str) -> Dict[str, Any]:
        """
        Check payment status for an invoice
        
        Args:
            invoice_id: Invoice ID to check
            
        Returns:
            Payment status information
        """
        try:
            response = requests.get(
                f"{self.config.api_url}/GetInvoiceInfo",
                params={'InvoiceID': invoice_id},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {
                'success': False,
                'error': str(e)
            }


class RobokassaNotification:
    """Handler for Robokassa payment notifications"""
    
    def __init__(self, processor: RobokassaPayment):
        """
        Initialize notification handler
        
        Args:
            processor: RobokassaPayment instance
        """
        self.processor = processor
    
    def process_result_notification(
        self,
        sum_amount: Decimal,
        invoice_id: str,
        signature: str,
        extra_params: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Process result notification from Robokassa
        
        Args:
            sum_amount: Payment amount
            invoice_id: Invoice ID
            signature: Notification signature
            extra_params: Extra parameters from notification
            
        Returns:
            Processing result with success flag
        """
        # Verify signature
        if not self.processor.verify_result_signature(
            sum_amount, invoice_id, signature, extra_params
        ):
            return {
                'success': False,
                'error': 'Invalid signature',
                'invoice_id': invoice_id
            }
        
        return {
            'success': True,
            'invoice_id': invoice_id,
            'amount': float(sum_amount),
            'extra_params': extra_params or {}
        }
    
    def get_notification_response(self, invoice_id: str) -> str:
        """
        Get proper notification response for Robokassa
        
        Args:
            invoice_id: Invoice ID
            
        Returns:
            Response string for Robokassa
        """
        return f"OK{invoice_id}"


# Example usage
if __name__ == "__main__":
    # Configure Robokassa
    config = RobokassaConfig(
        merchant_login="YOUR_MERCHANT_LOGIN",
        password1="YOUR_PASSWORD1",
        password2="YOUR_PASSWORD2",
        test_mode=True
    )
    
    # Create processor
    processor = RobokassaPayment(config)
    
    # Generate payment URL
    payment_url = processor.get_payment_url(
        invoice_id="12345",
        amount=Decimal("100.00"),
        description="Test Payment",
        email="customer@example.com",
        return_url="https://example.com/return"
    )
    
    print(f"Payment URL: {payment_url}")
