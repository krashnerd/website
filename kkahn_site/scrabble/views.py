from django.shortcuts import render
from django.http import HttpResponse


class Square():
    def __init__(self, bonustype = None):
        bonuses = dict({
            "DW": ("Double Word Score", "square-double-word"),
            "TW": ("Triple Word Score", "square-triple-word"),
            "DL": ("Double Letter Score", "square-double-letter"),
            "TL": ("Triple Letter Score", "square-triple-letter"),
            None: ("", "square"),
        })

        self.bonustext, self.type = bonuses.get(bonustype, ("", "square"))





def index(request):
    context = 

    return render(request, "scrabble/scrabble_view.html", context)
# Create your views here.
