VERSION     = (0, 8, 0)
__version__ = '.'.join(map(str, VERSION))
__author__ = 'Gavin Ballard'


WEBHOOK_TOPICS = [
    'app/uninstalled',
    'carts/create',
    'carts/update',
    'checkouts/create',
    'checkouts/update',
    'checkouts/delete',
    'collections/create',
    'collections/update',
    'collections/delete',
    'customer_groups/create',
    'customer_groups/update',
    'customer_groups/delete',
    'customers/create',
    'customers/disable',
    'customers/delete',
    'customers/enable',
    'customers/update',
    'disputes/create',
    'disputes/update',
    'fulfillments/create',
    'fulfillments/update',
    'orders/create',
    'orders/delete',
    'orders/updated',
    'orders/paid',
    'orders/cancelled',
    'orders/fulfilled',
    'orders/partially_fulfilled',
    'order_transactions/create',
    'products/create',
    'products/update',
    'products/delete',
    'refunds/create',
    'shop/update'
]
