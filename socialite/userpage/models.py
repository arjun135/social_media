from django.db import models 
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    caption=models.CharField(max_length=200)
    image=models.ImageField(upload_to="user_image/Post") #optional
    date=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.user)+' '+str(self.date.date())


class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="Profiles",default="default/default.jpg") 
    bio=models.CharField(max_length=100)
    connection=models.CharField(max_length=100,blank=True)
    follower12=models.IntegerField(default=0)
    followings12=models.IntegerField(default=0)
  


    def __str__(self):
        return str(self.user)

class Like(models.Model):
    user=models.ManyToManyField(User,related_name='likeimguser')
    post=models.OneToOneField(Post,on_delete=models.CASCADE)
    likes=models.IntegerField(default=0)
# for liking post
    @classmethod
    def like(cls,post,liking_user):
        obj,create=cls.objects.get_or_create(post=post)
        obj.user.add(liking_user)
    
    # for disliking post
    @classmethod
    def dislike(cls,post,disliking_user):
        obj,create=cls.objects.get_or_create(post=post)
        obj.user.remove(disliking_user)


    def __str__(self):
        return str(self.post)    

class Following(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    followed=models.ManyToManyField(User,related_name="followed")
    follower=models.ManyToManyField(User,related_name="follower")
    
    @classmethod
    def follow(cls,user,another_account):
        obj,create=cls.objects.get_or_create(user=user)
        obj.followed.add(another_account)
    


    @classmethod
    def unfollow(cls,user,another_account):
        obj,create=cls.objects.get_or_create(user=user)
        obj.followed.remove(another_account)
        



    def __str__(self):
        return str(self.user)    





