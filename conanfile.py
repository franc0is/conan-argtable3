from conans import ConanFile, CMake, tools


class Argtable3Conan(ConanFile):
    name = "argtable3"
    version = "3.0.3"
    license = "BSD"
    url = "http://www.argtable.org/"
    description = "A single-file, ANSI C, command-line parsing library that parses GNU-style command-line options."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/franc0is/argtable3.git")
        self.run("cd argtable3 && git checkout master")
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("argtable3/CMakeLists.txt", "project(argtable3)", '''project(argtable3)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="argtable3")
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="argtable3")
        self.copy("*argtable3.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["argtable3"]
