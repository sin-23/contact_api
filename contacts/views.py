from rest_framework import viewsets
from django.db.models import Q
from .models import Contact
from .serializers import ContactSerializer

class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('q', None)
        if search_query:
            # Split the search string into words
            names = search_query.strip().split()
            if len(names) == 2:
                # When two names are provided, assume first and last name
                first, last = names
                queryset = queryset.filter(
                    Q(first_name__iexact=first, last_name__iexact=last) |
                    Q(first_name__icontains=search_query) |
                    Q(last_name__icontains=search_query)
                )
            else:
                # Otherwise, search in both first_name and last_name
                queryset = queryset.filter(
                    Q(first_name__icontains=search_query) |
                    Q(last_name__icontains=search_query)
                )
        return queryset
