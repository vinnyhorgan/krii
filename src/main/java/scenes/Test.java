package scenes;

import core.Scene;
import graphics.*;
import org.joml.Matrix4f;
import org.joml.Vector3f;

public class Test extends Scene {
    private float[] vertices = {
        -0.5f,0.5f,0,
        -0.5f,-0.5f,0,
        0.5f,-0.5f,0,
        0.5f,0.5f,0,

        -0.5f,0.5f,1,
        -0.5f,-0.5f,1,
        0.5f,-0.5f,1,
        0.5f,0.5f,1,

        0.5f,0.5f,0,
        0.5f,-0.5f,0,
        0.5f,-0.5f,1,
        0.5f,0.5f,1,

        -0.5f,0.5f,0,
        -0.5f,-0.5f,0,
        -0.5f,-0.5f,1,
        -0.5f,0.5f,1,

        -0.5f,0.5f,1,
        -0.5f,0.5f,0,
        0.5f,0.5f,0,
        0.5f,0.5f,1,

        -0.5f,-0.5f,1,
        -0.5f,-0.5f,0,
        0.5f,-0.5f,0,
        0.5f,-0.5f,1
    };

    private float[] textureCoords = {
        0, 0,
        0, 1,
        1, 1,
        1, 0,
        0, 0,
        0, 1,
        1, 1,
        1, 0,
        0, 0,
        0, 1,
        1, 1,
        1, 0,
        0, 0,
        0, 1,
        1, 1,
        1, 0,
        0, 0,
        0, 1,
        1, 1,
        1, 0,
        0, 0,
        0, 1,
        1, 1,
        1, 0
    };

    private int[] indices = {
        0,  1,  3,
        3,  1,  2,
        4,  5,  7,
        7,  5,  6,
        8,  9,  11,
        11, 9,  10,
        12, 13, 15,
        15, 13, 14,
        16, 17, 19,
        19, 17, 18,
        20, 21, 23,
        23, 21, 22
    };

    private Loader loader;
    private Shader shader;
    private Renderer renderer;
    private Model model;
    private TexturedModel texturedModel;
    private Entity entity;
    private Camera camera;

    @Override
    public void init() {
        loader = new Loader();
        shader = new Shader("assets/shaders/shader.vert", "assets/shaders/shader.frag");
        renderer = new Renderer(shader);

        model = loader.loadModel(vertices, textureCoords, indices);
        texturedModel = new TexturedModel(model, loader.loadTexture("assets/textures/container.jpg"));
        entity = new Entity(texturedModel, new Vector3f(0, 0, -5), 0, 0, 0, 1);

        camera = new Camera();
    }

    @Override
    public void update(float dt) {
        entity.increaseRotation(1, 1, 0);
        camera.move();

        renderer.prepare();
        shader.bind();
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
