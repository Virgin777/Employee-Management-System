from django.db import models
from django.conf import settings
from decimal import Decimal


class Payroll(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payroll_records')
    month = models.IntegerField()  # 1-12
    year = models.IntegerField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    house_rent_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medical_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transport_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    overtime_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Deductions
    tax_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    provident_fund = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    insurance_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    total_deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    
    generated_date = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='generated_payrolls')
    
    class Meta:
        db_table = 'payroll'
        unique_together = ('employee', 'month', 'year')
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.employee.full_name} - {self.month}/{self.year}"

    def save(self, *args, **kwargs):
        # Calculate gross salary
        self.gross_salary = (
            self.basic_salary + 
            self.house_rent_allowance + 
            self.medical_allowance + 
            self.transport_allowance + 
            self.bonus + 
            self.overtime_pay
        )
        
        # Calculate total deductions
        self.total_deductions = (
            self.tax_deduction + 
            self.provident_fund + 
            self.insurance_deduction + 
            self.other_deductions
        )
        
        # Calculate net salary
        self.net_salary = self.gross_salary - self.total_deductions
        
        super().save(*args, **kwargs)
