from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'person_follow'

data_files = [
    (os.path.join('share', package_name, 'person_follow_cv/data'), glob('person_follow/person_follow_cv/data/*'))
]

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ] + data_files,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='robot_team',
    maintainer_email='robot_team@spacemit.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'person_follow_node = person_follow.person_follow_node:main',
        ],
    },
)
