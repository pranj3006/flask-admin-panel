from setuptools import setup, find_packages

setup(
    name='flask-admin-panel',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask==3.0.2',
        'flask-restx==1.3.0',
        'Flask-SQLAlchemy==3.1.1',
        'Flask-JWT-Extended==4.6.0',
        'pytest==8.1.1',
        'pytest-cov==5.0.0',
        'Flask-WTF==1.2.1',
        'WTForms==3.1.2',
        'SQLAlchemy==2.0.27',
        'WTForms-Alchemy==0.18.0',
        'WTForms-Components==0.10.5'        
        # Add other dependencies here
    ],
    package_data={
        'admin_panel': ['admin_panel/templates/admin_panel/*.html']
    },
    author='Pranjal Gharat',
    author_email='pranj3006@gmail.com',
    description='Simple Admin Panel for Flask',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pranj3006/flask-admin-panel',  # Update with your project URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
