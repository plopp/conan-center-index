import os

from conans import ConanFile, CMake, tools

class AvrocppConan(ConanFile):
    name = "avrocpp"
    description = "Avro is a data serialization system."
    homepage = "https://avro.apache.org/"
    url = "https://github.com/conan-io/conan-center-index"
    license = "Apache License 2.0"
    topics = ("serialization", "deserialization")
    # no_copy_source = True
    # exports_sources = ["CMakeLists.txt"]
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"

    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder/lang/c++"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def build_requirements(self):
        self.build_requires("boost/1.72.0")
#     libboost-dev
# libboost-filesystem-dev
# libboost-iostreams-dev
# libboost-program-options-dev
# libboost-system-dev


    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("avro-release-" + self.version, "source_subfolder")

    def package(self):
        self.copy("*.h", dst="include", src="hello")
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    # def package_info(self):
    #     self.cpp_info.libs = ["hello"]

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_subfolder)
        cmake.build()

