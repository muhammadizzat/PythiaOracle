import os
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.core.exceptions import ValidationError
import datetime

# Create your models here.
def validate_file_extension(value):
        # import os
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.pdf']
        if not ext in valid_extensions:
            raise ValidationError(u'File not supported!')

class Position(models.Model):
    """
    all positions
    """
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.position

class CountryOriginated(models.Model):
    """
    all positions
    """
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.country

class ApplicantList(models.Model):
    name = models.CharField(max_length=200) 
    applicant_email = models.EmailField(verbose_name="E-mail Address")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name="Position applied for :")   
    status_choice = (
                    ('new', 'New'),
                    ('submitted', 'Submitted'),
                    ('rejected','Rejected'),
                    ('offered', 'Offered')
                    )
    status = models.CharField(max_length=30, choices=status_choice, verbose_name="Status :", default='new')
    unique_id = models.CharField(max_length=200,blank=True, null=True)
    submitted_date = models.DateField(blank=True, null=True)
    def __str__(self):
        return self.name

class JobApplication(models.Model):
    CHOICES = (
                    ('yes', 'Yes'),
                    ('no', 'No')
                    )
    # INDIVIDUAL PARTICULARS
    applicant = models.ForeignKey(ApplicantList, on_delete=models.CASCADE, related_name='+')
    name = models.CharField(max_length=200, verbose_name="Name (as in NRIC)")
    nick_name = models.CharField(max_length=50, verbose_name="Nickname :")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name="Position applied for :")
    applied_date = models.DateField(default=datetime.date.today)
    address = models.CharField(max_length=200, verbose_name="Current address :")
    age = models.IntegerField(verbose_name="Age :")
    def upload_photo_dir(self, filename):
        path = 'media/oracle/applicant/{}/photo/{}'.format(self.applicant.id, filename)
        return path
    photo = models.ImageField(upload_to=upload_photo_dir)
    gender_choice = (
                    ('male', 'Male'),
                    ('female', 'Female')
                    )
    gender = models.CharField(max_length=10, choices=gender_choice, verbose_name="Gender :")
    marital_choice = (
                    ('single', 'Single'),
                    ('married', 'Married')
                    )
    marital_status = models.CharField(max_length=10, choices=marital_choice, verbose_name="Marital Status :")
    nationality_choice = (
                    ('malaysian', 'Malaysian'),
                    ('foreigner', 'Foreigner')
                    )
    nationality = models.CharField(max_length=15, choices=nationality_choice, verbose_name="Nationality :")
    passport_ic = models.CharField(max_length=50, verbose_name="NRIC No :")
    country_live_in = models.CharField(max_length=5, choices=CHOICES, verbose_name="Are you currently living in Malaysia?", null=True, blank=True)
    country_originated_from = models.ForeignKey("CountryOriginated", on_delete=models.CASCADE, null=True, blank=True)
    mobile_phone = models.CharField(max_length=50, verbose_name="Mobile Phone No :")
    contact_phone = models.CharField(max_length=50, verbose_name="Contact No :")
    medical_condition = models.CharField(max_length=5, choices=CHOICES, verbose_name="Do you have medical condition to declare ? YES / NO")
    medical_identify = models.CharField(max_length=100, verbose_name="If yes, please identify :", null=True, blank=True)
    police_record = models.CharField(max_length=5, choices=CHOICES, verbose_name="Do you have any police record ? YES / NO")
    police_identify = models.CharField(max_length=100, verbose_name="If yes, please identify case involved :", null=True, blank=True)

    # EDUCATION & TRAINING
    # SPM
    spm_school_name = models.CharField(max_length=50, verbose_name="SPM School Name", null=True, blank=True)
    spm_certificate_level = models.CharField(max_length=50, verbose_name="SPM Level of Certification", null=True, blank=True)
    spm_graduated_year = models.DateField(verbose_name="SPM Year of Graduated", null=True, blank=True)
    # HIGHEST EDUCATION
    highest_education_name = models.CharField(max_length=50, verbose_name="Highest Education School / College / University Name", null=True, blank=True)
    highest_certificate_level = models.CharField(max_length=50, verbose_name="Highest Education Level of Certification", null=True, blank=True)
    highest_graduated_year = models.DateField(verbose_name="Highest Education Year of Graduated", null=True, blank=True)
    # PROFESSIONAL & OTHERS
    professional_college_name = models.CharField(max_length=50, verbose_name="Professional College / University Name", null=True, blank=True)
    professional_certificate_level = models.CharField(max_length=50, verbose_name="Professional Level of Certification", null=True, blank=True)
    professional_graduated_year = models.DateField(verbose_name="Professional Year of Graduated", null=True, blank=True)

    language = models.CharField(max_length=50, verbose_name="Language and dialects you speaks :")

    # WORKING EXPERIENCE
    total_working_experience = models.IntegerField(default=0, verbose_name="Total working experience :")
    portfolio_url =  models.URLField(max_length=1000)
    portfolio_url_2 =  models.URLField(max_length=1000, blank=True, null=True)
    portfolio_url_3 =  models.URLField(max_length=1000, blank=True, null=True)
    # EMPLOYER 1
    employer_1 = models.CharField(max_length=50, verbose_name="Employer (1) :", null=True, blank=True)
    job_title_1 = models.CharField(max_length=50, verbose_name="Job Title :", null=True, blank=True)
    date_employed_1 = models.DateField(verbose_name="Date Employed :", null=True, blank=True)
    date_end_1 = models.DateField(verbose_name="Date End :", null=True, blank=True)
    # EMPLOYER 2
    employer_2 = models.CharField(max_length=50, verbose_name="Employer (2) :", null=True, blank=True)
    job_title_2 = models.CharField(max_length=50, verbose_name="Job Title :", null=True, blank=True)
    date_employed_2 = models.DateField(verbose_name="Date Employed :", null=True, blank=True)
    date_end_2 = models.DateField(verbose_name="Date End :", null=True, blank=True)
    # EMPLOYER 3
    employer_3 = models.CharField(max_length=50, verbose_name="Employer (3) :", null=True, blank=True)
    job_title_3 = models.CharField(max_length=50, verbose_name="Job Title :", null=True, blank=True)
    date_employed_3 = models.DateField(verbose_name="Date Employed :", null=True, blank=True)
    date_end_3 = models.DateField(verbose_name="Date End :", null=True, blank=True)

    # POSITION INTERESTED IN
    available_joining_date = models.DateField(verbose_name="Available Joining Date :")
    current_pay = models.IntegerField(verbose_name="Current Pay by Month :")
    expected_pay = models.IntegerField(verbose_name="Expected Pay by Month :")

    # PERSONAL INTEREST
    hobbies = models.CharField(max_length=50, verbose_name="Hobbies :")
    other_information = models.CharField(max_length=100, verbose_name="Other information which help to consider your application :")

    # REFERENCE
    # REFERENCE 1
    reference_name_1 = models.CharField(max_length=50, verbose_name="Name")
    reference_title_1 = models.CharField(max_length=50, verbose_name="Title")
    reference_company_1 = models.CharField(max_length=50, verbose_name="Company")
    reference_contact_1 = models.CharField(max_length=50, verbose_name="Contact")
    reference_email_1 = models.EmailField(verbose_name="E-mail Address")
    
    # REFERENCE 2
    reference_name_2 = models.CharField(max_length=50, verbose_name="Name")
    reference_title_2 = models.CharField(max_length=50, verbose_name="Title")
    reference_company_2 = models.CharField(max_length=50, verbose_name="Company")
    reference_contact_2 = models.CharField(max_length=50, verbose_name="Contact")
    reference_email_2 = models.EmailField(verbose_name="E-mail Address")
    
    # ATTACHMENT
    # Mandatory
    def upload_resume_dir(self, filename):
        path = 'media/oracle/applicant/{}/resume/{}'.format(self.applicant.id, filename)
        return path
    resume_copy = models.FileField(upload_to=upload_resume_dir, validators=[validate_file_extension])
    def upload_ic_dir(self, filename):
        path = 'media/oracle/applicant/{}/passport_ic/{}'.format(self.applicant.id, filename)
        return path
    passport_ic_copy = models.FileField(upload_to=upload_ic_dir, validators=[validate_file_extension])
    def upload_certificate_dir(self, filename):
        path = 'media/oracle/applicant/{}/certificate/{}'.format(self.applicant.id, filename)
        return path
    highest_education_cert_copy = models.FileField(upload_to=upload_certificate_dir, validators=[validate_file_extension])
    def upload_payslip_dir(self, filename):
        path = 'media/oracle/applicant/{}/payslip/{}'.format(self.applicant.id, filename)
        return path
    payslip_or_graduation_letter = models.FileField(upload_to=upload_payslip_dir, validators=[validate_file_extension])
    # Not Mandatory
    def upload_recommendation_dir(self, filename):
        path = 'media/oracle/applicant/{}/recommendation_letter/{}'.format(self.applicant.id, filename)
        return path
    recommendation_letter = models.FileField(upload_to=upload_recommendation_dir, validators=[validate_file_extension], blank=True, null=True)
    
    def __str__(self):
        return self.name

