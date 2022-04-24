from setuptools import setup, find_packages

setup(
    name="krate",
    version="1.0.0",
    description="Rank choices and compare with friends",
    author="Dave Fol",
    author_email="dof5@cornell.edu",
    install_requires=[
        "elosports @ git+https://github.com/ddm7018/Elo.git@master"
    ],
    entry_points={
        "console_scripts": [
            "krate=krate.krate:main",
            "kcreate=krate.kcreate:main",
            "kview=krate.kview:main",
        ]
    },
    packages=find_packages()
)
