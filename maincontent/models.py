from django.db import models
import uuid

# Create your models here.


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    img = models.ImageField(upload_to='posts/', default='img/images.png')
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    body = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.email}"


class ProjectCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "project categories"

    def __str__(self):
        return self.name


class Projects(models.Model):
    title = models.CharField(max_length=150)
    category = models.ForeignKey(
        ProjectCategory, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="projects",
    )
    img = models.ImageField(upload_to="projects/", default='img/images.png')
    description = models.TextField(default='')
    live_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tech_stack = models.CharField(
        max_length=200, blank=True, default="",
        help_text="Separate with commas, e.g. Flutter, Firebase, Dart",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()]

class ProjectImage(models.Model):
    project = models.ForeignKey(
        Projects, on_delete=models.CASCADE, related_name="gallery"
    )
    image = models.ImageField(upload_to="projects/gallery/")
    caption = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"{self.project.title} image"