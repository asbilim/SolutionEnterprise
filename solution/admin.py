from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from shop.models import Product, Request, Contact
from blog.models import Article
from django.contrib.admin import AdminSite
from unfold.admin import UnfoldAdminSite

def get_admin_dashboard(request):
    # Get date range
    today = timezone.now()
    last_30_days = today - timedelta(days=30)
    
    # Get statistics
    total_products = Product.objects.count()
    total_requests = Request.objects.filter(created_at__gte=last_30_days).count()
    total_contacts = Contact.objects.filter(created_at__gte=last_30_days).count()
    total_articles = Article.objects.count()
    
    # Most viewed articles
    popular_articles = Article.objects.order_by('-likes')[:5]
    
    # Recent requests
    recent_requests = Request.objects.order_by('-created_at')[:5]
    
    return {
        'title': 'Dashboard',
        'cards': [
            {'title': 'Total Products', 'value': total_products, 'icon': 'shopping-cart'},
            {'title': 'Recent Requests', 'value': total_requests, 'icon': 'paper-airplane'},
            {'title': 'Recent Contacts', 'value': total_contacts, 'icon': 'envelope'},
            {'title': 'Total Articles', 'value': total_articles, 'icon': 'newspaper'},
        ],
        'charts': [
            {
                'title': 'Popular Articles',
                'type': 'bar',
                'labels': [article.title for article in popular_articles],
                'datasets': [{
                    'label': 'Likes',
                    'data': [article.likes for article in popular_articles],
                }],
            }
        ],
        'tables': [
            {
                'title': 'Recent Requests',
                'headers': ['Email', 'Product', 'Date'],
                'rows': [[req.email, req.product.name, req.created_at] for req in recent_requests],
            }
        ],
    }

class CustomAdminSite(UnfoldAdminSite):
    site_title = "Solution Enterprise"
    site_header = "Solution Enterprise Admin"
    index_title = "Dashboard"

    def get_app_list(self, request, app_label=None):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_list = super().get_app_list(request, app_label)
        
        # Sort the apps alphabetically
        app_list.sort(key=lambda x: x['name'].lower())
        
        # Sort the models alphabetically within each app
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'].lower())
        
        return app_list

admin_site = CustomAdminSite() 