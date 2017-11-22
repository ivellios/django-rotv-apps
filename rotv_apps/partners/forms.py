from django import forms

from .models import MediaPatronage


try:
    from material import Layout, Row, Fieldset
    USE_MATERIAL = True
except ImportError:
    USE_MATERIAL = False


class MediaPatronageForm(forms.ModelForm):
    class Meta:
        model = MediaPatronage
        fields = ('name', 'city', 'spot', 'start', 'end', 'url', 'contact_email',
                  'additional_notes',
                  'logo', 'banner_image', 'cover_image', 'small_image',)

    def __init__(self, *args, **kwargs):
        super(MediaPatronageForm, self).__init__(*args, **kwargs)
        self.fields['logo'].required = True
        self.fields['banner_image'].required = True

        if USE_MATERIAL:
            self.layout = Layout('name',
                                 Row('city', 'spot'),
                                 Row('url', 'contact_email'),
                                 Row('start', 'end'),
                                 Fieldset(u'Grafiki wydarzenia',
                                          Row('logo', 'banner_image'),
                                          Row('cover_image', 'small_image')),
                                 'additional_notes', )
