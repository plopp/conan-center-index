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
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_snappy": [True, False],
    }
    default_options = {"shared": False, "fPIC": True, "with_snappy": True}
    generators = "cmake", "cmake_find_package"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("avro-release-" + self.version, "source_subfolder")
        tools.replace_in_file(
            os.path.join(self._source_subfolder, "CMakeLists.txt"),
            "project (Avro-cpp)",
            """project (Avro-cpp)
               include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
               conan_basic_setup() """,
        )

        # Let Conan find snappy
        if self.options.with_snappy:
            tools.replace_in_file(
                os.path.join(self._source_subfolder, "CMakeLists.txt"),
                "find_package(Snappy)",
                "",
            )

    @property
    def _source_subfolder(self):
        return os.path.join("source_subfolder", "lang", "c++")

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def _build_requirements(self):
        self.build_requires("boost/1.75.0")
        if self.options.with_snappy:
            self.build_requires("snappy/1.1.8")

    def package(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_subfolder)
        cmake.install()

    def package_info(self):
        self.cpp_info.filenames["cmake_find_package"] = "avrocpp"
        self.cpp_info.filenames["cmake_find_package_multi"] = "avrocpp"
        self.cpp_info.names["cmake_find_package"] = "AvroCPP"
        self.cpp_info.names["cmake_find_package_multi"] = "AvroCPP"
        self.cpp_info.components["avrocpplib"].names["cmake_find_package"] = "avrocpp"
        self.cpp_info.components["avrocpplib"].names[
            "cmake_find_package_multi"
        ] = "avrocpp"

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_subfolder)
        cmake.build()
