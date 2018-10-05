from mindrecord.utils import Router
from mindrecord.app import config
import mindrecord.views as views
import mindrecord.auth as auth
import mindrecord.debug_views as debug_views
import mindrecord.test_views as test_views

router = Router()
router.add_route('^/api/$', views.home_view)
router.add_route('^/api/auth$', auth.auth_view)
router.add_route('^/api/verify-email$', auth.verify_email_view)
router.add_route('^/api/user', views.user_view)

router.add_route('^/api/tests$', test_views.tests_list_view)
router.add_route('^/api/tests/(?P<uri>[0-9a-z_\-]+)$', test_views.test_details_view)
router.add_route('^/api/tests/(?P<uri>[0-9a-z_\-]+)/web/(?P<path>.*)$', test_views.web_resource_view)
router.add_route('^/api/tests/(?P<uri>[0-9a-z_\-]+)/cover$', test_views.cover_view)
router.add_route('^/api/tests/(?P<uri>[0-9a-z_\-]+)/results$', test_views.test_results_submission)

router.add_route('^/api/results/(?P<id>[0-9a-z_\-]+)$', test_views.test_results)
router.add_route('^/api/results/(?P<id>[0-9a-z_\-]+)/log$', test_views.test_results_log)
router.add_route('^/api/results/(?P<id>[0-9a-z_\-]+)/error_log$', test_views.test_results_error_log)

router.add_route('^/api/load-tests', test_views.load_tests_view)


if config.DEBUG:
    router.add_route('^/api/debug/private$', debug_views.private_view)
    router.add_route('^/api/debug/upload', debug_views.upload_view)
    router.add_route('^/api/debug/download', debug_views.download_view)
    router.add_route('^/api/debug/(?P<id>[0-9a-z]+)$', debug_views.get_param_view)
