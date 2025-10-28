from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Performance(models.Model):
    REVIEW_PERIOD_CHOICES = [
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Half Yearly', 'Half Yearly'),
        ('Annual', 'Annual'),
    ]

    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='performance_reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conducted_reviews')
    review_period = models.CharField(max_length=20, choices=REVIEW_PERIOD_CHOICES)
    review_date = models.DateField()
    
    # Rating fields (1-5 scale)
    technical_skills = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    communication_skills = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    teamwork = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    leadership = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    problem_solving = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    punctuality = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    overall_rating = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    strengths = models.TextField()
    areas_for_improvement = models.TextField()
    goals_for_next_period = models.TextField()
    feedback = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'performance'
        ordering = ['-review_date']

    def __str__(self):
        return f"{self.employee.full_name} - {self.review_period} Review ({self.review_date})"

    def save(self, *args, **kwargs):
        # Calculate overall rating as average of individual ratings
        ratings = [
            self.technical_skills,
            self.communication_skills,
            self.teamwork,
            self.leadership,
            self.problem_solving,
            self.punctuality
        ]
        self.overall_rating = sum(ratings) / len(ratings)
        super().save(*args, **kwargs)
