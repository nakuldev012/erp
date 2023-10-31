from django.contrib import admin
from .models import PrimaryEmpInfo, BasicEmpInfo, PersonalEmpInfo, AccountEmpInfo, AddressEmpInfo, AcademicEmpInfo, CertificationEmpInfo, DoctorateEmpInfo, EmpPreviousExp, EmpCurrentExp, EmpReporting
admin.site.register(PrimaryEmpInfo)
admin.site.register(BasicEmpInfo)
admin.site.register(PersonalEmpInfo)
admin.site.register(AccountEmpInfo)
admin.site.register(AddressEmpInfo)
admin.site.register(AcademicEmpInfo)
admin.site.register(CertificationEmpInfo)
admin.site.register(DoctorateEmpInfo)
admin.site.register(EmpPreviousExp)
admin.site.register(EmpCurrentExp)
admin.site.register(EmpReporting)