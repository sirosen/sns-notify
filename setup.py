from setuptools import setup

readme_text = ''
changelog_text = ''
with open('README.rst', 'r') as f:
    readme_text = f.read()
with open('CHANGELOG.rst', 'r') as f:
    changelog_text = f.read()

setup(
    name='sns-notify',
    version='0.1.0',

    install_requires=['argparse', 'boto>=2.34,<3'],
    packages=['sns_notify'],
    entry_points={'console_scripts': ['sns-notify = sns_notify.cli:main']},

    description='Simple SNS Notification Sender',
    long_description=readme_text + '\n\n\n' + changelog_text,
    author='Stephen Rosen',
    author_email='sirosen@uchicago.edu'
)
