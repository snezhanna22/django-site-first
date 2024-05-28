from goods.models import Products
from django.db.models import Q
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    SearchHeadline,
)


# функция поиск по сайту
def q_search(query):

    if query.isdigit() and len(query) <= 5:
        return Products.objects.filter(id=int(query))

    vector = SearchVector("name", "description")
    query = SearchQuery(query)

    resalt = (
        Products.objects.annotate(rank=SearchRank(vector, query))
        .filter(rank__gt=0)
        .order_by("-rank")
    )

    result = resalt.annotate(
        headline=SearchHeadline(
            "name",
            query,
            start_sel='<span style="backround-color: yellow;">',
            stop_sel="</span>",
        )
    )
    result = resalt.annotate(
        headline=SearchHeadline(
            "description",
            query,
            start_sel='<span style="backround-color: yellow;">',
            stop_sel="</span>",
        )
    )

    return resalt

    # keywords = [word for word in query.split() if len(word) > 2]

    # q_objects = Q()
    # for token in keywords:
    #     q_objects |= Q(description__icontains=token)
    #     q_objects |= Q(name__icontains=token)

    # return Products.objects.filter(q_objects)
