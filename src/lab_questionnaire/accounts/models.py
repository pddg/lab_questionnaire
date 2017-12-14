from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from questionnaire.models import StudyOffice


class MyUserManager(BaseUserManager):
    def create_user(self, student_number, password=None, **extra_fields):
        if not student_number:
            raise ValueError('Users must have a student number')
        user = self.model(student_number=student_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, student_number, password):
        return self.create_user(student_number, password, is_staff=True, is_superuser=True)


class MyUser(AbstractBaseUser, PermissionsMixin):
    student_number = models.CharField(max_length=64, unique=True, default="", verbose_name=u"学生ID")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # アンケートデータ
    display_name = models.CharField(max_length=16, null=True, blank=True, verbose_name=u"表示名", help_text=u"集計ページで学生IDの代わりに表示されます。（任意）")
    gpa = models.FloatField(default=0, verbose_name=u"GPA")
    first_choice = models.ForeignKey(StudyOffice, related_name="first_choiced_user",
                                     null=True, blank=True, on_delete=models.SET_NULL, verbose_name=u"第一希望研究室")

    USERNAME_FIELD = 'student_number'

    objects = MyUserManager()

    def __str__(self):
        return self.student_number

    class Meta:
        verbose_name = u"ユーザ"
