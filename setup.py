#!/usr/bin/env python

from setuptools import setup, find_packages  # type: ignore

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    author="Yandex Money",
    author_email="cms@yamoney.ru",
    python_requires=">=2.7",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
    description="",
    entry_points={"console_scripts": ["yandex_checkout_payout=yandex_checkout_payout.cli:main", ], },
    install_requires=['nox', 'distro'],
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    package_data={"yandex_checkout_payout": ["py.typed"]},
    include_package_data=True,
    keywords="yandex, checkout, payout, sdk, python",
    name="yandex_checkout_payout",
    package_dir={"": "src"},
    packages=find_packages(include=["src/yandex_checkout_payout", "src/yandex_checkout_payout.*"]),
    setup_requires=[],
    url="https://github.com/yandex-money/yandex-checkout-payout-sdk-python",
    version="1.0.0",
    zip_safe=False,
)
