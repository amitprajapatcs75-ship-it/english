from django.db import models
from common.models.common import CommonFields
from django.core.validators import FileExtensionValidator

class GrammarExercise(CommonFields):
    level = models.CharField(max_length=255, default="Elementary")
    topic_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to="grammar", validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'jfif'])],
                                      null=True, blank=True)

    def __str__(self):
        return self.name

class VocabularyExercise(CommonFields):
    words_count = models.PositiveIntegerField()
    level = models.CharField(max_length=255, default="Elementary")
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="exercise_category", validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'jfif'])],
                                      null=True, blank=True)

    def __str__(self):
        return self.title