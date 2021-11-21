from django.views.generic import ListView
from store.utils import DataMixin
from store.models import Woman

# Create your views here.


class Home_page(DataMixin, ListView):

    """class for depicting all news, start page"""

    model = Woman
    template_name = "store/home.html"
    context_object_name = "posts"

    # to add some list to our page

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)  # like dynamic list
        c_def = self.get_user_context(
            title="Home",
        )
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):

        return Woman.objects.filter(is_published=True)
        # to find only those element we need
