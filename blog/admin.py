from django.contrib import admin
from .models import Blog, Kategori, Comment, FavoriteBlog, NewComment

admin.site.register(Blog)
admin.site.register(Kategori)
admin.site.register(Comment)
admin.site.register(FavoriteBlog)
admin.site.register(NewComment)

