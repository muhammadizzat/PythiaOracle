from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import EmailMultiAlternatives
from rest_framework import status
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import JobApplication, Feedback, ApplicantList
from .serializers import JobApplicationSerializer, ApplicantStatusSerializer, FeedbackSerializer, ApplicantListSerializer, JobApplicationAttachmentSerializer, ApplicantAddSerializer


class ApplicantListAllAPI(APIView):
    def get(self, request):
        all_applicant = ApplicantList.objects.all().select_related('position')
        applicant_list_serializer = ApplicantListSerializer(all_applicant, many=True)
        return Response(applicant_list_serializer.data)
    
    def post(self, request, format=None):
        serializer = ApplicantAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            inst = request.data
            # ------------------------------------------------ EMAIL NOTIFICATION SETTINGS START---------------------------------------------------------------------------#
            # subject = 'Thank you for applying to our company! - {}'.format(inst["name"])
            # text_content = 'Thank you for applying to our company! - {}'.format(inst["name"])
            # html_content = """
            #             <p>Dear {},<br><br>
            #                Greetings!<br>
            #                 Thank you for your interest in our company. <br><br>
            #                 To proceed with your application, we will require you to fill up the form linked below.<br>
            #                 <h3 style="color: #0b9ac4"><a href="http://127.0.0.1:8000/oracle/application_form/{}/" target="_blank">Application Form Link</a></h3>
            #                 Please remember to not leave any blanks and attached the proper documents. Remember to check for any mistake as you will not be able to edit the form again after submitting.<br><br>
            #                 We will update you as soon as we have received your submission.<br>
            #                 Thank you and looking forward!<br><br>
            #                 Please email us at oracle@pythiacareer.com if you have any inquiries.<br>
            #                 Thanks!</p>
            #             """.format(inst["name"] ,inst["unique_id"])
            # to = [inst["applicant_email"]]
            # send_email(subject, text_content, html_content, to)
            # ------------------------------------------------ EMAIL NOTIFICATION SETTINGS END ---------------------------------------------------------------------------#
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApplicantListUpdateAPI(APIView):
    def get_object(self, applicant_id):
        try:
            return ApplicantList.objects.get(pk=applicant_id)
        except ApplicantList.DoesNotExist:
            raise Http404

    def get(self, request, applicant_id, format=None, **kwargs):
        model_object = self.get_object(applicant_id)
        serializer = ApplicantListSerializer(model_object)
        return Response(serializer.data)

    def put(self, request, applicant_id):
        model_object = self.get_object(applicant_id)
        serializer = ApplicantListSerializer(model_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, applicant_id, format=None):
        model_object = self.get_object(applicant_id)
        model_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ApplicantStatusAPI(APIView):
    def get_object(self, applicant_id):
        try:
            return ApplicantList.objects.get(pk=applicant_id)
        except ApplicantList.DoesNotExist:
            raise Http404

    def get(self, request, applicant_id, format=None, **kwargs):
        model_object = self.get_object(applicant_id)
        serializer = ApplicantStatusSerializer(model_object)
        return Response(serializer.data)

    def put(self, request, applicant_id):
        model_object = self.get_object(applicant_id)
        serializer = ApplicantStatusSerializer(model_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # ------------------------------------------------ EMAIL NOTIFICATION SETTINGS START---------------------------------------------------------------------------#
            # inst = request.data
            # if inst["status"] == "submitted":
            #     subject = 'Thank you for your submission - {}'.format(inst["name"])
            #     text_content = 'Thank you for your submission - {}'.format(inst["name"])
            #     html_content = """
            #                 <p>Dear {},<br><br>
            #                 Thank you, we have received your submission and is currently reviewing your application.<br><br>
            #                 We will update you once we are done reviewing your application.<br>
            #                 Appreciate your kind understanding and patience on the process.<br><br>
            #                 Please email us at oracle@pythiacareer.com if you have any inquiries.<br> 
            #                 Thanks!
            #                 </p>
            #                 """.format(inst["name"])
            # if inst["status"] == "rejected":
            #     subject = 'Application Status - {}'.format(inst["name"])
            #     text_content = 'Application Status - {}'.format(inst["name"])
            #     html_content = """
            #                 <p>Dear {},<br><br>
            #                 Greetings!<br><br>
            #                 Thank you for your interest in our company!<br><br>
            #                 After reviewed your application we received, we regret to inform that there is no suitable vacancy fit with your skills and capabilities at this moment.<br><br> 
            #                 We really appreciate the time you invested in your application and encourage you to apply again in the future as we are pleased to see your improvement skills. We wish you all the best in your career endeavour!<br><br>
            #                 Have a great day ahead!
            #                 </p>
            #                 """.format(inst["name"])
            # # ------------------------------------------------ EMAIL NOTIFICATION SETTINGS END ---------------------------------------------------------------------------#
            # if inst["status"] == "offered":
            #     return Response(serializer.data, status=status.HTTP_201_CREATED)
            # to = [inst["applicant_email"]]
            # send_email(subject, text_content, html_content, to)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobApplicationAttachmentAPI(APIView):
    def get_object(self, applicant_id):
        try:
            return JobApplication.objects.all().filter(applicant=applicant_id).select_related('applicant', 'position')
        except JobApplication.DoesNotExist:
            raise Http404

    def get(self, request, applicant_id, format=None, **kwargs):
        model_object = self.get_object(applicant_id)
        serializer = JobApplicationAttachmentSerializer(model_object, many=True)
        return Response(serializer.data)

class FeedbackAPI(APIView):
    def get_object(self, applicant_id):
        try:
            return Feedback.objects.all().filter(applicant=applicant_id).select_related('applicant')
        except Feedback.DoesNotExist:
            raise Http404

    def get(self, request, applicant_id, format=None, **kwargs):
        applicant_feedback = self.get_object(applicant_id)
        serializer = FeedbackSerializer(applicant_feedback, many=True)
        return Response(serializer.data)

def send_email(subject, text_content, html_content, to):
    """
    Send email notification
    """
    # INSERT SENDER EMAIL HERE
    from_email = ''
    footer = """
                </br>
                </br>
                </br>
                </br>
                <h5>Do not reply to this email. This is automated email notification from Pythia.</h5>
                </br>
                <div style="font-size: 13px; font-family: Tahoma, Helvetica, sans-serif;"><br></div>
                <div style="font-size: 13px; font-family: Tahoma, Helvetica, sans-serif;"><br></div>
                <div style="font-size: 13px; font-family: Tahoma, Helvetica, sans-serif;"><br></div>
                <div style="font-size: 13px; font-family: Tahoma, Helvetica, sans-serif;"><span style="color: rgb(153, 153, 153); font-family: tahoma, sans-serif; font-size: x-small; background-color: rgb(255, 255, 255);">This message and any attachment(s) is intended only for the use of the addressee(s) and may contain information that is PRIVILEGED and CONFIDENTIAL. If you are not the intended addressee(s), you are hereby notified that any use, distribution, disclosure or copying of this communication is strictly prohibited. If you have received this communication in error, please erase all copies of the message and its attachment(s) and notify the sender immediately.</span></div>&nbsp;</div>
                """
    email_body = html_content + footer
    email_template = EmailMultiAlternatives(subject, text_content, from_email, to)
    email_template.attach_alternative(email_body, "text/html")
    email_template.send()