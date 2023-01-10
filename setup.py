from setuptools import find_packages, setup

long_description = open('README.md', 'r').read()

requirements = [
    'beautifulsoup4==4.11.1',
    'certifi==2022.12.7',
    'charset-normalizer==2.1.1',
    'idna==3.4',
    'mutagen==1.46.0',
    'Pillow==9.3.0',
    'plum-py==0.8.5',
    'PyPDF2==3.0.1',
    'PySocks==1.7.1',
    'requests==2.28.1',
    'soupsieve==2.3.2.post1',
    'urllib3==1.26.13'
]

setup(
    name='unsafe',
    version='1.2.70',
    author='Ahura Rahmani',
    author_email='ahur4.rahmani@gmail.com',
    maintainer='Masoud Nayebi',
    maintainer_email='mesut@gmail.com',
    license='MIT',
    url='https://github.com/ahur4/unsafe',
    install_requires=requirements,
    keywords=[
        'hack', 'hack-module', 'pentest', 'unsafe', 'osint',
        'osint-python', 'hacking-python', 'cryptography', 'vulnerability-scanner', 'vulnerability', 'security',
        'hacker', 'admin-finder', 'wordpress-scanner', 'instagram-osint', 'cve', 'proxy-wrapper', 'proxy-checker',
        'ssh-connect', 'hydra', 'cracker', 'sqlmap', 'ahur4', 'mesutfd', 'crawler', 'acunetix'
    ],
    description='A practical and optimal library for those interested in Pentest, cryptography,Vulnerability Scanner and ..',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={},
    python_requires=">=3.8",
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
