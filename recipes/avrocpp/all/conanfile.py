import os

from conans import ConanFile, CMake, tools

class AvrocppConan(ConanFile):
    name = "avrocpp"
    versuib = "0.1"
    license = "Apache License 2.0"
    url = "https://github.com/conan-io/conan-center-index"
    description = "Avro is a data serialization system."
    homepage = "https://avro.apache.org/"
    topics = ("serialization", "deserialization")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake", "cmake_find_package"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("avro-release-" + self.version, "source_subfolder")
        # os.remove("source_subfolder/lang/c++/FindSnappy.cmake")
        tools.replace_in_file(os.path.join(self._source_subfolder, "CMakeLists.txt"), "project (Avro-cpp)",
            '''project (Avro-cpp)
               include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
               conan_basic_setup() ''')

        tools.replace_in_file(os.path.join(self._source_subfolder, "CMakeLists.txt"), "find_package(Snappy)",
            "")


    @property
    def _source_subfolder(self):
        return os.path.join("source_subfolder", "lang", "c++")

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def build_requirements(self):
        self.build_requires("boost/1.75.0")
        self.build_requires("snappy/1.1.8")

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

