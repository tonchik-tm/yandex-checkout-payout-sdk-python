#!/usr/bin/env python

from setuptools import setup, find_packages  # type: ignore

with open("README.en.md") as readme_file:
    readme = readme_file.read()

setup(
    author="Yandex Money",
    author_email="cms@yamoney.ru",
    python_requires=">=3.3",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="",
    entry_points={"console_scripts": ["yandex_checkout_payout=yandex_checkout_payout.cli:main", ], },
    install_requires=['nox', 'urllib3', 'requests', 'lxml'],
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    package_data={"yandex_checkout_payout": ["py.typed"]},
    include_package_data=True,
    keywords="yandex, checkout, payout, sdk, python",
    name="yandex_checkout_payout",
    package_dir={"": "src"},
    packages=find_packages(include=[
        "src/yandex_checkout_payout", "src/yandex_checkout_payout.*",
        "src/yandex_checkout_payout.domain.*", "src/yandex_checkout_payout.domain.common.*",
        "src/yandex_checkout_payout.domain.exceptions.*", "src/yandex_checkout_payout.domain.models.*",
        "src/yandex_checkout_payout.domain.request.*", "src/yandex_checkout_payout.domain.response.*"
    ]),
    setup_requires=[],
    url="https://github.com/yandex-money/yandex-checkout-payout-sdk-python",
    version="0.1.0",
    zip_safe=False,
)
