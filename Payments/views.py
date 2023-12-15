from rest_framework.response import Response
from rest_framework.views import APIView
from Core.permissions import IsVerified
from rest_framework.permissions import IsAuthenticated
from Order.models import Order
from rest_framework.exceptions import ParseError
from .payment_helper import initiate, verify
from rest_framework import status

class InitializePaymentApiView(APIView):
    permission_classes = [IsAuthenticated,IsVerified]
    def post(self,request):
        order_id = request.data['tracking_id']
        user = request.user
        email = user.email
        try:
            order_obj = Order.objects.get(tracking_id=order_id)
            if order_obj.status!= 'PEN':
                raise ParseError('Wrong order')
            try:
                price = order_obj.total_price
                resp = initiate(email=email,amount=price,tracking_id=order_id)
                return Response(resp)
            except Exception as e:
                return Response(e)
        except Order.DoesNotExist:
            raise ParseError("Order does not exist")


class VerifyPayment(APIView):
    permission_classes = [IsAuthenticated,IsVerified]
    def get(self,request,ref_id):
        payment = Payment()
        resp = verify(ref_id)
        if resp:
            order = Order.objects.get(tracking_id=ref_id)
            order.status = 'APR'
            order.save()
            return Response({
                'detail' : 'Transaction Successful'
            }, status=status.HTTP_200_OK)
# Create your views here.
