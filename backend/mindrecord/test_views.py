import logging
import os
import json
import glob
import re
import datetime
import threading
from urllib.parse import unquote
from bson import ObjectId

from mindrecord.utils import Request, JsonResponse, \
    Status, HTTPError, Response, allow_methods, FileResponse, allow_cors, cache_control, BaseConfig
from mindrecord.app import config, db
from mindrecord.auth import *
from mindrecord.processing import run
from mindrecord.models import TestResult

logger = logging.getLogger(__name__)
tests = {}
results_db = db['results']


def load_test_from_config(config_path):
    if not os.path.exists(config_path):
        logger.debug('Config path does not exits: {0}'.format(config_path))
        return None

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            test_config = json.load(f)  # type: dict
    except json.JSONDecodeError as err:
        logger.exception(err)
        logger.debug('Invalid JSON configuration: {0}'.format(config_path))
        return None

    required_fields = ['id', 'name', 'inputs', 'outputs', 'processing']
    for field in required_fields:
        if field not in test_config:
            logger.warning('Field {0} required'.format(field))
            return None
    test_dir = os.path.dirname(config_path)
    test = test_config.copy()
    test.update({
        'dir': test_dir,
        'config_path': config_path,
    })

    if 'readme' in test_config:
        readme_path = os.path.join(test_dir, test_config.get('readme'))
        if os.path.exists(readme_path):
            test['readme_path'] = readme_path

    if 'web' in test_config:
        web_cfg = test_config.get('web')
        work_dir = web_cfg.get('workdir', './')
        entry = web_cfg.get('entry', 'index.html')
        test['web_workdir'] = os.path.join(test_dir, work_dir)
        test['web_entry'] = os.path.join(test_dir, work_dir, entry)

    if 'processing' in test_config:
        processing_cfg = test_config.get('processing')
        work_dir = processing_cfg.get('workdir', './')
        test['processing_workdir'] = os.path.join(test_dir, work_dir)

    if 'cover' in test_config:
        cover_path = test_config.get('cover')
        if cover_path is not None:
            cover_path = os.path.join(test_dir, cover_path)
        test['cover_path'] = cover_path
    return test


def load_tests():
    tests.clear()
    config_paths = glob.glob(config.TESTS_CONFIG_PATTERN)
    for config_path in config_paths:
        logger.debug('Reading config: {0}'.format(config_path))
        test = load_test_from_config(config_path)
        if not test:
            continue
        logger.debug('Test {0}'.format(test.get('id')))
        tests[test.get('id')] = test


@requires_auth(allowed_roles=[Roles.ADMIN])
@allow_methods('GET')
def load_tests_view(request: Request):
    """ Utility view for loading the tests (ADMIN only) """
    load_tests()
    return JsonResponse(tests)


def _test_to_view(test: dict) -> dict:
    exclude = ['processing']
    view = {k: v for k, v in test.items() if k not in exclude}
    return view


@allow_cors(methods='GET')
@allow_methods('GET')
def tests_list_view(request: Request):
    return JsonResponse([_test_to_view(v) for v in tests.values()])


@allow_cors(methods='GET')
@allow_methods('GET')
def test_details_view(request: Request, uri: str):
    test = tests.get(uri, None)
    if not test:
        raise HTTPError(Status.NOT_FOUND)

    return JsonResponse(_test_to_view(test))


def __static_404():
    return Response(data='<h1>404: Not found</h1>'.encode('utf-8'),
                    status_code=Status.NOT_FOUND, content_type='text/html')


@cache_control()
@allow_cors(methods='GET')
@allow_methods('GET')
def web_resource_view(request: Request, uri: str, path: str):
    test = tests.get(uri, None)
    if not test:
        return __static_404()

    web_workdir = test.get('web_workdir', None)
    if not web_workdir:
        return __static_404()

    if not path:
        web_entry = test.get('web_entry', None)
        if not web_entry or not os.path.exists(web_entry):
            return __static_404()
        return FileResponse(web_entry)

    path = unquote(path)
    # Todo: IMPROVE SECURITY!
    match = re.match('^[\\\/.]*(.*)$', path)
    if match:
        path = match.group(1)

    resource_path = os.path.join(web_workdir, path)

    if os.path.exists(resource_path):
        return FileResponse(resource_path)
    return __static_404()


