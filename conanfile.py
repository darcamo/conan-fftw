from conans import ConanFile, CMake, tools
import os
import shutil

class FftwConan(ConanFile):
    name = "fftw3"
    version = "3.3.8"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Fftw here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def configure(self):
        # FFTW is implemented in C
        del self.settings.compiler.libcxx

    def source(self):
#         self.run("git clone https://github.com/memsharded/hello.git")
#         self.run("cd hello && git checkout static_shared")
#         # This small hack might be useful to guarantee proper /MT /MD linkage
#         # in MSVC if the packaged project doesn't have variables to set it
#         # properly
        tools.get("http://www.fftw.org/fftw-3.3.8.tar.gz")
        shutil.move("fftw-{0}".format(self.version), "sources")
        tools.replace_in_file("sources/CMakeLists.txt", "project (fftw)",
                              '''project (fftw)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        # Note that fftw library can build only one precision at a time. That
        # is way we need multiple cmake configure/build/install calls, each
        # with different definitions.
        os.mkdir("build")
        shutil.move("conanbuildinfo.cmake", "build/")
        cmake = CMake(self)

        cmake.definitions["BUILD_SHARED_LIBS"] = True
        cmake.definitions["BUILD_TESTS"] = "OFF"
        cmake.definitions["ENABLE_THREADS"] = True  # Use pthread for multithreading
        cmake.definitions["ENABLE_OPENMP"] = True

        # cmake.definitions["ENABLE_FLOAT"] = "ON"  # single-precision
        # cmake.definitions["ENABLE_LONG_DOUBLE"] = "ON"  # long-double precision
        # cmake.definitions["ENABLE_QUAD_PRECISION"] = "ON"  # quadruple-precision

        # cmake.definitions["ENABLE_SSE"] = True  # Compile with SSE instruction set support
        # cmake.definitions["ENABLE_SSE2"] = True # Compile with SSE2 instruction set support
        # cmake.definitions["ENABLE_AVX"] = True  # Compile with AVX instruction set support
        # cmake.definitions["ENABLE_AVX2"] = True # Compile with AVX2 instruction set support

        cmake.configure(source_folder="sources", build_folder="build")
        cmake.build()
        cmake.install()

        cmake.definitions["ENABLE_FLOAT"] = "ON"  # single-precision
        cmake.configure(source_folder="sources", build_folder="build")
        cmake.build()
        cmake.install()

        cmake.definitions["ENABLE_FLOAT"] = "OFF"  # single-precision
        cmake.definitions["ENABLE_LONG_DOUBLE"] = "ON"  # long-double precision
        cmake.configure(source_folder="sources", build_folder="build")
        cmake.build()
        cmake.install()

        cmake.definitions["ENABLE_FLOAT"] = "OFF"  # single-precision
        cmake.definitions["ENABLE_LONG_DOUBLE"] = "OFF"  # long-double precision
        cmake.definitions["ENABLE_QUAD_PRECISION"] = "ON"  # quadruple-precision
        cmake.configure(source_folder="sources", build_folder="build")
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libdirs = ["lib64", "lib"]
        self.cpp_info.libs = ["fftw3"]
