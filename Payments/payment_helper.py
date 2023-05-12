from Order.models import Order
import requests
from django.conf import settings
class Payment:
    def __init__(self) -> None:
        self.base_url = "https://api.paystack.co/transaction/"
        self.secret_key = settings.PAYSTACK_SECRET_KEY

    def initiate(self, amount:str, email:str, tracking_id:str):
        self.amount = amount
        self.email = email
        headers = {
            "Authorization" : f"Bearer {self.secret_key}"
            }
        data = {
            "email" : self.email,
            "amount" : self.amount,
            "reference" : tracking_id
        }
        url = self.base_url + "initialize"
        resp = requests.post(url,data=data,headers=headers)
        return resp.json()
    
    def verify(self, ref_id:str) -> bool:
        url = self.base_url + f"verify/{ref_id}"
        headers = {
            "Authorization" : f"Bearer {self.secret_key}"
        }
        resp = requests.get(url,headers=headers)
        data = resp.json()['data']
        if data['status'] == "success":
            return True
        return False