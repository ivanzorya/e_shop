import logging

from django.conf import settings
from django.utils import timezone
from django.utils.html import escape

from .loader import get_revison

logger = logging.getLogger(settings.DEBUG_LOGGER)


class RevisionMiddleware:
    """
    Middleware component which will modify every response to include the header
    with the source revision (last commit id) information
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        source_revision = get_revison()

        if source_revision:
            response["X-Source-Revision"] = source_revision

        return response


class LogRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        logger.info(f"{timezone.now()} -> {escape(request.path)} {response.status_code}")
        return response
