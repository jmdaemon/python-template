from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="{{- project_name -}}-{{- alias -}}",
    version="0.1.0",
    author="{{- author -}}",
    author_email="{{- email -}}",
    description="{{- desc -}}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/{{- username -}}/{{- project_name -}}",
    project_urls={
        "Bug Tracker": "https://github.com/{{- username -}}/{{- project_name -}}/issues",
    },
    license='MIT',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    py_modules=[],
    {% - if cli == 'Click' - %}
    install_requires=[
        'Click',
    ],
    {% - elif cli == 'argparse' - %}
    install_requires=[
        'argparse',
    ],
    {% - else - %}
    {% - endif - %}
    test_suite='tests',
)