class Feedback(models.Model):
    applicant = models.ForeignKey(ApplicantList, on_delete=models.CASCADE, related_name='+')
    interviewer_name = models.CharField(max_length=100, verbose_name="INTERVIEWER: ")
    interview_date = models.DateField(default=datetime.date.today)
    Feedback_CHOICES = (
                    ('unacceptable', 'Unacceptable'),
                    ('average', 'Average'),
                    ('acceptable', 'Acceptable')
                    )

    def __str__(self):
        return self.applicant.name

    # APPEREANCE 
    grooming = models.CharField(max_length=15, choices=Feedback_CHOICES, verbose_name="Grooming", default='')
    body_language = models.CharField(max_length=15, choices=Feedback_CHOICES, verbose_name="Body Language", default='')
    eye_contact = models.CharField(max_length=15, choices=Feedback_CHOICES, verbose_name="Eye Contact", default='')

    # CHARACTERISTIC
    confidence = models.CharField(max_length=15, choices=Feedback_CHOICES, verbose_name="Confidence", default='')
    teamwork = models.CharField(max_length=15, choices=Feedback_CHOICES, verbose_name="Teamwork", default='')
    responsible = models.CharField(max_length=15, choices=Feedback_CHOICES, verbose_name="Responsible", default='')
    professional = models.CharField(max_length=15, choices=Feedback_CHOICES, verbose_name="Professional/ Problem Solver", default='')
    communication = models.CharField(max_length=15, choices=Feedback_CHOICES, verbose_name="Communication", default='')
    ability_to_learn = models.CharField(max_length=15, choices=Feedback_CHOICES, verbose_name="Ability to Learn", default='')
    punctuality = models.CharField(max_length=15, choices=Feedback_CHOICES, verbose_name="Punctuality", default='')
    qualification = models.CharField(max_length=15, choices=Feedback_CHOICES, verbose_name="Education / Qualification", default='')
    skills = models.CharField(max_length=15, choices=Feedback_CHOICES, verbose_name="Skills", default='')
    creativity = models.CharField(max_length=15, choices=Feedback_CHOICES, verbose_name="Creativity", default='')
    knowledge_on_company = models.CharField(max_length=15, choices=Feedback_CHOICES, verbose_name="Knowledge on Company", default='')
    knowledge_on_industry = models.CharField(max_length=15, choices=Feedback_CHOICES, verbose_name="Knowledge on Industry", default='')
    evaluation = models.CharField(max_length=15, choices=Feedback_CHOICES, verbose_name="Evaluation", default='')
    comments = models.TextField(verbose_name="ADDITIONAL COMMENTS :")

    feedback_time = models.DateField(auto_now_add=True)