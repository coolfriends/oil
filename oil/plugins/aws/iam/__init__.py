from oil.plugins.aws.iam.extra_access_key import ExtraAccessKeyPlugin
from oil.plugins.aws.iam.access_key_usage import AccessKeyUsagePlugin
from oil.plugins.aws.iam.user_mfa import UserMFAPlugin
from oil.plugins.aws.iam.user_password_rotation import UserPasswordRotationPlugin
from oil.plugins.aws.iam.total_users import TotalUsersPlugin

core_plugins = [
    ExtraAccessKeyPlugin,
    AccessKeyUsagePlugin,
    UserMFAPlugin,
    UserPasswordRotationPlugin,
    TotalUsersPlugin,
]
