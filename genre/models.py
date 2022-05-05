from django.db import models

# Create your models here.

class Genre(models.Model):
	title = models.CharField(max_length=150)
	slug = models.SlugField(null=False, unique=False)
	livros = models.ManyToManyField('livros.Ebook', related_name= 'genero_livros', blank=True)

	def get_absolute_url(self):
		return reverse('genres', args=[self.slug])

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.title.replace(" ", "")
			self.slug = slugify(self.title)
		return super().save(*args, **kwargs)