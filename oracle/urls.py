from django.conf.urls import url
from .views import *
from . import api
urlpatterns = [
    # API URL PATH
    url(r'^api/oracle/applicant_list/$', api.ApplicantListAllAPI.as_view(), name='applicant_list'), 
    url(r'^api/oracle/applicant_update/(?P<applicant_id>\d+)/$', api.ApplicantListUpdateAPI.as_view(), name='applicant_list_update'),
    url(r'^api/oracle/applicant_attachment/(?P<applicant_id>\d+)/$', api.JobApplicationAttachmentAPI.as_view(), name='applicant_attachment'),
    url(r'^api/oracle/status_detail/(?P<applicant_id>\d+)/$', api.ApplicantStatusAPI.as_view(), name='status_detail'),
    url(r'^api/oracle/feedback_detail/(?P<applicant_id>\d+)/$', api.FeedbackAPI.as_view(), name='feedback'),

    url(r'^$', oracle_view, name='oracle_view'),
    url(r'^oracle/application_form/(?P<unique_id>[\w ]+)/$', application_form_view, name='application_form_view'),
    url(r'^oracle/applicant_credential/(?P<applicant_id>\d+)/$', applicant_credential_view, name='applicant_credential_view'),
    url(r'^oracle/feedback_checklist/(?P<applicant_id>\d+)/$', feedback_checklist_view, name='feedback_checklist_view'),
    url(r'^oracle/feedback_result/(?P<feedback_id>\d+)/$', feedback_result_view, name='feedback_result_view'),
]