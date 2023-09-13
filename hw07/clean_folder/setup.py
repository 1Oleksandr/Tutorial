from setuptools import setup

setup(
    name='clean_folder from Alex',
    version='0.0.1',
    description='Sort selected directory by type of file.',
    author='Oleksandr',
    author_email='test@te.net.ua',
    # url='https://github.com/'
    readme="README.md",
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    packages=['clean_folder'],
    entry_points={'console_scripts': ['clean-folder=clean_folder.clean:main']}
    )