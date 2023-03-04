package graphics;

import org.joml.Vector3f;

public class Entity {
    private TexturedModel texturedModel;
    private Vector3f position;
    private float rx, ry, rz;
    private float scale;

    public Entity(TexturedModel texturedModel, Vector3f position, float rx, float ry, float rz, float scale) {
        this.texturedModel = texturedModel;
        this.position = position;
        this.rx = rx;
        this.ry = ry;
        this.rz = rz;
        this.scale = scale;
    }

    public void increasePosition(float dx, float dy, float dz) {
        this.position.x += dx;
        this.position.y += dy;
        this.position.z += dz;
    }

    public void increaseRotation(float dx, float dy, float dz) {
        this.rx += dx;
        this.ry += dy;
        this.rz += dz;
    }

    public TexturedModel getTexturedModel() {
        return texturedModel;
    }

    public Vector3f getPosition() {
        return position;
    }

    public float getRx() {
        return rx;
    }

    public float getRy() {
        return ry;
    }

    public float getRz() {
        return rz;
    }

    public float getScale() {
        return scale;
    }
}
