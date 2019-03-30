from django.db import models
from django.shortcuts import reverse
from unidecode import unidecode
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from uuid import uuid4
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify, safe
import os
from ckeditor.fields import RichTextField


def upload_to(instance, filename):
    uzanti = filename.split('.')[-1]
    new_name = "%s.%s" % (str(uuid4()), uzanti)
    unique_id = instance.unique_id
    return os.path.join('blog', unique_id, new_name)


class Kategori(models.Model):
    isim = models.CharField(max_length=10, verbose_name='Kategori İsim')

    class Meta:
        verbose_name_plural = 'Kategoriler'

    def __str__(self):
        return self.isim


class Blog(models.Model):
    YAYIN_TASLAK = ((None, 'Lütfen Birini Seçiniz'), ('yayin', 'YaYIN'), ('taslak', 'TASLAK'))
    user = models.ForeignKey(User, default=1, null=True, verbose_name='User',on_delete=models.DO_NOTHING,related_name='blog')
    title = models.CharField(max_length=100, blank=False, null=True, verbose_name='Baslik Giriniz.',
                             help_text='Baslik Bilgisi Burada Girilir.')
    icerik = RichTextField(null=True, blank=False, max_length=5000, verbose_name='İçerik')
    created_date = models.DateField(auto_now_add=True, auto_now=False)
    slug = models.SlugField(null=True, unique=True, editable=False)
    kategoriler = models.ManyToManyField(to=Kategori, related_name='blog', blank=True)
    image = models.ImageField(default='default/default-photo.jpg', verbose_name='Resim', null=True,
                              help_text='Kapak Fotoğrafı Yükleyiniz', upload_to=upload_to, blank=True)
    unique_id = models.CharField(max_length=100, editable=False, null=True)
    yayin_taslak = models.CharField(choices=YAYIN_TASLAK, max_length=6, blank=False, null=True)

    class Meta:
        verbose_name_plural = 'Gönderiler'
        ordering = ['-id']

    def __str__(self):
        return " %s %s " % (self.title, self.user)

    def get_added_favorite_user(self):
       return self.favorite_blog.values_list('user__username', flat=True)

    def get_added_favorite_user_as_object(self):
       data_list = []
       qs = self.favorite_blog.all()
       for obj in qs:
            data_list.append(obj.user)
            return data_list

    def get_comment_count(self):
        yorum_sayisi = self.comment.count()
        if yorum_sayisi > 0:
            return yorum_sayisi
        return "Henüz yorum yok."

    def get_favorite_count(self):
        favori_sayisi = self.favorite_blog.count()
        return favori_sayisi

    @classmethod
    def get_taslak_or_yayin(cls, taslak_yayin):
        return cls.objects.filter(yayin_taslak=taslak_yayin)

    def get_yayin_taslak_html(self):
        if self.yayin_taslak == 'taslak':
            return safe('<span style="vertical-align:text-top;font-size:15px" class="label label-{1}">{0}</span>'.format(self.get_yayin_taslak_display(), 'danger'))
        return safe('<span style="vertical-align:text-top;font-size:15px" class="label label-{1}">{0}</span>'.format(self.get_yayin_taslak_display(), 'primary'))

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return '/media/default/default-photo.jpg'

    def get_blog_comment(self):
        #gönderiye ait tüm yorumları bana veren fonksiyon
        return self.comment.all()

    def get_blog_comment_count(self):
        return len(self.get_blog_new_comment())

    def get_blog_new_comment(self):
        content_type = ContentType.objects.get_for_model(self)
        object_id = self.id
        all_comment = NewComment.objects.filter(content_type=content_type, object_id=object_id)
        return all_comment

    def get_unique_slug(self):
        sayi = 0
        slug = slugify(unidecode(self.title))
        new_slug = slug
        while Blog.objects.filter(slug=new_slug).exists():
            sayi += 1
            new_slug = "%s-%s" % (slug, sayi)

        slug = new_slug
        return slug

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.id is None:
            new_unique_id = str(uuid4())
            self.unique_id = new_unique_id
            self.slug = self.get_unique_slug()
        else:
            blog = Blog.objects.get(slug=self.slug)
            if blog.title != self.title:
                self.slug = self.get_unique_slug()

        super(Blog, self).save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(User,null=True,default=1,related_name='comment', on_delete=models.DO_NOTHING)
    blog = models.ForeignKey(Blog, null=True,on_delete=models.DO_NOTHING, related_name='comment')
   # comment = models.ForeignKey(to='self', null=True)
    comment_date = models.DateTimeField(auto_now_add=True,null=True)
    icerik = models.TextField(verbose_name='Yorum', max_length=1000, blank=False, null=True)

    class Meta:
        verbose_name_plural = 'Yorumlar'

    def __str__(self):
        return "%s %s" % (self.user, self.blog)

    def get_screen_name(self):
        if self.user.first_name:
            return "%s " % (self.user.get_full_name())
        return self.user.username


class FavoriteBlog(models.Model):
    user = models.ForeignKey(User, null=True, default=1, related_name='favorite_blog', on_delete=models.DO_NOTHING)
    blog = models.ForeignKey(Blog, null=True, on_delete=models.DO_NOTHING, related_name='favorite_blog')

    class Meta:
        verbose_name_plural = 'Favorilere Eklenen Gönderiler'

    def __str__(self):
        return "%s %s" % (self.user, self.blog)


class NewComment(models.Model):
    user = models.ForeignKey(User, null=True, default=1, related_name='+',on_delete=models.DO_NOTHING)
    is_parent = models.BooleanField(default=False)

    content_type = models.ForeignKey(to=ContentType, null=True,on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    icerik = models.TextField(verbose_name='Yorum', max_length=1000, blank=False, null=True)
    comment_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        username = self.user.username
        text = "{0} {1}".format(username,self.content_type.model)
        return text

    class Meta:
        verbose_name_plural = "İç içe yorum sistemi"

    @classmethod
    def add_comment(cls,model_type,user,icerik,nesne):
        content_type = ContentType.objects.get_for_model(nesne.__class__)
        cls.objects.create(user=user, icerik=icerik, content_type=content_type, object_id=nesne.pk)
        if model_type == 'comment':
            nesne.is_parent = True
            nesne.save()

    def get_child_comment(self):
        if self.is_parent:
            content_type = ContentType.objects.get_for_model(self.__class__)
            all_child_comment = NewComment.objects.filter(content_type=content_type,object_id=self.pk)
            return all_child_comment
        return None
