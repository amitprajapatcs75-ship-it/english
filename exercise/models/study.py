from django.db import models
from django.core.validators import FileExtensionValidator
from common.models.common import CommonFields
from users.models.users import User

class Song(CommonFields):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to="study_materials/", validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'jfif'])])
    tag = models.CharField(max_length=120, null=True, blank=True)
    file = models.FileField(upload_to='study_materials/songs/', validators=[FileExtensionValidator(allowed_extensions=['mp3', '.mp3', '.aac', '.wav', '.aiff', '.flac', '.alac'])])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.tag = "Song"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Books(CommonFields):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to="study_materials/books", validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'jfif'])])
    tag = models.CharField(max_length=120, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.tag = "Books"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Article(CommonFields):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to="study_materials/article", validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'jfif'])])
    tag = models.CharField(max_length=120, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.tag = "Article"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Interview(CommonFields):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to="study_materials/interview", validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'jfif'])])
    tag = models.CharField(max_length=120,null=True, blank=True)

    def save(self, *args, **kwargs):
        self.tag = "Interview"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Question(CommonFields):
    phrase = models.CharField(max_length=255)
    question = models.CharField(max_length=250)
    option_a = models.CharField(max_length=100)
    option_b = models.CharField(max_length=100)
    correct_option = models.CharField(max_length=100)

    def __str__(self):
        return self.question

class UserAnswer(CommonFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="question_answer")
    user_answer = models.CharField(max_length=120)
    is_correct = models.BooleanField(default=False)