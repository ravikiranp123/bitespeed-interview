from django.db import models

# Create your models here.
class User(models.Model):
#     {
# 	id                   Int                   
#   phoneNumber          String?
#   email                String?
#   linkedId             Int? // the ID of another Contact linked to this one
#   linkPrecedence       "secondary"|"primary" // "primary" if it's the first Contact in the link
#   createdAt            DateTime              
#   updatedAt            DateTime              
#   deletedAt            DateTime?
# }
    class LinkPrecedenceChoices(models.TextChoices):
        primary = 'primary'
        secondary = 'secondary'
    
    # id = models.UUIDField()
    phoneNumber = models.CharField(max_length=15)
    email = models.CharField(max_length=45)
    linkedId = models.ForeignKey('self', on_delete=models.CASCADE, default=None, blank=True, null=True)
    linkPrecedence = models.CharField(max_length=30, choices=LinkPrecedenceChoices.choices)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(default=None, blank=True, null=True)
    
    def __str__(self) -> str:
        return f"id: {self.id}; email: {self.email}; phoneNumber: {self.phoneNumber}"