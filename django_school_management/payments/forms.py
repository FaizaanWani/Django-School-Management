from django import forms
from .models import (
    SSLAdmissionPaymentVerfication,
    SSLPayment
)


class FeeEntry(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
        # super(FeeEntry, self).__init__(*args, **kwargs)
        # super().__init__()

    # def __init__(self, transaction_id=None, *args, **kwargs):
    #     super(FeeEntry, self).__init__(*args, **kwargs)
    #     print(kwargs,transaction_id, "....--")
        # self.site_id = kwargs.pop('site_id')
        # super(FeeEntry, self).__init__(*args, **kwargs)
        # self.fields['transaction_id'].widget = "Ddd"
        # self.fields['payer'].widget = "ccc"

    class Meta:
        model = SSLPayment
        fields = (
            'transaction_id', 'student_name', 'payer', 'received_amount',
            'pay_reason', 'payer_mobile', 'payer_email',
            'payer_city', 'payer_country', 'payment_month'
        )
        widgets = {'transaction_id': forms.HiddenInput(),
                   'payer': forms.HiddenInput(),
                   'payer_email': forms.HiddenInput(),
                   'payer_city': forms.HiddenInput(),
                   'payer_country': forms.HiddenInput(),
                   'payer_mobile': forms.HiddenInput()}