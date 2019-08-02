import boto3
from local_config import s3_bucket_config
import logging

logger = logging.getLogger(__name__)

def connectToS3():
    """Connect to S3 consent buckets"""
    logger.debug('Received call to connectToS3')
    sess = boto3.Session()
    sr = sess.resource(
        service_name = 's3',
        aws_access_key_id = s3_bucket_config['access_key'],
        aws_secret_access_key = s3_bucket_config['secret_key'],
        endpoint_url =  s3_bucket_config['url']
        )

    return(sr)

def listBucketFiles(b = 'patient-records'):
    """list all the files in a given bucket"""
    logger.debug('Received call to listBucketFiles for %s' % b)
    bu = s.Bucket(b) 
    l = [(b, x.key) for x in bu.objects.all()]
    logger.info('Got listing of %s files in %s' % (len(l), b))
    return(l)

def createS3Obj(b, k):
    """create and S3 object from bucket name and object key"""
    logger.debug('Received call to createS3Obj - %s : %s' % (b, k))
    return(s.Object(b, k))

s = connectToS3() 

