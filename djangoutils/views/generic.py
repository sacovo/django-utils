from django.views.generic import TemplateView, ListView, CreateView, UpdateView,\
                                 DeleteView, DetailView, ArchiveIndexView

app_specific = {}

class ExtraContext(object):
    extra = {}

    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)
        for key, value in self.extra.items():
            context[key] = value(context) if callable(value) else value
        for key, value in app_specific[self.extra['appname']].items():
            context[key] = value(context) if callable(value) else value
        return context

class ExtraArchiveIndexView(ExtraContext,ArchiveIndexView):
    pass


class ExtraDetailView(ExtraContext, DetailView):
    pass


class ExtraTemplateView(ExtraContext, TemplateView):
    pass


class ExtraListView(ExtraContext, ListView):
    pass


class ExtraCreateView(ExtraContext, CreateView):
    pass


class ExtraUpdateView(ExtraContext, UpdateView):
    pass

class ExtraDeleteView(ExtraContext, DeleteView):
    pass
