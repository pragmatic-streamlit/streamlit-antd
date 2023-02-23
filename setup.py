import setuptools

setuptools.setup(
    name="streamlit-antd",
    version="0.2.9",
    author="mapix",
    author_email="mapix.me@gmail.com",
    description="",
    long_description="",
    long_description_content_type="text/plain",
    url="https://github.com/mapix/streamlit-antd",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 0.63",
    ],
)