@cache_control()
@allow_cors(methods='GET')
@allow_methods('GET')
def cover_view(request: Request, uri: str):
    test = tests.get(uri, None)
    if not test:
        return __static_404()

    cover_path = test.get('cover_path', None)
    if not cover_path or not os.path.exists(cover_path):
        return __static_404()

    return FileResponse(cover_path)


@allow_cors()
@allow_methods('GET')
def test_results(request: Request, id: str):
    result_id = ObjectId(id)
    result = results_db.find_one({'_id': result_id})
    if not result:
        raise HTTPError(Status.NOT_FOUND)
    fields = ['state', 'created', 'processed', 'user', 'test', 'data']
    data = {k: v for k, v in result.items() if k in fields}
    data['id'] = str(result_id)
    data['user'] = str(data['user'])

    created = data.get('created', None)
    if created and isinstance(created, datetime.datetime):
        data['created'] = created.isoformat()

    processed = data.get('processed', None)
    if created and isinstance(processed, datetime.datetime):
        data['processed'] = processed.isoformat()

    return JsonResponse(data)


@allow_cors()
@allow_methods('GET')
@requires_auth(allowed_roles=[Roles.ADMIN])
def test_results_log(request: Request, id: str):
    result_id = ObjectId(id)
    result = results_db.find_one({'_id': result_id})
    if not result:
        raise HTTPError(Status.NOT_FOUND)
    directory = result.get('directory', os.path.join(config.TESTS_RESULTS_DIR, result.get('test'), str(result_id)))
    log_file = os.path.join(directory, config.TESTS_PROCESSING_LOG)
    if not os.path.exists(log_file):
        raise HTTPError(Status.NOT_FOUND)
    return FileResponse(log_file)


@allow_cors()
@allow_methods('GET')
@requires_auth(allowed_roles=[Roles.ADMIN])
def test_results_error_log(request: Request, id: str):
    result_id = ObjectId(id)
    result = results_db.find_one({'_id': result_id})
    if not result:
        raise HTTPError(Status.NOT_FOUND)
    directory = result.get('directory', os.path.join(config.TESTS_RESULTS_DIR, result.get('test'), str(result_id)))
    log_file = os.path.join(directory, config.TESTS_PROCESSING_ERROR_LOG)
    if not os.path.exists(log_file):
        raise HTTPError(Status.NOT_FOUND)
    return FileResponse(log_file)


