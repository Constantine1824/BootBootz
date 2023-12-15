from Order.models import Order
import requests
from django.conf import settings

BASE_URL = "https://api.paystack.co/transaction/"
SECRET_KEY = settings.PAYSTACK_SECRET_KEY

def initiate(amount:str, email:str, tracking_id:str):
    """
    Initiates a payment transaction by sending a request to the API.

    Parameters:
        - amount (str): The amount of the payment.
        - email (str): The email address of the customer.
        - tracking_id (str): The tracking ID for the payment transaction.

    Returns:
        - dict: The JSON response from the API containing the details of the payment transaction.
    """
    headers = {
        "Authorization" : f"Bearer {SECRET_KEY}"
        }
    data = {
        "email" : self.email,
        "amount" : self.amount,
        "reference" : tracking_id
        }
    url = self.base_url + "initialize"
    resp = requests.post(url,data=data,headers=headers)
    return resp.json()
    
def verify(ref_id:str) -> bool:
    """
    Verify the reference ID by sending a GET request to the API.
    
    Parameters:
        ref_id (str): The reference ID to be verified.
        
    Returns:
        bool: True if the verification is successful, False otherwise.
    """
    url = self.base_url + f"verify/{ref_id}"
    headers = {
        "Authorization" : f"Bearer {self.secret_key}"
    }
    resp = requests.get(url,headers=headers)
    data = resp.json()['data']
    if data['status'] == "success":
        return True
    return False