from setuptools import setup, find_packages
setup(
    name='otf_general_public',  # Name of your overall repo/package
    version='0.1.0',
    author='Iskandar E, Sihao J',
    description='On-the-Fly RBFE/ABFE simulation framework for AMBER20',
    packages=find_packages(),  # include submodules
    # install_requires=[
    #     'pymbar==4.0.3',
    #     'alchemlyb==2.3.1',
    #     'scipy==1.8.1'
    # ],
    python_requires='>=3.0',
    include_package_data=True,
)

