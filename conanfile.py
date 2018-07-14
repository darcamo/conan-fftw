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
        os.mkdir("build")
        shutil.move("conanbuildinfo.cmake", "build/")
        cmake = CMake(self)
        cmake.configure(source_folder="sources", build_folder="build")
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("*.h", dst="include", src="hello")
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libdirs = ["lib64", "lib"]
        self.cpp_info.libs = ["fftw3"]
