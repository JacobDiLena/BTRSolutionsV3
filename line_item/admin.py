from django.contrib import admin
from .models import Income,FixedExpense,VariableExpense,Spending
# Register your models here.

'''class CommentInline(admin.TabularInline):
    model=Comment
    extra=0

class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]
'''


admin.site.register(Income)
admin.site.register(FixedExpense)
admin.site.register(VariableExpense)
admin.site.register(Spending)
