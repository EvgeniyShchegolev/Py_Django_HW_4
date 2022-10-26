from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError
from .models import Article, Tag, Scope


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    pass


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        try:
            tags = []
            count_main_tag = 0
            for form in self.forms:

                if form.cleaned_data["is_main"]:
                    count_main_tag += 1
                if count_main_tag > 1:
                    raise ValidationError('Основной тэг выставлен более одного раза!')

                if form.cleaned_data['tag'].name in tags:
                    raise ValidationError('Есть повторяющиеся тэги!')
                else:
                    tags.append(form.cleaned_data['tag'].name)

            if count_main_tag == 0:
                raise ValidationError('Основной тэг не выставлен!')

        except KeyError:
            raise ValidationError('Тэги не выставлены!')

        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Article.tags.through
    formset = ScopeInlineFormset
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'text', 'published_at', 'image']
    list_filter = ['title', 'published_at']
    inlines = [ScopeInline, ]
