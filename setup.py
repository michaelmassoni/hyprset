from setuptools import setup, find_packages

setup(
    name="hyprset",
    version="0.1.0",
    description="A GTK4/LibAdwaita tool to configure your Hyprland desktop",
    author="michaelmassoni",
    author_email="hello@michaelmassoni.com", 
    url="https://github.com/michaelmassoni/hyprset",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PyGObject",
        # "hyprparser>=0.1.0", # Uncomment if/when hyprparser is on PyPI
    ],
    entry_points={
        "gui_scripts": [
            "hyprset=app.__main__:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Environment :: X11 Applications :: GTK",
    ],
    python_requires='>=3.6',
)
