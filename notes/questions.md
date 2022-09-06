# Questions

1. why do functions in views.py need a request parameter in its definition?
    ```python3
    def index(request):
        return HttpResponse("yo.")
    ```
2. why does django have you add apps with a dot syntax?
    - ['polls.apps.PollsConfig'](https://docs.djangoproject.com/en/4.0/intro/tutorial02/)
    - 

    
3. how does the django API get `q.choice_set.all()`?
    - `q = Question.objects.get(pk=1)`
    - <Question: What's up?>
    - `q.choice_set.all()`
        ```python3
        import datetime
        
        from django.db import models
        from django.utils import timezone
        
        class Question(models.Model):
            question_text = models.CharField(max_length=200)
            pub_date = models.DateTimeField('date published')
            
            def was_published_recently(self):
                return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
            
            def __str__(self):
                return self.question_text
        
        class Choice(models.Model):
            question = models.ForeignKey(Question, on_delete=models.CASCADE)
            choice_text = models.CharField(max_length=200)
            votes = models.IntegerField(default=0)
            
            def __str__(self):
                return self.choice_text
        ```
    
[index](index.md)
