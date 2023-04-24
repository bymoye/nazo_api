from setuptools import setup, Extension
from Cython.Build import cythonize
from Cython.Compiler import Options
from sys import platform

extra_compile_args = []
extra_link_args = []

if platform == "win32":
    extra_compile_args = ["/std:c++17", "/O2"]
elif platform == "linux":
    extra_compile_args = ["-std=c++17", "-O3"]
    extra_link_args = ["-Wl,-O3"]
elif platform == "darwin":  # macOS
    extra_compile_args = ["-std=c++17", "-O3"]
    extra_link_args = ["-Wl,-dead_strip"]

Options.cimport_from_pyx = False
ext = [
    Extension(
        "modules.rand.randimg",
        sources=["./modules/rand/randimg.pyx"],
        language="c++",
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    ),
    Extension(
        "modules.asn.ip2asn",
        sources=[
            "./modules/asn/ip2asn.pyx",
            #  "./modules/asn/ipasn.cpp"
        ],
        language="c++",
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    ),
]

setup(
    ext_modules=cythonize(
        ext,
        compiler_directives={
            "language_level": 3,
            "boundscheck": False,
            "wraparound": False,
            "binding": True,
        },
    )
)
