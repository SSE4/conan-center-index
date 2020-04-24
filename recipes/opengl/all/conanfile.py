from conans import ConanFile, tools
from conans.errors import ConanException
import os


class SysConfigOpenGLConan(ConanFile):
    name = "opengl"
    version = "0.0.1"
    description = "cross-platform virtual conan package for the OpenGL support"
    topics = ("conan", "opengl", "gl")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.opengl.org/"
    license = "MIT"
    exports_sources = ["LICENSE"]
    settings = ("os",)

    def source(self):
        from six.moves.urllib.parse import urlparse

        for source in self.conan_data["sources"][self.version]:
            url = source["url"]
            #sha256 = source["sha256"]
            filename = urlparse(url).path
            filename = filename[len("/registry/"):]
            if not os.path.isdir(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
            tools.download(url, filename)
            #tools.check_sha256(filename, sha256)

    def package_id(self):
        self.info.header_only()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=".")
        self.copy(pattern="*.h", dst="include", src=".", keep_path=True)

    @property
    def _libs_pkgconfig(self):
        pkg_config = tools.PkgConfig('gl')
        if not pkg_config.provides:
            raise ConanException("OpenGL development files aren't available, give up")
        libs = [lib[2:] for lib in pkg_config.libs_only_l]
        return libs

    def system_requirements(self):
        if tools.os_info.is_linux and self.settings.os == "Linux":
            package_tool = tools.SystemPackageTool(conanfile=self, default_mode='verify')
            if tools.os_info.with_yum:
                packages = ["mesa-libGLU-devel", "mesa-libGL-devel"]
            elif tools.os_info.with_apt:
                packages = ["libglu1-mesa-dev", "libgl1-mesa-dev"]
            elif tools.os_info.with_pacman:
                packages = ["glu", "libglvnd"]
            elif tools.os_info.with_yum:
                packages = ["glu-devel", "Mesa-libGL-devel"]
            else:
                self.warn("don't know how to install OpenGL for your distro")
            package_tool.install(update=True, packages=packages)

    def package_info(self):
        if self.settings.os == "Macos":
            self.cpp_info.defines.append("GL_SILENCE_DEPRECATION=1")
            self.cpp_info.frameworks.append("OpenGL")
        elif str(self.settings.os) in ["iOS", "watchOS", "tvOS"]:
            self.cpp_info.frameworks.append("OpenGLES")
        elif self.settings.os == "Android":
            self.cpp_info.libs = ["EGL", "GLESv2"]
        elif self.settings.os == "Windows":
            self.cpp_info.libs = ["OpenGL32.lib"]
        elif self.settings.os == "Linux":
            # FreeBSD should be the same?
            self.cpp_info.libs = self._libs_pkgconfig
