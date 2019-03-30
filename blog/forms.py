from django import forms
from .models import Blog, Comment
from ckeditor.widgets import CKEditorWidget

banned_email_liste = ['ahmet@gmail.com','deneme@gmail.com']


class IletisimForm(forms.Form):
    Isim = forms.CharField(widget=forms.TextInput(attrs={'clas:':'form-control'}), max_length=50,label='İsim',required=False)
    soyisim=forms.CharField(max_length=50,label='Soyisim',required=False)
    email=forms.EmailField(max_length=50,label='Email',required=True)
    email2=forms.EmailField(max_length=50,label='Email Kontrol',required=True)
    icerik=forms.CharField(max_length=1000,label='İçerik',required=True)

    def __init__(self, *args, **kwargs):
        super(IletisimForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs={'class': 'form-control'}
        self.fields['icerik'].widget = forms.Textarea(attrs={'class': 'form-control'})

    def clean_Isim(self):
        isim = self.cleaned_data.get('Isim')
        if isim == 'ahmet' :
            raise forms.ValidationError('Lütfen Ahmet Dışında Bir Kullanıcı Giriniz.')
        return isim

    def clean_email(self):
        email=self.cleaned_data.get('email')
        if email in banned_email_liste:
            raise forms.ValidationError('Lütfen Geçerli Bir Mail Adresi Giriniz. ')
        return email

    def clean(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')

        if email != email2:
            self.add_error('email','Emailler Eşleşmedi.')
            self.add_error('email2', 'Emailler Eşleşmedi.')
            raise forms.ValidationError('Emailler Eşleşmedi')


class BlogForm(forms.ModelForm):
    icerik = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Blog
        fields = ['title','image', 'icerik', 'yayin_taslak', 'kategoriler']

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs= {'class': 'form-control'}
        self.fields['icerik'].widget.attrs['rows']=10

    def clean_icerik(self):
        icerik = self.cleaned_data.get('icerik')
        if len(icerik) < 250:
            uzunluk = len(icerik)
            msg = 'Lütfen en az 250 karakter giriniz girilen karakter sayısı (%s)' % (uzunluk)
            raise forms.ValidationError(msg)
        return icerik


class PostSorguForm(forms.Form):
    YAYIN_TASLAK = (('all', 'Hepsi'),('yayin', 'YaYIN'), ('taslak', 'TASLAK'))

    search = forms.CharField(required=False, max_length=500, widget=forms.TextInput(attrs={'placeholder': 'ARA', 'class': 'form-control'}))
    taslak_yayin = forms.ChoiceField(label='',widget=forms.Select(attrs={'class': 'form-control'}), choices=YAYIN_TASLAK, required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields=['icerik']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}