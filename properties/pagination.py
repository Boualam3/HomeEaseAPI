from rest_framework.pagination import PageNumberPagination

# custom pagination instead of one pagination for everything
# we need to add more for other viewset


class DefaultPagination(PageNumberPagination):
    page_size = 10
