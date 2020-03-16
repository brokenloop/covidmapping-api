from django.urls import include, path
from rest_framework import routers
from cases import views
from cases.updater import Updater


updater = Updater()
updater.run()

router = routers.DefaultRouter()
router.register(r'raw-cases', views.CoronaCaseRawViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    # path('cases/', include('cases.urls')),
    # path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]