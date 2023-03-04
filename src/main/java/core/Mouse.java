package core;

import java.util.HashMap;
import java.util.Map;

import static org.lwjgl.glfw.GLFW.GLFW_PRESS;
import static org.lwjgl.glfw.GLFW.GLFW_RELEASE;

public class Mouse {
    private static Mouse instance = null;

    private double x, y, lastX, lastY;
    private double scrollX, scrollY;
    private Map<Integer, Boolean> buttonsDown = new HashMap<>();
    private Map<Integer, Boolean> buttonsPressed = new HashMap<>();

    private Mouse() {
        this.x = 0;
        this.y = 0;
        this.lastX = 0;
        this.lastY = 0;
        this.scrollX = 0;
        this.scrollY = 0;
    }

    public static Mouse getInstance() {
        if (instance == null) {
            instance = new Mouse();
        }

        return instance;
    }

    public static void cursorPosCallback(long window, double x, double y) {
        getInstance().lastX = getInstance().x;
        getInstance().lastY = getInstance().y;
        getInstance().x = x;
        getInstance().y = y;
    }

    public static void mouseButtonCallback(long window, int button, int action, int mods) {
        if (action == GLFW_PRESS) {
            getInstance().buttonsDown.put(button, true);
            getInstance().buttonsPressed.put(button, true);
        } else if (action == GLFW_RELEASE) {
            getInstance().buttonsDown.put(button, false);
        }
    }

    public static void scrollCallback(long window, double x, double y) {
        getInstance().scrollX = x;
        getInstance().scrollY = y;
    }

    public static void update() {
        getInstance().buttonsPressed.clear();

        getInstance().scrollX = 0;
        getInstance().scrollY = 0;
    }

    public static float getX() {
        return (float)getInstance().x;
    }

    public static float getY() {
        return (float)getInstance().y;
    }

    public static float getDX() {
        return (float)(getInstance().x - getInstance().lastX);
    }

    public static float getDY() {
        return (float)(getInstance().y - getInstance().lastY);
    }

    public static float getScrollX() {
        return (float)getInstance().scrollX;
    }

    public static float getScrollY() {
        return (float)getInstance().scrollY;
    }

    public static boolean isButtonDown(int button) {
        return getInstance().buttonsDown.getOrDefault(button, false);
    }

    public static boolean isButtonPressed(int button) {
        return getInstance().buttonsPressed.getOrDefault(button, false);
    }
}
