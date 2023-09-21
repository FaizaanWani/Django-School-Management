from django.urls import path
from . import views


app_name = 'payments'

urlpatterns = [
    path('sslpays/', views.dashboard_ssl_payments_list,
        name='dashboard_ssl_payments_list'
    ),
path('add/', views.add_fees_view,
        name='add_offline_fee'
    ),
# path('view_fees/', views.TableView,
#         name='dashboard_ssl_payments_list'
#     ),
# path('view_fees2/', views.PermissionAjaxDatatableView.as_view(), name="ajax_datatable_permissions"),
]