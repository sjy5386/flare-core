from django.urls import path

from . import views

app_name = 'dns_records'
urlpatterns = [
    path('', views.DnsRecordListView.as_view(), name='list'),
    path('export/', views.ZoneExportView.as_view(), name='zone_export'),
    path('import/', views.ZoneImportView.as_view(), name='zone_import'),
    path('create/', views.DnsRecordCreateView.as_view(), name='create'),
    path('<str:id>/', views.DnsRecordDetailView.as_view(), name='detail'),
    path('<str:id>/update/', views.DnsRecordUpdateView.as_view(), name='update'),
    path('<str:id>/delete/', views.DnsRecordDeleteView.as_view(), name='delete'),
]
