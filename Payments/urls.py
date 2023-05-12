from django.urls import path
from .views import InitializePaymentApiView,VerifyPayment

urlpatterns = [path(
    "/initialize",
    InitializePaymentApiView.as_view(),
    name="initialize"
),
    path(
    '/verify/<str:ref_id>',
    VerifyPayment.as_view(),
    name='verify-payment'
    )
]
