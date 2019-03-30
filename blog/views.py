from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404, reverse, Http404
from django.contrib import messages
from django.http import  JsonResponse
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from .models import Blog, FavoriteBlog, NewComment
from .forms import IletisimForm, BlogForm, PostSorguForm, CommentForm
# Create your views here.
from django.db.models import Q
from fallowing.models import Fallowing
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
mesajlar = []


def iletisim(request):
    form = IletisimForm(data=request.GET or None)
    if form.is_valid():
        isim = form.cleaned_data.get('Isim')
        soyisim = form.cleaned_data.get('soyisim')
        email = form.cleaned_data.get('email')
        icerik = form.cleaned_data.get('icerik')
        data = {'isim': isim, 'soyisim': soyisim, 'email': email, 'icerik': icerik}
        mesajlar.append(data)
        return render(request, 'iletisim.html', context={'mesajlar': mesajlar, 'form': form})

    return render(request, 'iletisim.html', context={'form': form})

#@login_required(login_url=reverse('user_login'))
# @login_required(login_url='/auths/login/')
def posts_list(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_login'))
    posts = Blog.objects.all()
    page = request.GET.get('page', 1)
    form = PostSorguForm(data=request.GET or None)
    if form.is_valid():
        taslak_yayin = form.cleaned_data.get('taslak_yayin', None)
        search = form.cleaned_data.get('search', None)
        if search:
            posts = posts.filter(
                Q(icerik__icontains=search) | Q(title__icontains=search) | Q(
                    kategoriler__isim__icontains=search)).distinct()
        if taslak_yayin and taslak_yayin != 'all':
           # posts = Blog.get_taslak_or_yayin(taslak_yayin)
            posts = posts.filter(yayin_taslak=taslak_yayin)
    # if gelen_deger:
    #   posts = posts.filter(id = gelen_deger)
    paginator = Paginator(posts, 3)
    try:
        posts = paginator.page(page)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    except PageNotAnInteger:
        posts = paginator.page(1)

    context = {'posts': posts, 'form': form}
    return render(request, 'blog/post_list.html', context)


def post_update(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if request.user != blog.user:
        return HttpResponseForbidden()
    # instance() formu güncellemek için eski verileri formun içini doldurur.
    form = BlogForm(instance=blog, data=request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form.save()
        msg = "Tebrikler <strong>%s </strong> isimli gönderiniz başarıyla güncellendi." % (blog.title)
        messages.success(request, msg, extra_tags='info')
        return HttpResponseRedirect(blog.get_absolute_url())
    context = {'form': form, 'blog': blog}
    return render(request, 'blog/post_update.html', context=context)


def post_delete(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if request.user != blog.user:
        return HttpResponseForbidden()
    blog.delete()
    msg = " <strong>%s </strong> isimli gönderiniz silindi." % (blog.title)
    messages.success(request, msg, extra_tags='danger')
    return HttpResponseRedirect(reverse('post_list'))


def post_detail(request, slug):
    form = CommentForm()
    blog = get_object_or_404(Blog, slug=slug)
    return render(request, 'blog/post_detail.html', context={'blog': blog, 'form': form})


def add_comment(request, slug):
    if request.method == 'GET':
        return HttpResponseBadRequest()
    blog = get_object_or_404(Blog, slug=slug)
    form = CommentForm(data=request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.blog = blog
        new_comment.user = request.user
        new_comment.save()
        messages.success(request, 'Tebrikler Yorumunuz Başarıyla Oluşturuldu')
        return HttpResponseRedirect((blog.get_absolute_url()))


def post_create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_login'))
    form = BlogForm()
    if request.method == "POST":
        form = BlogForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        blog = form.save(commit=False)
        blog.user = request.user
        blog.save()
        msg = "Tebrikler <strong>%s </strong> isimli gönderiniz başarıyla oluşturuldu." % (blog.title)
        messages.success(request, msg, extra_tags='success')
        # reverse('post_detail', kwargs={'pk':blog.pk})
        return HttpResponseRedirect(blog.get_absolute_url())

    return render(request, 'blog/post_create.html', context={'form': form})


def add_or_remove_favorite(request, slug):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_login'))
    data = {'count':0,'status':'deleted'}
    blog = get_object_or_404(Blog, slug=slug)
    favori_blog = FavoriteBlog.objects.filter(blog=blog, user=request.user)
    if favori_blog.exists():
        favori_blog.delete()
    else:
        FavoriteBlog.objects.create(blog=blog, user=request.user)
        data.update({'status':'added'})

    count = blog.get_favorite_count()
    data.update({'count':count})

    return JsonResponse(data=data)


def post_list_favorite_user(request, slug):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_login'))
    page = request.GET.get('page', 1)
    blog = get_object_or_404(Blog, slug=slug)
    user_list = blog.get_added_favorite_user_as_object()
    paginator = Paginator(user_list, 1)
    try:
        user_list = paginator.page(page)
    except PageNotAnInteger:
        user_list = paginator.page(1)
    except EmptyPage:
        user_list = paginator.page(paginator.num_pages)
    my_fallowed_user = Fallowing.get_fallowed_username(request.user)
    html = render_to_string('blog/include/favorite/favorite-user-list.html', context={'my_fallowed_user':my_fallowed_user,'user_list':user_list},request=request)

    page_html = render_to_string('blog/include/favorite/buttons/show_more_button.html',
                                 context={'post':blog, 'user_list':user_list}, request=request)

    return JsonResponse(data={'html':html, 'page_html':page_html})


def new_add_comment(request, pk, model_type):
    data = {'is_valid':True, 'blog_comment_html':'','model_type':model_type}
    nesne = None
    all_comment = None
    form = CommentForm(data=request.POST)

    if model_type == 'blog':
        nesne = get_object_or_404(Blog, pk=pk)
    elif model_type == 'comment':
        nesne = get_object_or_404(NewComment,pk=pk)
    else:
        raise Http404

    if form.is_valid():
        icerik = form.cleaned_data.get('icerik')
        NewComment.add_comment(nesne,model_type,request.user,icerik)

    ##yorum ekranını güncelleyeceğimiz yer
    if model_type == 'comment':
       nesne = nesne.content_object  # burada gelen değer comment ise blogu almak için
            # tüm yorumlarını tekrardan çekiyoruz

       comment_html = render_to_string('blog/include/comment/comment-list-partial.html', context={
            'blog': nesne
        })
       data.update({'blog_comment_html': comment_html})

    return JsonResponse(data=data)


def get_child_comment_form(request):
    data = {'form_html':''}
    pk = request.GET.get('comment_pk')
    comment = get_object_or_404(NewComment, pk=pk)
    form = CommentForm()
    form_html = render_to_string('blog/include/comment/comment-child-comment-form.html', context={
        'form': form,
        'comment': comment
    },request=request)
    data.update({'form_html': form_html})
    return JsonResponse(data=data)


def sanatcilar(request, sayi):
    sanatcilar_sozluk = {
        '1': 'Eminem',
        '2': 'Tupack',
        '3': 'Tarkan',
        '4': 'Aleyna Tilki',
        '5': 'Müslüm Gürses',
        '6': 'Neşet Ertaş',
        '7': 'Teoman',
        '89': 'Metallica',
        'eminem': 'Without me'
    }
    sanatci = sanatcilar_sozluk.get(sayi, "Bu id adresine ait sanatci bulunmuyor")
    return HttpResponse(sanatci)
