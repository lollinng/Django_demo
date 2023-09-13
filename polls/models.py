from django.db import models

import datetime

from django.utils import timezone
from django.contrib import admin


# Create your models here.

class Question(models.Model):
    
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    # This method defines how an instance of the Question model s
    # hould be displayed as a string. In this case, it displays 
    # the question_text.
    def __str__(self):
        return self.question_text
    

    """
    This method checks whether the question was published recently by
    comparing the pub_date field with the current time (using timezone.now()) 
    and a time delta of 1 day. If the pub_date is within the last day, 
    it returns True, indicating that the question was published recently; 
    otherwise, it returns False.
    """
    # This hyperparams are used for display Question in admin
    @admin.display(
        boolean = True,
        ordering = "pub_date",
        description = "Published recently"
    )
    def was_published_recently(self):
        now = timezone.now() 
      
        # bug caught using testcase
        # return self.pub_date >= now - datetime.timedelta(days=1)

        # Future bug solved for future dates
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    


class Choice(models.Model):

    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    # A ForeignKey field that establishes a relationship with the Question model.
    # This field indicates that each choice is associated with a particular question.

    question = models.ForeignKey(
        Question,
        # on_delete parameter specifies that if a related question is deleted, all its related choices should be deleted as well.
        on_delete=models.CASCADE
    )   


    # This method defines how an instance of the Choice model should be displayed as a string. In this case, it displays the choice_text.

    def __str__(self):
        return self.choice_text

   
