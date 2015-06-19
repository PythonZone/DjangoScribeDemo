# coding=utf-8

from django.contrib import admin

from .models import Company, Department, Employee


class CompanyAdmin(admin.ModelAdmin):
    pass


class DepartmentAdmin(admin.ModelAdmin):
    pass


class EmployeeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Company, CompanyAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)
