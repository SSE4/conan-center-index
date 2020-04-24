#include <X11/Xlib.h>
#include <X11/Xutil.h>

int main()
{
    Display *display = XOpenDisplay(NULL);
    if (display)
        XCloseDisplay(display);
}
