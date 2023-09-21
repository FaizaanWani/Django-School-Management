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

from django_tables2.export.export import TableExport


class DashboardSSLPaymentsList(SingleTableMixin, FilterView):
    model = SSLPayment
    table_class = SSLPaymentTable
    template_name = 'payments/dashboard/sslpayments.html'
    filterset_class = SSLPaymentFilter
    # def get(self, request, *args, **kwargs):
    #     table = SSLPaymentTable(SSLPayment.objects.all())
    #
    #     RequestConfig(request).configure(table)
    #
    #     export_format = request.GET.get('_export', None)
    #     if TableExport.is_valid_format(export_format):
    #         exporter = TableExport(export_format, table)
    #         return exporter.response('table.{}'.format(export_format))
    #     return render(request, 'payments/dashboard/sslpayments.html', {
    #         'people': table
    #     })
    #     export_format = request.GET.get('_export', None)
    #     print(export_format)
    # if TableExport.is_valid_format(export_format):
    #     table = [[your table object]]
    #     exporter = TableExport(export_format, table)
    #     return exporter.response('File_Name.{}'.format(export_format))


dashboard_ssl_payments_list = DashboardSSLPaymentsList.as_view()

from django_tables2 import RequestConfig
from django_tables2.export.export import TableExport


def TableView(request):
    table = SSLPaymentTable(SSLPayment.objects.all())

    RequestConfig(request).configure(table)

    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('table.{}'.format(export_format))

    return render(request, 'payments/dashboard/view_fees.html', {
        'people': table
    })


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


from django.shortcuts import render


def ViewFees(request):
    fees = FeeEntry(SSLPayment.objects.all())
    # print(fees)
    return render(request, "payments/dashboard/view_fees.html", {'people': fees})


from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.models import Permission


class PermissionAjaxDatatableView(AjaxDatatableView):
    model = SSLPayment
    title = 'Permissions'
    initial_order = [["app_label", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'
    template_name = 'payments/dashboard/permissions_list.html'

    # column_defs = [
    #     AjaxDatatableView.render_row_tools_column_def(),
    #     {'name': 'id', 'visible': False, },
    #     {'name': 'codename', 'visible': True, },
    #     {'name': 'name', 'visible': True, },
    #     {'name': 'app_label', 'foreign_field': 'content_type__app_label', 'visible': True, },
    #     {'name': 'model', 'foreign_field': 'content_type__model', 'visible': True, },
    # ]
