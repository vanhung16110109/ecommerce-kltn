from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from apps.account.models import UserProfile
from django.forms.widgets import FileInput, Select, TextInput
User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Tài khoản đã tồn tại")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email khoản đã tồn tại")
        return email

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password2!=password:
            raise forms.ValidationError("Mật khẩu không trùng khớp")
        return data


CITY = [
    ('An Giang', 'An Giang'), ('Bà Rịa-Vũng Tàu', 'Bà Rịa-Vũng Tàu'), ('Bạc Liêu', 'Bạc Liêu'),
    ('Bắc Kạn', 'Bắc Kạn'), ('Bắc Giang', 'Bắc Giang'), ('Bắc Ninh', 'Bắc Ninh'),
    ('Bến Tre', 'Bến Tre'),('Bình Dương', 'Bình Dương'),('Bình Định', 'Bình Định'),
    ('Bình Phước', 'Bình Phước'),('Bình Thuận', 'Bình Thuận'),('Cà Mau', 'Cà Mau'),
    ('Cao Bằng', 'Cao Bằng'),('Cần Thơ (TP)', 'Cần Thơ (TP)'),('Đà Nẵng (TP)', 'Đà Nẵng (TP)'),
    ('Đắk Lắk', 'Đắk Lắk'),('Đắk Nông', 'Đắk Nông'),('Điện Biên','Điện Biên'),
    ('Đồng Nai','Đồng Nai'),('Đồng Tháp','Đồng Tháp'),('Gia Lai','Gia Lai'),
    ('Hà Giang', 'Hà Giang'),('Hà Nam', 'Hà Nam'),('Hà Nội (TP)', 'Hà Nội (TP)'),
    ('Hà Tây', 'Hà Tây'),('Hà Tĩnh','Hà Tĩnh'),('Hải Dương','Hải Dương'),
    ('Hải Phòng (TP)', 'Hải Phòng (TP)'),('Hòa Bình', 'Hòa Bình'),('Hồ Chí Minh (TP)', 'Hồ Chí Minh (TP)'),
    ('Hậu Giang', 'Hậu Giang'),('Hưng Yên', 'Hưng Yên'),('Khánh Hòa', 'Khánh Hòa'),
    ('Kiên Giang', 'Kiên Giang'),('Kon Tum', 'Kon Tum'),('Lai Châu', 'Lai Châu'),
    ('Lào Cai', 'Lào Cai'),('Lạng Sơn', 'Lạng Sơn'),('Lâm Đồng', 'Lâm Đồng'),
    ('Long An', 'Long An'),('Nam Định', 'Nam Định'),('Nghệ An', 'Nghệ An'),
    ('Ninh Bình', 'Ninh Bình'),('Ninh Thuận', 'Ninh Thuận'),('Phú Thọ', 'Phú Thọ'),
    ('Phú Yên', 'Phú Yên'),('Quảng Bình', 'Quảng Bình'),('Quảng Nam', 'Quảng Nam'),
    ('Quảng Ngãi', 'Quảng Ngãi'),('Quảng Ninh', 'Quảng Ninh'),('Quảng Trị', 'Quảng Trị'),
    ('Sóc Trăng', 'Sóc Trăng'),('Sơn La', 'Sơn La'),('Tây Ninh', 'Tây Ninh'),
    ('Thái Bình', 'Thái Bình'),('Thái Nguyên', 'Thái Nguyên'),('Thanh Hóa', 'Thanh Hóa'),
    ('Thừa Thiên – Huế', 'Thừa Thiên – Huế'),('Tiền Giang', 'Tiền Giang'),('Trà Vinh', 'Trà Vinh'),
    ('Tuyên Quang', 'Tuyên Quang'),('Vĩnh Long', 'Vĩnh Long'),('Vĩnh Phúc', 'Vĩnh Phúc'),
    ('Yên Bái', 'Yên Bái'),
]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('image', 'email', 'phone', 'address', 'city', 'country', )
        widgets = {
            'image': FileInput(attrs={'class':'input','placeholder':'Ảnh'}),
            'email': TextInput(attrs={'class':'input','placeholder':'Email'}),
            'phone': TextInput(attrs={'class':'input','placeholder':'Điện thoại'}),
            'address': TextInput(attrs={'class':'input','placeholder':'Địa chỉ'}),
            'city': Select(attrs={'class':'input','placeholder':'Thành phố/Tỉnh thành'}, choices=CITY),
            'country': TextInput(attrs={'class':'input','placeholder':'Quốc gia'}),
        }
        
