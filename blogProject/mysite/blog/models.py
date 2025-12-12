from django.conf import settings
from django.db import models
from django.utils import timezone
# from django.db.models.functions import Now  

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        Published = 'PB', 'Published'
    # defined the enumeration class Status by subclassing models.TextChoices. The available
    # choices for the post status are DRAFT and PUBLISHED. Their respective values are DF and PB, and their
    # labels or readable names are Draft and Published.
    # We can access Post.Status.choices to obtain the available choices, Post.Status.names to obtain the
    # names of the choices, Post.Status.labels to obtain the human-readable names, and Post.Status.
    # values to obtain the actual values of the choices.

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    # imported the project’s settings and we have added an author field to the Post model 'from django.conf import settings'. 
    # This field defines a many-to-one relationship with the default user model, meaning that each post is written
    # by a user, and a user can write any number of posts. For this field, Django will create a foreign key in
    # the database using the primary key of the related model.
    # The on_delete parameter specifies the behavior to adopt when the referenced object is deleted. This
    # is not specific to Django; it is a SQL standard. Using CASCADE, you specify that when the referenced
    # user is deleted, the database will also delete all related blog posts. You can take a look at all the possible
    # options at https://docs.djangoproject.com/en/5.0/ref/models/fields/#django.db.models.
    # ForeignKey.on_delete.
    # We use related_name to specify the name of the reverse relationship, from User to Post. This will
    # allow us to access related objects easily from a user object by using the user.blog_posts notation.
    # We will learn more about this later.
    # Django comes with different types of fields that you can use to define your models. You can find all
    # field types at https://docs.djangoproject.com/en/5.0/ref/models/fields/.


    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    # or instead we can use database-generated default values
    #To use database-generated default values, we use the db_default attribute instead of default. In this
    # example, we use the Now database function. It serves a similar purpose to default=timezone.now, but
    # instead of a Python-generated datetime, it uses the NOW() database function to produce the initial value.
    # You can read more about the db_default attribute at https://docs.djangoproject.com/en/5.0/ref/
    # models/fields/#django.db.models.Field.db_default. You can find all available database functions
    # at https://docs.djangoproject.com/en/5.0/ref/models/database-functions/.
    #      
    #       from django.db.models.functions import Now  
    #       publish = models.DateTimeField(db_default= Now())
    
  
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # created: This is a DateTimeField field. We will use it to store the date and time when the post
    # was created. By using auto_now_add, the date will be saved automatically when creating an
    # object.
    # updated: This is a DateTimeField field. We will use it to store the last date and time when the
    # post was updated. By using auto_now, the date will be updated automatically when saving an
    # object.
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
    )
    # added a new status field to the model that is an instance of CharField. It includes a
    # choices parameter to limit the value of the field to the choices in Status. We have also set a default
    # value for the field using the default parameter. We use DRAFT as the default choice for this field
        
    class Meta():
        ordering = ['-publish']  
        # added a Meta class inside the model. This class defines metadata for the model. We use the
    # ordering attribute to tell Django that it should sort results by the publish field. This ordering will
    # apply by default for database queries when no specific order is provided in the query. We indicate
    # descending order by using a hyphen before the field name, -publish. Posts will be returned in reverse
    # chronological order by default.
        indexes = [
            models.Index(fields=['-publish']),
            ]
    #added the indexes option to the model’s Meta class. 
    # This option allows you to define database
    # indexes for your model, which could comprise one or multiple fields, in ascending or descending order,
    # or functional expressions and database functions.


    def __str__(self):
        return self.title