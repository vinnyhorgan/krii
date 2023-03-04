package core;

import java.util.HashMap;
import java.util.Map;

import static org.lwjgl.glfw.GLFW.GLFW_PRESS;
import static org.lwjgl.glfw.GLFW.GLFW_RELEASE;

public class Keyboard {
    private static Keyboard instance = null;

    private Map<Integer, Boolean> keysDown = new HashMap<>();
    private Map<Integer, Boolean> keysPressed = new HashMap<>();

    private Keyboard() {

    }

    public static Keyboard getInstance() {
        if (instance == null) {
            instance = new Keyboard();
        }

        return instance;
    }

    public static void keyCallback(long window, int key, int scancode, int action, int mods) {
        if (action == GLFW_PRESS) {
            getInstance().keysDown.put(key, true);
            getInstance().keysPressed.put(key, true);
        } else if (action == GLFW_RELEASE) {
            getInstance().keysDown.put(key, false);
        }
    }

    public static void update() {
        getInstance().keysPressed.clear();
    }

    public static boolean isKeyDown(int key) {
        return getInstance().keysDown.getOrDefault(key, false);
    }

    public static boolean isKeyPressed(int key) {
        return getInstance().keysPressed.getOrDefault(key, false);
    }
}
