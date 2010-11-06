try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
        name='gh-hooky',
        description='Enhanced Github issues',
        version='0.1',
        author='Wes Mason',
        author_email='wes@1stvamp.org',
        url='http://github.com/1stvamp/gh-hooky',
        packages=find_packages('src', exclude=['ez_setup']),
        package_dir={'': 'src'},
        setup_requires=open('requirements.txt', 'r').readlines(),
        install_requires=['setuptools'],
        license='Apache License 2.0'
)
