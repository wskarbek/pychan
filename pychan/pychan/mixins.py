from boards.models import Board

class ChanCoreView(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        boards = Board.objects.all()
        context["board_list"] = boards.values_list('short', flat=True)
        if 'short' in self.kwargs:
            context["board"] = Board.objects.get(short=self.kwargs['short'])
        return context