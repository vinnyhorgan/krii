package core;

public class SceneManager {
    private static SceneManager instance = null;

    private Scene currentScene;

    private SceneManager() {

    }

    public static SceneManager getInstance() {
        if (instance == null) {
            instance = new SceneManager();
        }

        return instance;
    }

    public static void setScene(Scene scene) {
        if (getInstance().currentScene != null) {
            getInstance().currentScene.unload();
        }

        getInstance().currentScene = scene;
        getInstance().currentScene.init();
    }

    public static void update(float dt) {
        getInstance().currentScene.update(dt);
    }

    public static void unload() {
        getInstance().currentScene.unload();
    }
}
