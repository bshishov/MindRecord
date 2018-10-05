import subprocess
import os
import logging
import json

from mindrecord.app import config


__all__ = ['run']

logger = logging.getLogger(__name__)


def run(cmd: list, input_path: str, output_path: str, work_dir: str=None):
    abs_input_path = os.path.abspath(input_path)
    abs_output_path = os.path.abspath(output_path)
    input_dir = os.path.dirname(abs_input_path)

    if not os.path.exists(abs_input_path):
        logger.debug('Input file for processing does not exist')
        return None

    stdout_path = os.path.join(input_dir, config.TESTS_PROCESSING_LOG)
    stderr_path = os.path.join(input_dir, config.TESTS_PROCESSING_ERROR_LOG)

    process = subprocess.Popen(cmd + [abs_input_path, abs_output_path],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               cwd=work_dir)
    stdout, stderr = process.communicate()
    logger.debug('Processing {0} finished with code: {1}'.format(cmd, process.returncode))

    # Log process outputs
    with open(stdout_path, 'wb') as f:
        f.write(stdout)

    if stderr:
        with open(stderr_path, 'wb') as f:
            f.write(stderr)

    # Check if program is completed with code 0
    if process.returncode != 0:
        logger.debug('Processing {0} failed'.format(cmd))
        return None

    if not os.path.exists(abs_output_path):
        logger.debug('No output provided')
        return None

    # Try read results from JSON
    try:
        with open(abs_output_path, encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as err:
        logger.exception(err)
        return None