@allow_cors()
@allow_methods('POST')
@requires_auth()
def test_results_submission(request: Request, uri: str):
    """ 1. Authorized person submits a POST request via:
            - multipart
            - urlencoded form-data
            - plain/text
            - queryset
        containing keys and values for a specific set of fields
        listed in 'inputs' section in test configuration.
        2. All necessary fields are saved to the config.TESTS_RESULTS_PATH/{results_id} path
            2.1 If field do not fulfill the requirements - the request is rejected
        3. Processing runs (if required/possible) asynchronously
            3.1. If processing is successful results.json is produced containing 'outputs'
            3.2. Outputs are stored in the database
        4. {result_id} is returned while processing is still going
    """
    user = get_user_from_request(request)
    if not user or not user.id or user.role == Roles.UNAUTHORIZED:
        raise HTTPError(Status.UNAUTHORIZED)

    test = tests.get(uri, None)
    if not test:
        raise HTTPError(Status.NOT_FOUND)

    inputs = test.get('inputs', None)
    if not inputs:
        raise HTTPError(Status.INTERNAL_SERVER_ERROR, message='Test is improperly configured')

    # Check inputs
    for name, input_desc in inputs.items():
        # if the field is required and not present - raise an error
        if input_desc.get('required', True) and name not in request.data:
            raise HTTPError(Status.INTERNAL_SERVER_ERROR,
                            message='{0} field required but there is none'.format(name))

    # Create new results entry
    results_id = ObjectId()

    # Location to store results: RESULTS_PATH/<test_id>/<results_id>
    results_dir = os.path.join(config.TESTS_RESULTS_DIR, test.get('id'), str(results_id))
    os.makedirs(results_dir)

    # Save json object to RESULTS_RAW_FILE
    inputs_obj = {
        '_fields': inputs,
        '_test_id': test.get('id'),
        '_user_id': user.id,
        '_results_id': str(results_id),
        '_created': datetime.datetime.utcnow().isoformat(),
        '_results': config.TESTS_RESULTS_FILE
    }
    for name, input_desc in inputs.items():
        value = request.data.get(name, None)
        if not value:
            continue
        if input_desc.get('type') == 'file':
            # TODO: save file from request
            inputs_obj[name] = input_desc.get('filename', name + '.dat')
        else:
            inputs_obj[name] = value

    # Output all RAW inputs for processing to the corresponding file
    with open(os.path.join(results_dir, config.TESTS_RESULTS_RAW_FILE), 'w', encoding='utf-8') as fp:
        json.dump(inputs_obj, fp)

    # TODO: If no processing specified - do 'COPY PROCESSING'
    test_processing_desc = test.get('processing', None)
    if not test_processing_desc:
        # TODO: implement bypassing in tests
        raise HTTPError(Status.NOT_IMPLEMENTED)

    # Save result (raw one)
    result = TestResult(id=results_id,
                        user=ObjectId(user.id),
                        directory=results_dir,
                        test=test.get('id'),
                        raw_file=config.TESTS_RESULTS_RAW_FILE,
                        output_file=config.TESTS_RESULTS_FILE)
    result.save()

    # Initiate processing of raw results
    __process_and_save_async(result_id=results_id,
                             test=test,
                             result_dir=result.directory,
                             raw_file_name=result.raw_file,
                             output_file_name=result.output_file)

    # Return valid result id
    return JsonResponse({'results_id': str(results_id)}, status_code=Status.ACCEPTED)


def __fail(result_id: ObjectId, reason: str = None):
    logger.error('Failed processing: {0} {1}'.format(result_id, reason))
    results_db.update_one({'_id': result_id}, update={'$set': {'state': 'fail'}})


def __process_and_save(result_id: ObjectId,
                       cmd: list,
                       input_path: str,
                       output_path: str,
                       work_dir: str,
                       output_spec: dict):
    try:
        data = run(cmd, input_path, output_path, work_dir)
    except Exception as err:
        __fail(result_id)
        return

    if not data:
        __fail(result_id)
        return

    # Filter outputs according to test configuration
    # TODO: verify type
    filtered_data = {k: data.get(k, None) for k in output_spec}

    # Update database row
    results_db.update_one({'_id': result_id}, update={'$set': {
        'state': 'processed',
        'processed': datetime.datetime.utcnow(),
        'data': filtered_data
    }})


def __process_and_save_async(result_id: ObjectId, test: dict, result_dir: str, raw_file_name: str, output_file_name: str):
    processing_desc = test.get('processing', None)
    if not processing_desc:
        __fail(result_id)
        return

    cmd = processing_desc.get('call', None)
    if isinstance(cmd, str):
        cmd = [cmd]
    if not cmd:
        __fail(result_id)
        return

    cwd = test.get('processing_workdir', test.get('dir', result_dir))
    if not cwd:
        __fail(result_id)
        return

    thread = threading.Thread(None, __process_and_save, kwargs={
        'result_id': result_id,
        'cmd': cmd,
        'input_path': os.path.join(result_dir, raw_file_name),
        'output_path': os.path.join(result_dir, output_file_name),
        'work_dir': cwd,
        'output_spec': test.get('outputs', {})
    }, daemon=True)
    thread.start()


""" If tests are not set - load them"""
if not tests:
    load_tests()
