from django import forms
from .models import Post, Comment
from PIL import Image
from io import BytesIO
from django.core.files import File

class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'image']

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image:
                image = self.make_square_image(image)
        return image

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

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']