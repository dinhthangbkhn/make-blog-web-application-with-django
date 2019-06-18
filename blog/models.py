'''
Design blog data schema by defining the data models for blog. 
A model is a python class that subclasses django.db.models.Model, 
in which each attribute represents a database field. 

Django provides with a practical API to query objects in the database easily.
'''


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    ''' Create PublishedManager

    This class is used to create a custom manager to retrieve all posts with the 'published' status
    The manager will allow us to retrieve posts using Post.published.all()
    '''
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset() \
                                            .filter(status='published')



class Post(models.Model):
    ''' Define Post Model

    Dat model for blog posts
    '''
    STATUS_CHOICES = (
        ('drafe', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', 
                        args=[
                            self.publish.year,
                            self.publish.month,
                            self.publish.day,
                            self.slug
                        ])
