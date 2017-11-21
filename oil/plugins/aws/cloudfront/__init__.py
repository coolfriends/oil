from oil.plugins.aws.cloudfront.tls_protocol import TLSProtocolPlugin
from oil.plugins.aws.cloudfront.https import HTTPSPlugin
from oil.plugins.aws.cloudfront.s3_origin_access_identity import S3OriginAccessIdentityPlugin

core_plugins = [
    TLSProtocolPlugin,
    HTTPSPlugin,
    S3OriginAccessIdentityPlugin,
]
