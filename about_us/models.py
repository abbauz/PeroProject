from django.db import models


class About(models.Model):
    class Meta:
        verbose_name = "About"
        verbose_name_plural = "1.About"

    id = models.AutoField(primary_key=True)
    description_en = models.TextField(verbose_name="About company Ru")
    description_uz = models.TextField(verbose_name="Description Uz", blank=True, null=True)
    description_ru = models.TextField(verbose_name="About company En")
    logo = models.CharField(max_length=1000, verbose_name="Company Logo")

    def __str__(self):
        return "about-company"


class PhotoModel(models.Model):
    class Meta:
        verbose_name = "Photo"
        verbose_name_plural = "2.Photo"

    id = models.AutoField(primary_key=True)
    photo = models.CharField(max_length=1000, verbose_name="Photo")
    description_uz = models.TextField(verbose_name="Description UZ", blank=True, null=True)
    description_ru = models.TextField(verbose_name="Description RU", blank=True, null=True)
    description_en = models.TextField(verbose_name="Description EN", blank=True, null=True)

    def __str__(self):
        return f"image - {self.id}"


class VideoModel(models.Model):
    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "3. Videos"

    id = models.AutoField(primary_key=True)
    video = models.CharField(max_length=1000, verbose_name="Video")
    description_uz = models.TextField(verbose_name="Description UZ", blank=True, null=True)
    description_ru = models.TextField(verbose_name="Description RU", blank=True, null=True)
    description_en = models.TextField(verbose_name="Description EN", blank=True, null=True)

    def __str__(self):
        return f"video - {self.id}"


class Messenger(models.Model):
    class Meta:
        verbose_name = "Messengers"
        verbose_name_plural = "2. Messengers"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=250)

    def __str__(self):
        return self.name
