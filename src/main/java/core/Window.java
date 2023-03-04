package core;

import org.lwjgl.glfw.GLFWErrorCallback;
import org.lwjgl.opengl.GL;
import scenes.Test;

import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.system.MemoryUtil.NULL;
import static org.lwjgl.opengl.GL33.*;

public class Window {
    private static Window instance = null;

    private int width, height;
    private String title;
    private long glfwWindow;

    private Window() {
        this.width = 800;
        this.height = 600;
        this.title = "Krii by Vinny Horgan";
    }

    public static Window getInstance() {
        if (instance == null) {
            instance = new Window();
        }

        return instance;
    }

    public void run() {
        init();
        loop();

        SceneManager.unload();

        glfwTerminate();
    }

    public static int getWidth() {
        return getInstance().width;
    }

    public static int getHeight() {
        return getInstance().height;
    }

    private void init() {
        GLFWErrorCallback.createPrint(System.err).set();

        if (!glfwInit()) {
            throw new IllegalStateException("Error initializing GLFW");
        }

        glfwDefaultWindowHints();

        glfwWindow = glfwCreateWindow(width, height, title, NULL, NULL);
        if (glfwWindow == NULL) {
            throw new RuntimeException("Error creating GLFW window");
        }

        glfwSetKeyCallback(glfwWindow, Keyboard::keyCallback);
        glfwSetCursorPosCallback(glfwWindow, Mouse::cursorPosCallback);
        glfwSetMouseButtonCallback(glfwWindow, Mouse::mouseButtonCallback);
        glfwSetScrollCallback(glfwWindow, Mouse::scrollCallback);
        glfwSetFramebufferSizeCallback(glfwWindow, (window, width, height) -> {
            glViewport(0, 0, width, height);
            this.width = width;
            this.height = height;
        });

        glfwMakeContextCurrent(glfwWindow);

        glfwSwapInterval(1);

        GL.createCapabilities();

        SceneManager.setScene(new Test());
    }

    private void loop() {
        float beginTime = (float)glfwGetTime();
        float endTime;
        float dt = -1.0f;

        while (!glfwWindowShouldClose(glfwWindow)) {
            glfwPollEvents();

            if (dt >= 0) {
                SceneManager.update(dt);
            }

            Keyboard.update();
            Mouse.update();

            glfwSwapBuffers(glfwWindow);

            endTime = (float)glfwGetTime();
            dt = endTime - beginTime;
            beginTime = endTime;
        }
    }
}
