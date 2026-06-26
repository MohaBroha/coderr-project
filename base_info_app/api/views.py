from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Avg

from reviews_app.models import Review
from profile_app.models import Profile
from offers_app.models import Offer


class BaseInfoView(APIView):
    """
    API view for retrieving aggregated platform statistics.
    """

    def get(self, request):
        """
        Return general platform statistics.
        """
        return Response(
            {
                "review_count": Review.objects.count(),
                "average_rating": round(
                    Review.objects.aggregate(Avg("rating"))["rating__avg"] or 0,
                    1,
                ),
                "business_profile_count": Profile.objects.filter(
                    type="business"
                ).count(),
                "offer_count": Offer.objects.count(),
            }
        )
