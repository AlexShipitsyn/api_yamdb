from rest_framework import filters, mixins, viewsets


class CategoryGenreBaseViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'slug']