from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post, BlogComment
from django.contrib import messages
from blog.templatetags import extras

# Create your views here.
def bloghome(request):
    allposts=Post.objects.all()
    context={'allposts':allposts}
    return render(request, 'blog/bloghome.html', context)
    # return HttpResponse('     aall   blog this is bloghome page')

def blogpost(request, slug):
    post=Post.objects.filter(slug=slug).first()
    post.views=post.views + 1
    post.save()

    comments=BlogComment.objects.filter(post=post, parent=None)
    replies=BlogComment.objects.filter(post=post).exclude(parent=None)
    replydict={}
    for reply in replies:
        if reply.parent.sno not in replydict.keys():
            replydict[reply.parent.sno]=[reply]
        else:
            replydict[reply.parent.sno].append(reply)


    # print(replydict)
    # print(comments, replies)
    context={'post':post, 'comments':comments, 'user':request.user, 'replydict':replydict}
    # print(request.user)
    return render(request, 'blog/blogpost.html', context)
    # return HttpResponse(f'this is blogpost page {slug}')

def postcomment(request):
    if request.method=="POST":
        comment=request.POST.get("comment")
        user=request.user
        postsno=request.POST.get("postsno")
        post=Post.objects.get(sno=postsno)
        parentsno=request.POST.get("parentsno")
        if parentsno=="":
            comment=BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "your comment has been send successfully !")
        else:
            parent=BlogComment.objects.get(sno=parentsno)
            comment=BlogComment(comment=comment, user=user, post=post,parent=parent)
            comment.save()
            messages.success(request, "your reply has been send successfully !")

    return redirect(f"/blog/{post.slug}")