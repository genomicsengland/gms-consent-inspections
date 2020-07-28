"""
provides functions for interacting with files on S3 Buckets
"""
import boto3
from local_config import s3_bucket_config
import logging

LOGGER = logging.getLogger(__name__)


def connect_to_s3():
    """
    Connect to S3 consent buckets
    """

    LOGGER.debug('Received call to connect_to_s3')

    sess = boto3.Session()
    sr = sess.resource(
        service_name='s3',
        aws_access_key_id=s3_bucket_config['access_key'],
        aws_secret_access_key=s3_bucket_config['secret_key'],
        endpoint_url=s3_bucket_config['url']
    )

    return sr


def list_bucket_files(b='patient-records'):
    """
    list all the files in a given bucket
    :params b: name of bucket to connect to
    :returns: list of all files in the bucket
    """

    LOGGER.debug('Received call to list_bucket_files for %s', b)

    # connect to the S3 Bucket
    bu = s.Bucket(b)

    # retrieve all files in the bucket
    l = [x for x in bu.objects.all()]

    LOGGER.info('Got listing of %s files in %s', len(l), b)

    return l


def create_s3_obj(b, k):
    """
    create and S3 object from bucket name and object key
    :params b: bucket name
    :params k: object key
    :returns: S3 bucket object
    """

    LOGGER.debug('Received call to create_s3_obj - %s : %s',b, k)

    return s.Object(b, k)


# create an S3 connection to work with
s = connect_to_s3()
