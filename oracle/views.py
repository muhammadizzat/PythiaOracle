from django.shortcuts import render, get_object_or_404
from .models import *
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from .forms import JobApplicationForm, FeedbackForm, ApplicantListForm, PositionForm

def oracle_view(request):
    """
    Homepage Page
    :param request:
    :return:
    """
    applicant = JobApplication.objects.all()
    form = ApplicantListForm(request.POST or None)
    position_form = PositionForm(request.POST or None, request.FILES or None)
    if position_form.is_valid():
        inst = position_form.save(commit=False)
        inst.save()
        return HttpResponseRedirect("/")
    context = {'form': form,
               'position_form': position_form,
               'applicant': applicant}
    return render(request, 'oracle/homepage.html', context=context)

def application_form_view(request, unique_id):
    """
    Application Form
    :param request:
    :return:
    """
    selected_applicant = get_object_or_404(ApplicantList, unique_id=unique_id)
    form = JobApplicationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        inst = form.save(commit=False)
        inst.save()
        # ------------------------------------------------ APPLICANT EMAIL NOTIFICATION SETTINGS START---------------------------------------------------------------------------#
        # applicant_subject = 'Thank you for your submission - {}'.format(inst.name)
        # applicant_text_content = 'Thank you for your submission - {}'.format(inst.name)
        # applicant_html_content = """
        #             <p>Dear {},<br><br>
        #             Thank you, we have received your submission and is currently reviewing your application.<br><br>
        #             We will update you once we are done reviewing your application.<br>
        #             Appreciate your kind understanding and patience on the process.<br><br>
        #             Please email us at inquire@pythiacareer.com if you have any inquiries.<br> 
        #             Thanks!
        #             </p>
        #             """.format(inst.name)
        # applicant_to = [selected_applicant.applicant_email, "oracle.core@gmail.com"]
        # send_email(applicant_subject, applicant_text_content, applicant_html_content, applicant_to)
        # ------------------------------------------------ APPLICANT EMAIL NOTIFICATION SETTINGS END ---------------------------------------------------------------------------#
        # ------------------------------------------------ HR EMAIL NOTIFICATION SETTINGS START---------------------------------------------------------------------------#
        # hr_subject = 'Pythia Oracle Interview'
        # hr_text_content = 'Pythia Oracle Interview (Update : Submitted form Received)'
        # hr_html_content = """
        #             <h3 style="color: #0b9ac4"><span style="text-transform: uppercase;">{}</span>, has submitted his/her form</h3>
        #             """.format(inst.name)
        # hr_to = [selected_applicant.applicant_email, "oracle.core@gmail.com"]
        # send_email(hr_subject, hr_text_content, hr_html_content, hr_to)
        # # ------------------------------------------------ HR EMAIL NOTIFICATION SETTINGS END ---------------------------------------------------------------------------#
    context = {'form': form,
                'selected_applicant': selected_applicant}
    return render(request, 'oracle/application_form.html', context=context)

def applicant_credential_view(request, applicant_id):
    credential_list = JobApplication.objects.all().filter(applicant_id=applicant_id)
    for credential in credential_list:
        available_joining_date = credential.available_joining_date.strftime('%B, %Y')
        
        if credential.spm_graduated_year is None:
            spm_graduated_year = 'None'
        else:
            spm_graduated_year = credential.spm_graduated_year.strftime('%Y')
        if credential.highest_graduated_year is None:
            highest_graduated_year = 'None'
        else:
            highest_graduated_year = credential.highest_graduated_year.strftime('%Y')
        if credential.professional_graduated_year is None:
            professional_graduated_year = 'None'
        else:
            professional_graduated_year = credential.professional_graduated_year.strftime('%Y')

    context = {'credential_list': credential_list,
                'available_joining_date': available_joining_date,
                'spm_graduated_year': spm_graduated_year,
                'highest_graduated_year': highest_graduated_year,
                'professional_graduated_year': professional_graduated_year}
    return render(request,'oracle/applicant_credential.html', context)

def feedback_checklist_view(request, applicant_id):
    """
    Feedback Checklist
    :param request:
    :return:
    """
    form = FeedbackForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        inst = form.save(commit=False)
        inst.save()
    context = {'form': form, 'applicant_id': applicant_id}
    return render(request, 'oracle/feedback_checklist.html', context=context)

def feedback_result_view(request, feedback_id):
    result_list = Feedback.objects.all().filter(id=feedback_id)
    context = {'result_list': result_list}
    return render(request,'oracle/feedback_result.html', context=context)

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