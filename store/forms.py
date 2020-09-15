from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from store.models import Customer, Category, Product, Supplier


class UserRegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username','password')


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

class  ProfileForm(ModelForm):
    class Meta:
        model = Customer
        fields = ('image', 'phone')

class SupplierForm(ModelForm):
    class Meta:
        model = Supplier
        fields = ('company',)

class addcategory(ModelForm):
    class Meta:
        model= Category
        fields= '__all__'

class productform(forms.ModelForm):
    Details = forms.CharField(widget=forms.Textarea)
    class Meta:
        model= Product
        fields = ('name','code', 'price', 'digital', 'discount','image','image_back_view','image_right_view','image_left_view')


class Register(ModelForm):
    class Meta:
        name= forms.CharField(max_length=10)
        model= User
        fields = "__all__"



class CreateUser(UserCreationForm):
    class Meta:
        model= User
        fields= ['first_name','last_name','email','username','password1','password2']