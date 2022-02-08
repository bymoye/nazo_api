from setuptools import setup, Extension
from Cython.Build import cythonize
from Cython.Compiler import Options
Options.cimport_from_pyx = False
ext = [
    Extension("modules.rand.nazorand",sources = ["./modules/rand/nazorand.pyx"],extra_compile_args=["-std=c++17","-O2"]),
    Extension("modules.rand.randimg",sources = ["./modules/rand/randimg.pyx"],language=["c++"]),
]

setup(
    ext_modules=cythonize(ext,
        compiler_directives={
            'language_level': 3,
            'boundscheck': False,
            'wraparound': False,
            'binding': True,
        },
    )
)