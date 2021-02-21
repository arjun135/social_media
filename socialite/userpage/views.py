from django.contrib import messages
from django.contrib.auth.models import User

from django.shortcuts import HttpResponse, redirect, render

from .models import Like, Post, Profile,Following
from django.conf import settings
import json
from django.views.generic import ListView



def userhome(request):
    #fetching post from database
    
    user=Following.objects.get(user=request.user) # following_obj of user
    followed_user=[i for i in user.followed.all()]
    followed_user.append(request.user)

    posts=Post.objects.filter(user__in=followed_user).order_by('-pk')
    # liked_post=Like.objects.filter(user=request.user)  
    # liked_posts=[i.post for i in liked_post]
    
    # liked_post=[]
    # for i in posts:
        # is_liked=Like.objects.filter(post=i,user=request.user)
        # if is_liked:
            # liked_post.append(i)

    liked_=[i for i in posts if Like.objects.filter(post=i,user=request.user)]
    # print(liked_post)
    # print(liked_) 

    data={
        'posts':posts,
        'liked_post':liked_
        }       

    return render(request,'userpage/postfeed.html',data)

def post(request):
    if request.method=='POST':
        image_=request.FILES['image']
        caption_=request.POST.get('caption','')
        user_=request.user
        # print(caption_,user_,end='\n')
        post_obj=Post(user=user_,caption=caption_,image=image_)

        post_obj.save()
        messages.success(request,'we showed !!!')
        return redirect('/userpage')

    else:
        messages.error(request,'something went wrong!!')
        return redirect('/userpage')        

def delPost(request,postId):
    # every post have a unique identity
    post_=Post.objects.filter(pk=postId)
    image_path=post_[0].image.url    #image location in system
    post_.delete()
    messages.info(request,'post deleted successfully')


    # print(post_)
    # print(post_[0].image.url)
    return redirect('/userpage') 

def userProfile(request,username):
    user=User.objects.filter(username=username)   # if exist then return a list
    if user:
        user=user[0]
        profile=Profile.objects.get(user=user)  # did not return list
        post=getPost(user)
        bio=profile.bio
        conn=profile.connection
        user_img=profile.image
        
        is_following=Following.objects.filter(user=request.user,followed=user)
        
        following_obj=Following.objects.get(user=user)
        
        follower,following=following_obj.follower.count(),following_obj.followed.count()

        data={
            'user_obj':user,
            'bio':bio,
            'conn':conn,
            'userImg':user_img,
            'posts':post,
            'follower':follower,
            'following':following,
            'connection':is_following,
        }
    else:
        return HttpResponse('no such user')    
    return render(request,"userpage/userProfile.html",data)

def getPost(user):
    post_obj=Post.objects.filter(user=user)
    imgList=[
        post_obj[i:i+3] for i in range(0,len(post_obj),3)
    ]
    return imgList

def likePost(request):
    post_id=request.GET.get("likeId", "")  # key
    post=Post.objects.get(pk=post_id)
    user=request.user          # current user
    like=Like.objects.filter(post=post,user=user)
    liked=False
    
    if like:
        Like.dislike(post,user)
    else:
        liked=True
        Like.like(post,user)
    
    resp={
        'liked':liked
    }
    response=json.dumps(resp)
    return HttpResponse(response,content_type="application/json")
    # print(id)

def comment(request):
    comment_=request.GET.get('comment','')
    print(comment_)
    return render(request,'userpage/comment.html')

def follow(request,username):
    main_user=request.user
    to_follow=User.objects.get(username=username)

    #check if aleready follwing

    following=Following.objects.filter(user=main_user,followed=to_follow)
    is_following=True if following else False

    if is_following:
        Following.unfollow(main_user,to_follow)
        is_following=False


    else:
        Following.follow(main_user,to_follow)
        is_following=True    
   

    resp={
        'following':is_following,

    }
    response=json.dumps(resp)
    return HttpResponse(response,content_type="application/json")


class Search_User(ListView):
    model=User
    template_name="userpage/search_user.html"
    paginate_by=2
    
    def get_queryset(self):
        username=self.request.GET.get('username','')
        print("edfe ")
        queryset=User.objects.filter(username__icontains=username)  #icontains me case unsensitive he username ke mid me se be search karega

        return queryset



