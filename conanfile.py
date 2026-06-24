import sys

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout


class ShapelyConan(ConanFile):
    name = "shapely"
    settings = "os", "compiler", "build_type", "arch"

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["Python3_EXECUTABLE"] = sys.executable.replace("\\", "/")
        tc.generate()
        CMakeDeps(self).generate()

    def requirements(self):
        self.requires("geos/3.13.0")

    def configure(self):
        if self.settings.os == "Windows":
            self.options["geos"].shared = True

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
