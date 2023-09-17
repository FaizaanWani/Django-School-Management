from unicodedata import decimal

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.views.generic import ListView
from .models import SSLPayment
from .tables import SSLPaymentTable
from .filters import SSLPaymentFilter
from django_school_management.accounts.forms import UserCreateFormDashboard
from django_school_management.payments.forms import FeeEntry
from django_school_management.payments.models import SSLPayment
from django_school_management.students.models import AdmissionStudent, Student
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
import copy


class DashboardSSLPaymentsList(SingleTableMixin, FilterView):
    model = SSLPayment
    table_class = SSLPaymentTable
    template_name = 'payments/dashboard/sslpayments.html'
    filterset_class = SSLPaymentFilter


dashboard_ssl_payments_list = DashboardSSLPaymentsList.as_view()


def store_admission_pay_record(post_body):
    try:
        SSLPayment.objects.create(**post_body)
        return True
    except Exception as e:
        raise e
        return False


from decimal import Decimal


def clean_data(data):
    clnd = {}
    for key, val in data.items():
        if key in ["student_name", "payer_email", "payer_mobile", "payer_city", "payer_country"]:
            all = AdmissionStudent.objects.all()
            print(all)
            registrant = Student.objects.get(pk=data['student_name'][0])
            adm = AdmissionStudent.objects.get(pk=data['student_name'][0])
            clnd["student_name"] = registrant
            clnd["payer_email"] = adm.email
            clnd["payer_mobile"] = adm.mobile_number
            clnd["payer_city"] = adm.city
            clnd["payer_country"] = adm.permanent_address
        elif key in ["transaction_id", "received_amount"]:
            amt = val[0]
            print(amt)
            clnd[key] = Decimal(amt)
        else:
            clnd[key] = val[0]

        # assert len(data) == len(clnd)
    print(clnd)
    return clnd


from datetime import datetime


@login_required
def add_fees_view(request):
    if request.user.has_perm('create_stuff'):
        if request.method == 'POST':
            data = dict(copy.deepcopy(request.POST))
            # del data["transaction_id"]
            del data["csrfmiddlewaretoken"]
            print(data, "DDD)))))))")
            key = datetime.now().strftime("%Y%m%d%H%M%S%Z")
            data["transaction_id"] = [key]
            data["payer"] = [request.user.username]
            clnd_data = clean_data(data)

            print(clnd_data, "Afterrrrrr")
            store_admission_pay_record(clnd_data)
            return render(request, 'payments/add_payments.html', {'user_form': FeeEntry()})

            user_form = FeeEntry(**data)

            # print(user_form)
            if user_form.is_valid():
                user = user_form.save()
                # return redirect(
                #     user.get_author_url()
                # )
                context = {
                    'user_form': user_form,
                }
                return render(request, 'payments/add_payments.html', context)
        else:
            user_form = FeeEntry()
        context = {
            'user_form': user_form,
        }
        return render(request, 'payments/add_payments.html', context)
    else:
        return render(request, 'academics/permission_required.html')
