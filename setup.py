from setuptools import setup, Extension
from Cython.Build import cythonize
from Cython.Compiler import Options

Options.cimport_from_pyx = False
ext = [
    Extension(
        "modules.rand.randimg",
        sources=["./modules/rand/randimg.pyx"],
        language=["c++"],
        extra_compile_args=["-O3"],
    ),
    Extension(
        "modules.asn.ip2asn",
        sources=["./modules/asn/ip2asn.pyx"],
        language=["c++"],
        extra_compile_args=["-std=c++17", "-O2"],
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
