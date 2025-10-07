from setuptools import setup, find_packages

setup(
    name="prediction_production_enr",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas>=1.5.0",
        "requests>=2.28.0",
        "supabase>=1.0.0",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
    ],
    python_requires=">=3.8",
)
