import glfw


def create_window():
    glfw.init()
    glfw.window_hint(glfw.MAXIMIZED, glfw.TRUE)
    window = glfw.create_window(800, 600, "Bloxel", None, None)
    glfw.set_window_size_limits(window, 800, 600, glfw.DONT_CARE, glfw.DONT_CARE)
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    return window

window = create_window()

while not glfw.window_should_close(window):
    glfw.poll_events()
    glfw.swap_buffers(window)

glfw.terminate()