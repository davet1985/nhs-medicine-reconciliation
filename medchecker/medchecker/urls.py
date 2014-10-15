from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

# Regular URLs
urlpatterns = patterns('',
    url(r'^', include('core.urls')),
    url(r'^medicine/', include('medicine.urls')),
    )

# AJAX URLs
urlpatterns += patterns('',
    url(r'^' + settings.AJAX_URL + 'medicine/', include('medicine.urlsajax')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )