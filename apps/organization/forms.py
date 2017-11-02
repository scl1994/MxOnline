import re

from django import forms

from operation.models import UserAsk


# 不再继承普通form，使用modelform直接从数据库模型转换成form（两者的相似度极高）
class UserAskForm(forms.ModelForm):
    class Meta:
        # 指明由那个模型生成form
        model = UserAsk
        # 指明要生成那些字段
        fields = ['name', 'mobile', 'course_name']

    # 定义一个验证函数，要以clean开头，来验证mobile字段是否为电话号
    def clean_mobile(self):
        """验证手机号码是否合法"""
        mobile = self.cleaned_data['mobile']
        RE_MOBILE = r"^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(RE_MOBILE)
        if p.match(mobile):
            # 验证成功，返回号码
            return mobile
        else:
            # 验证失败，抛出异常，会在实例化UserAskForm后调用is_valid时包含在他的_errors中
            raise forms.ValidationError("手机号码错误", code="mobile_valid")
