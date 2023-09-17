import django_tables2 as tables
from .models import (
    SSLAdmissionPaymentVerfication, 
    SSLPayment
)


class SSLPaymentTable(tables.Table):
    class Meta:
        model  = SSLPayment
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = (
            'transaction_id',
            'student_name',
            'payer',
            'payment_month',
            'received_amount',
            'pay_reason',
            'payer_mobile',
            'created'
        )