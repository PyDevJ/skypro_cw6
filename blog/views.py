from django.views.generic import DetailView

from blog.models import Blog


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/detail_view.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_views += 1
        self.object.save()
        return self.object
