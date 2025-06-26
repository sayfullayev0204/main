from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class Nation(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Region(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name


class District(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="districts")

    def __str__(self):
        return f"{self.name} ({self.region.name})"


class Village(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="villages")

    def __str__(self):
        return f"{self.name} ({self.district.name})"


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    last_login = models.DateTimeField(auto_now=True)

    CHOISE_ROLE = (
        ('region_admin', 'region_admin'),
        ('district_admin', 'district_admin'),
        ('inspector', 'inspector'),
    )
    role = models.CharField(max_length=50, choices=CHOISE_ROLE)
    birthday = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True, choices=(
        ('male','male'),
        ('fmale','fmale')
    ))
    phone = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    rank = models.CharField(max_length=50, null=True, blank=True)
    photo = models.ImageField(upload_to='users/', null=True, blank=True)
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, null=True, blank=False)
    jshshir = models.IntegerField(unique=True, null=True, blank=True, verbose_name="JSHSHIR")
    nation = models.ForeignKey(Nation, on_delete=models.SET_NULL, null=True, blank=False, related_name="users")
    position = models.CharField(max_length=50, null=True, blank=True)
    work_addres = models.TextField(null=True, blank=True)
    @property
    def district(self):
        """Foydalanuvchiga tegishli tumanni qaytaradi."""
        return self.village.district if self.village else None

    @property
    def region(self):
        """Foydalanuvchiga tegishli viloyatni qaytaradi."""
        return self.village.district.region if self.village else None

    def __str__(self) -> str:
        return f"{self.username}"


class Apartment(models.Model):
    name = models.CharField(max_length=100)
    village = models.ForeignKey(Village, on_delete=models.CASCADE, related_name="apartments")
    area = models.FloatField()
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = "Uy"
        verbose_name_plural = "Uylar"

class Citizn(models.Model):
    Village = models.ForeignKey(Village, on_delete=models.CASCADE, related_name="citizens")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    birthday = models.DateTimeField()
    phone = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, null=True, blank=True, choices=(
        ('male','male'),
        ('female','female')
    ))
    nation = models.ForeignKey(Nation, on_delete=models.CASCADE)
    jshshir = models.IntegerField()
    photo = models.ImageField(upload_to='citizens/', null=True, blank=True)
    marital_status = models.CharField(max_length=50, null=True, blank=True, choices=(
        ("oilali","oilali"),
        ("uyalnmagan","uyalnmagan"),
        ("beva","beva"),
        ("ajrashgan","ajrashgan")
    ))
    children_count = models.IntegerField()
    income_level = models.CharField(max_length=50, null=True, blank=True, choices=(
        ("past","past"),
        ("o'rta","o'rta"),
        ("yuqori","yuqori")
    ))
    workplace = models.TextField()
    employment_status = models.CharField(max_length=50, null=True, blank=True, choices=(
        ("ishsiz","ishsiz"),
        ("ishlaydigan","ishlaydigan"),
        ("pensioner","pensioner"),
        ("talaba","talaba")
    ))
    house_ownership = models.CharField(max_length=50, null=True, blank=True, choices=(
        ("o'zida","o'zida"),
        ("ijarada","ijarada"),
        ("uysiz","uysiz")
    ))
    street = models.CharField(max_length=300)
    home = models.CharField(max_length=300)
    is_at_risk = models.BooleanField(default=False)
    needs_support = models.BooleanField(default=False)
    under_supervision = models.BooleanField(default=False)
    apartment = models.ForeignKey(Apartment, on_delete=models.SET_NULL, null=True, blank=True, related_name="citizens")
    landlord = models.BooleanField(default=False)
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

class PersonalCategroy(models.Model):
    name = models.CharField(max_length=300)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Shaxsiy toifasi"
        verbose_name_plural = "Shaxsiy toifalari"

class PersonalStatus(models.Model):
    citzen = models.ForeignKey(Citizn, on_delete=models.CASCADE, related_name="personal_statuses")
    category = models.ForeignKey(PersonalCategroy, on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return f"{self.citzen.first_name} - {self.category.name}"
    
    class Meta:
        verbose_name = "Shaxsiy holati"
        verbose_name_plural = "Shaxsiy holatlari"


class GoalLeaave(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ketish maqsadi"
        verbose_name_plural = "Ketish maqsadi"

class FieldWork(models.Model):
    name = models.CharField(max_length=300)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ish yoki o'qish joyi"
        verbose_name_plural = "Ishyoki o'qish joyi"
        

class State(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Davlat"
        verbose_name_plural = "Davlat"
        

class Leave(models.Model):
    citizen = models.ForeignKey(Citizn, on_delete=models.CASCADE,related_name="leaves")
    start_add_date = models.DateTimeField()
    end_add_date = models.DateTimeField()
    start_leave_date = models.DateTimeField()
    end_leave_date = models.DateTimeField()
    deadline = models.CharField(max_length=20)
    goal = models.ForeignKey(GoalLeaave, on_delete=models.CASCADE)
    work_field = models.ForeignKey(FieldWork, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    address = models.TextField()
    start_come_date = models.DateTimeField()
    end_come_date = models.DateTimeField()
    reason_come = models.TextField()
    deport = models.BooleanField(default=False)
    violation = models.BooleanField()

    def __str__(self):
        return self.citizen.first_name
    
    class Meta:
        verbose_name = "Tark etish"
        verbose_name_plural = "Tark etish"


class ServiceCategory(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Xizmat turlari"
        verbose_name_plural = "Xizmatlar turlari"

class Service(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="services")
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name="services")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.name} - {self.user.username}"

    class Meta:
        verbose_name = "Xizmat"
        verbose_name_plural = "Xizmatlar"

class ServiceImage(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='service_images/')
    
    def __str__(self):
        return f"Image for {self.service}"
    
    class Meta:
        verbose_name = "Xizmat rasmi"
        verbose_name_plural = "Xizmat rasmlari"