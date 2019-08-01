import boto3
from local_config import s3_bucket_config


def ConnectToS3():
    """Connect to S3 consent buckets"""
    sess = boto3.Session()
    sr = sess.resource(
        service_name = 's3',
        aws_access_key_id = s3_bucket_config['access_key'],
        aws_secret_access_key = s3_bucket_config['secret_key'],
        endpoint_url =  s3_bucket_config['url']
        )

    return(sr)

def ListBucketFiles(b):
    """list all the files in a given bucket"""
    b = s.Bucket(b) 
    l = [x.key for x in b.objects.all()]
    return(l)

s = ConnectToS3() 

