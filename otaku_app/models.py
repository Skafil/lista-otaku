from django.db import models
from django.contrib.auth.models import User

# Wszystkie modele posiadają nazwę modelu oraz status.
NA_BIEZACO = 'Na bieżąco'
W_TRAKCIE = "W trakcie"
PORZUCONE = "Porzucone"
SKONCZONE = "Skończone"
PLANOWANE = "Planowane"
WSTRZYMANE = "Wstrzymane"

CHOICES = (
    (NA_BIEZACO, "Na bieżąco"),
    (W_TRAKCIE, "W trakacie"),
    (PORZUCONE, "Porzucone"),
    (SKONCZONE, "Skończone"),
    (PLANOWANE, "Planowane"),
    (WSTRZYMANE, "Wstrzymane"),
)

class Title(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=CHOICES)

    class Meta:
        verbose_name_plural = "Titles"
    
    def __str__(self):
        """Zwraca reprezentację modelu w postaci ciągu tekstowego."""
        return self.name

class Category(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, null=True, 
        blank=True)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=CHOICES)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        """Zwraca reprezentację modelu w postaci ciągu tekstowego."""
        return self.name

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True,
        blank=True)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=CHOICES)
    
    class Meta:
        verbose_name_plural = "Subcategories"

    def __str__(self):
        """Zwraca reprezentację modelu w postaci ciągu tekstowego."""
        return self.name