import os
import sys

# add arcimoto-aws-services git submodule to path to allow imports to work
(parent_folder_path, current_dir) = os.path.split(os.path.dirname(__file__))
sys.path.append(os.path.join(parent_folder_path, 'arcimoto_aws_services'))
