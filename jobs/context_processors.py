from .models import SavedSearch
from .views import new_matches

# counts new saved search matches for the navbar
def saved_search_alerts(request):
    if not request.user.is_authenticated or not request.user.is_recruiter:
        return {}
    total = 0
    for saved_search in SavedSearch.objects.filter(recruiter=request.user):
        total += new_matches(saved_search).count()
    return {'new_match_count': total}
