package scenes;

import core.Scene;
import graphics.*;
import org.joml.Vector3f;

public class Test extends Scene {
    private Loader loader;
    private Shader shader;
    private Renderer renderer;
    private Model model;
    private TexturedModel texturedModel;
    private Entity entity;
    private Camera camera;
    private Light light;

    @Override
    public void init() {
        loader = new Loader();
        shader = new Shader("assets/shaders/shader.vert", "assets/shaders/shader.frag");
        renderer = new Renderer(shader);

        model = OBJLoader.loadObjModel("assets/models/dragon.obj", loader);
        texturedModel = new TexturedModel(model, loader.loadTexture("assets/textures/white.png"));

        Texture texture = texturedModel.getTexture();
        texture.setShineDamper(10);
        texture.setReflectivity(1);

        entity = new Entity(texturedModel, new Vector3f(0, 0, -50), 0, 0, 0, 1);

        camera = new Camera();

        light = new Light(new Vector3f(0, 0, -20), new Vector3f(1, 1, 1));
    }

    @Override
    public void update(float dt) {
        entity.increaseRotation(0, 1, 0);
        camera.move();

        renderer.prepare();
        shader.bind();
        shader.setVector3("lightPosition", light.getPosition());
        shader.setVector3("lightColor", light.getColor());
        shader.setMatrix4("viewMatrix", camera.getViewMatrix());
        renderer.render(entity, shader);
        shader.unbind();
    }

    @Override
    public void unload() {
        shader.unload();
        loader.unload();
    }
}
