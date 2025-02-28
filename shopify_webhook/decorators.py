import json
from functools import wraps

from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponse
from django.conf import settings

from .helpers import domain_is_valid, hmac_is_valid, proxy_signature_is_valid


class HttpResponseMethodNotAllowed(HttpResponse):
    status_code = 405

class HttpResponseUnauthorized(HttpResponse):
    status_code = 401


def webhook(f):
    """
    A view decorator that checks and validates a Shopify Webhook request.
    """

    @wraps(f)
    def wrapper(request, *args, **kwargs):
        # Ensure the request is a POST request.
        if request.method != 'POST':
            return HttpResponseMethodNotAllowed()
        
        # Try to get required headers and decode the body of the request.
        try:
            topic   = request.META['HTTP_X_SHOPIFY_TOPIC']
            domain  = request.META['HTTP_X_SHOPIFY_SHOP_DOMAIN']
            hmac    = request.META['HTTP_X_SHOPIFY_HMAC_SHA256'] if 'HTTP_X_SHOPIFY_HMAC_SHA256' in request.META else None
            webhook_id = request.META['HTTP_X_SHOPIFY_WEBHOOK_ID']
            triggered_at = request.META['HTTP_X_SHOPIFY_TRIGGERED_AT']
            data    = json.loads(request.body.decode('utf-8'))
        except (KeyError, ValueError) as e:
            return HttpResponseBadRequest()

        # Verify the domain.
        if not domain_is_valid(domain):
            return HttpResponseBadRequest()

        # Verify the HMAC.
        if not hmac_is_valid(request.body, settings.SHOPIFY_APP_API_SECRET, hmac):
            return HttpResponseUnauthorized()

        # Otherwise, set properties on the request object and return.
        request.webhook_topic        = topic
        request.webhook_data         = data
        request.webhook_domain       = domain
        request.webhook_id           = webhook_id
        request.webhook_triggered_at = triggered_at
        return f(request, *args, **kwargs)

    return wrapper


def carrier_request(f):
    """
    A view decorator that checks and validates a CarrierService request from Shopify.
    """

    @wraps(f)
    def wrapper(request, *args, **kwargs):
        # Ensure the request is a POST request.
        if request.method != 'POST':
            return HttpResponseMethodNotAllowed()

        # Try to get required headers and decode the body of the request.
        try:
            domain  = request.META['HTTP_X_SHOPIFY_SHOP_DOMAIN']
            hmac    = request.META['HTTP_X_SHOPIFY_HMAC_SHA256'] if 'HTTP_X_SHOPIFY_HMAC_SHA256' in request.META else None
            data    = json.loads(request.body)
        except (KeyError, ValueError) as e:
            return HttpResponseBadRequest()

        # Verify the domain.
        if not domain_is_valid(domain):
            return HttpResponseBadRequest()

        # Verify the HMAC.
        if not hmac_is_valid(request.body, settings.SHOPIFY_APP_API_SECRET, hmac):
            return HttpResponseForbidden()

        # Otherwise, set properties on the request object and return.
        request.carrier_request_data    = data
        request.carrier_request_domain  = domain
        return f(request, *args, **kwargs)

    return wrapper


def app_proxy(f):
    """
    A view decorator that checks and validates a Shopify Application proxy request.
    """

    @wraps(f)
    def wrapper(request, *args, **kwargs):

        # Verify the signature.
        if not proxy_signature_is_valid(request, settings.SHOPIFY_APP_API_SECRET):
            return HttpResponseBadRequest()

        return f(request, *args, **kwargs)

    return wrapper
