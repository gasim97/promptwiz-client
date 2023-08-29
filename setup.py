from setuptools import setup, find_packages  

setup(
    name='promptwizclient', 
    version='0.1.1', 
    packages=find_packages(), 
    author='Prompt Wiz', 
    author_email='', 
    description='A client to interact with the PromptWiz API.', 
    long_description=open('README.md').read(),
    url='https://github.com/gasim97/promptwizclient', 
    install_requires=[
        'requests'
    ],
)