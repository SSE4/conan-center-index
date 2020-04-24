#include <iostream>

#ifdef __APPLE__

#include "TargetConditionals.h"

#if TARGET_OS_TV || TARGET_OS_WATCH || TARGET_OS_IPHONE
#include <OpenGLES/ES2/gl.h>
#else
#include <OpenGL/gl.h>
#endif

#elif defined(__ANDROID__)

#include <GLES2/gl2.h>

bool init_context() { return true; }

#else

#ifdef _WIN32
#include <Windows.h>
#endif

#include <GL/gl.h>
#include <GL/glu.h>
#endif

bool init_context();

int main()
{
    if (!init_context())
    {
        std::cerr << "failed to initialize OpenGL context!" << std::endl;
        return -1;
    }
    const char * gl_vendor = (const char *) glGetString(GL_VENDOR);
    const char * gl_renderer = (const char *) glGetString(GL_RENDERER);
    const char * gl_version = (const char *) glGetString(GL_VERSION);
    const char * gl_extensions = (const char *) glGetString(GL_EXTENSIONS);
    std::cout << "GL_VENDOR: " << (gl_vendor ? gl_vendor : "(null)") << std::endl;
    std::cout << "GL_RENDERER: " << (gl_renderer ? gl_renderer : "(null)") << std::endl;
    std::cout << "GL_VERSION: " << (gl_version ? gl_version : "(null)") << std::endl;
    std::cout << "GL_EXTENSIONS: " << (gl_extensions ? gl_extensions : "(null)") << std::endl;
    return 0;
}
