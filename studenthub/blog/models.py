from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    introduction = models.TextField(blank=True, null=True)
    main_content = models.TextField(blank=True, null=True)
    conclusion = models.TextField(blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='media/products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def like(self, user):
        product_like, created = ProductLike.objects.get_or_create(product=self, user=user)
        if created or not product_like.liked:
            product_like.liked = True
            product_like.save()
            self.likes = self.product_likes.filter(liked=True).count()
            self.dislikes = self.product_likes.filter(liked=False).count()
            self.save()

    def dislike(self, user):
        product_dislike, created = ProductLike.objects.get_or_create(product=self, user=user)
        if created or product_dislike.liked:
            product_dislike.liked = False
            product_dislike.save()
            self.likes = self.product_likes.filter(liked=True).count()
            self.dislikes = self.product_likes.filter(liked=False).count()
            self.save()

    def remove_like(self, user):
        try:
            product_like = ProductLike.objects.get(product=self, user=user)
            if product_like.liked:
                product_like.delete()
                self.likes = self.product_likes.filter(liked=True).count()
                self.save()
        except ProductLike.DoesNotExist:
            pass

    def remove_dislike(self, user):
        try:
            product_dislike = ProductLike.objects.get(product=self, user=user)
            if not product_dislike.liked:
                product_dislike.delete()
                self.dislikes = self.product_likes.filter(liked=False).count()
                self.save()
        except ProductLike.DoesNotExist:
            pass

    def short_description(self):
        words = self.description.split()
        if len(words) > 50:
            return ' '.join(words[:30]) + '...'
        else:
            return self.description

class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.product}'

class ProductLike(models.Model):
    product = models.ForeignKey(Product, related_name='product_likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_likes', on_delete=models.CASCADE)
    liked = models.BooleanField(default=True)
