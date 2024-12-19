from .recommendations import JobRecommender


class RecommendationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            request.recommended_jobs = JobRecommender.get_recommendations(
                request.user)

        return response
