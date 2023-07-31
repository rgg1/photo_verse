from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile
from PIL import Image
from io import BytesIO
from django.core.files import File

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username').lower()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("That email is already in use.")
        return email

class LoginForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username').lower()
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

class UserSearchForm(forms.Form):
    username = forms.CharField(label='Search for user profiles')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['display_name', 'bio', 'profile_picture', 'timezone']

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture', False)
        if profile_picture:
            profile_picture = self.make_square_image(profile_picture)
        return profile_picture

    def make_square_image(self, img):
        im = Image.open(img)
        width, height = im.size
        if width != height:
            min_side = min(width, height)
            offsets = (0, 0)
            if width < height:
                offsets = (0, (height - min_side) // 2)
            else:
                offsets = ((width - min_side) // 2, 0)

            im = im.crop((offsets[0], offsets[1], offsets[0] + min_side, offsets[1] + min_side))

        output = BytesIO()

        if im.mode not in ["RGB"]:
            im = im.convert("RGB")

        if im.format in ['JPEG', 'PNG', 'JPG', 'jpeg', 'png', 'jpg']:
            im.save(output, format=im.format)
        else:
            # Fallback to JPEG if the format is not recognized
            im.save(output, format='JPEG')

        output.seek(0)
        img = File(output, img.name)

        return img