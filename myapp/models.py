from django.db import models

def validate_date(value):
    if value.year < 1920 or value.year > 2023:
        raise ValidationError(
            _("Invalid date: Year must be greater than or equal to 1900.")
        )
        
# Create your models here.
class Student(models.Model):
    masv = models.TextField(primary_key=True)
    hoten = models.TextField(max_length=100)
    ngaysinh = models.DateField(validators=[validate_date])
    quequan = models.TextField(max_length=100)
    class Meta:
        db_table = 'sinhvien'