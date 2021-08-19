"""
Config path for resource
"""

ROUTER_CONFIG = {
    "api": {
        "path": '/api',
        "v1": {
            "path": "/api/v1",
            "auth": {
                "path_login": "/api/v1/login", #done
                "path_logout": "/api/v1/logout", #done
            },
            "user": {
                "path_add_user": "/api/v1/register", #done
            },
            "transactions": {
                "path_list_transaction": "/api/v1/transaction",
                "path_add_transaction": "/api/v1/transaction/add",
                "path_update_transaction": "/api/v1/transaction/update",
                "path_filter_date": "/api/v1/transaction/filter/date",
            },
#done
            "currency": {
                "path_list_currency": "/api/v1/currency",
                "path_add_currency": "/api/v1/currency/add",
                "path_update_currency": "/api/v1/currency/update",
                "path_delete_currency": "/api/v1/currency/delete"
            }
        }
    }
}
