import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

"""
a separate TestClass for each model or view
a separate test method for each set of conditions you want to test
test method names that describe their function
"""

#  to run use : python manage.py test polls
class QuestionModelsTests(TestCase):

    # check if published in future
    def test_was_published_recently_with_future_question(self):
        """
        was published_recently() returns False for questions whose pub_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    # check if published yesterday
    def test_was_published_recently_old_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)
    
    # checking if published today
    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() return True for questions whose pub_date is within last day
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59,seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(),True)


# used to take some repetition out of the process of creating questions.
def create_question(question_text,days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)

class QuestionIndexViewTests(TestCase):
    
    # doesn’t create any questions, but checks the message: “No polls are available.” and verifies the latest_question_list is empty.
    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No polls are available")
        
        # check if the list is null for no questions
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
       
    
    # we create a question and verify that it appears in the list.
    def test_past_question(self):
        """Question with a pub_date in the past are displayed on the insdex page"""
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [question],
        )
    
    # we create a question with a pub_date in the future. The database is reset for each test method, 
    # so the first question is no longer there, and so again the index shouldn’t have any questions in it.
    def test_future_question(self):
        """Questions with a pub_date in the future aren't displayed on"""
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """Evend if both past and future questions exist, only past questions are displayed"""
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """The qustions index page may display multiple questions"""
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )

class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text
        """
        past_question = create_question(question_text="Past Question.",days=-5)
        url = reverse("polls:detail",args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response,past_question.question_text)