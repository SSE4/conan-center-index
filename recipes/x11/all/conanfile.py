from conans import ConanFile, tools
from conans.errors import ConanException
import os


class SysConfigX11Conan(ConanFile):
    name = "x11"
    version = "0.0.1"
    description = "cross-platform virtual conan package for the X11 support"
    topics = ("conan", "x11", "xorg")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.x.org/wiki/"
    license = "MIT"
    exports_sources = ["LICENSE"]
    settings = {"os": ["Linux"]}

    def package_id(self):
        self.info.header_only()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=".")

    @property
    def _libs_pkgconfig(self):
        pkg_config = tools.PkgConfig('x11')
        if not pkg_config.provides:
            raise ConanException("X11 development files aren't available, give up")
        libs = [lib[2:] for lib in pkg_config.libs_only_l]
        return libs

    def system_requirements(self):
        if tools.os_info.is_linux and self.settings.os == "Linux":
            package_tool = tools.SystemPackageTool(conanfile=self, default_mode='verify')
            if tools.os_info.with_yum:
                packages = ["TODO"]
            elif tools.os_info.with_apt:
                packages = ["xorg-dev"]
            elif tools.os_info.with_pacman:
                packages = ["TODO"]
            elif tools.os_info.with_yum:
                packages = ["TODO"]
            else:
                self.warn("don't know how to install OpenGL for your distro")
            package_tool.install(update=True, packages=packages)

    def package_info(self):
        self.cpp_info.libs = self._libs_pkgconfig
