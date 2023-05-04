from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from .utils import get_countries

def GetCurrentHostapdSettings(field):
    try:
        with open('/etc/hostapd/hostapd.conf','r') as f:
            for line in f.readlines():
                if len(line)==0 or line[0]=='#':
                    continue
                t=line.split('=')
                if len(t)<1:
                    continue
                if t[0]==field:
                    if len(t)==1:
                        return ""
                    else:
                        return t[1]
    except:
        pass
    return ""


def GetStaticIpAddress():
    try:
        with open('/etc/dhcpcd.conf', 'r') as f:
            for line in f.readlines():
                if len(line)==0 or line[0]=='#':
                    continue
                if 'static ip_address' in line:
                    t = line.split("=")
                    if len(t)<2:
                        return ""
                    else:
                        return t[1]
    except:
        pass
    return ""

def GetDHCPSettings(field, fid=-1):
    try:
        with open('/etc/dnsmasq.d/p4pi.conf','r') as f:
            for line in f.readlines():
                if len(line)==0 or line[0]=='#':
                    continue
                t=line.split('=')
                if len(t)<1:
                    continue
                if t[0]==field:
                    if len(t)==1:
                        return ""
                    else:
                        if fid!=-1:
                            subt = t[1].split(',')
                            if len(subt)<=fid:
                                return ""
                            else:
                                return subt[fid]
                        else:
                            return t[1]
    except:
        pass
    return ""



class AccessPointSettingsForm(forms.Form):
    ssid = forms.CharField(
        label='Service Set Identifier (SSID)',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'P4Pi',
                'value' : GetCurrentHostapdSettings("ssid"),
                'class': 'form-control'
            }
        ),
        max_length=60
    )
    passphrase = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'raspberry',
                'value' : GetCurrentHostapdSettings("wpa_passphrase"),
                'class': 'form-control',
            }
        ),
        label="Password"
    )
    channel = forms.DecimalField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '7',
                'value' : GetCurrentHostapdSettings("channel"),
                'class': 'form-control',
            }
        ),
        label="Channel",
        min_value=1,
        max_value=14
    )
    country_code = forms.ChoiceField(
        label='Country Code',
        choices=get_countries(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    static_ip_address = forms.CharField(
        label='Static IP Address',
        widget=forms.TextInput(
            attrs={
                'placeholder': '192.168.4.1/24',
                'value' : GetStaticIpAddress(),
                'class': 'form-control'
            }
        ),
    )
    range_min = forms.CharField(
        label='DHCP Range Start Address',
        widget=forms.TextInput(
            attrs={
                'placeholder': '192.168.4.2',
                'value': GetDHCPSettings("dhcp-range",1),
                'class': 'form-control'
            }
        ),
    )
    range_max = forms.CharField(
        label='DHCP Range End Address',
        widget=forms.TextInput(
            attrs={
                'placeholder': '192.168.4.20',
                'value': GetDHCPSettings("dhcp-range",2),
                'class': 'form-control'
            }
        ),
    )
    lease = forms.CharField(
        label='DHCP Lease',
        widget=forms.TextInput(
            attrs={
                'placeholder': '24h',
                'value': GetDHCPSettings("dhcp-range",4),
                'class': 'form-control'
            }
        ),
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_action = 'password_change'
        self.helper.label_class = 'control-label'
        self.helper.field_class = 'mb-4'
        self.helper.add_input(
            Submit('submit', 'Change Password', css_class='mb-4 shadow-2')
        )

        self.base_fields['old_password'].widget.attrs['class'] = 'form-control'
        self.base_fields['old_password'].widget.attrs['class'] = 'form-control'
        self.base_fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.base_fields['new_password1'].help_text = ''
        self.base_fields['new_password2'].widget.attrs['class'] = 'form-control'
