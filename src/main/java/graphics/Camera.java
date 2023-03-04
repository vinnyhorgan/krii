package graphics;

import core.Keyboard;
import org.joml.Math;
import org.joml.Matrix4f;
import org.joml.Vector3f;

import static org.lwjgl.glfw.GLFW.*;

public class Camera {
    private Vector3f position = new Vector3f(0, 0, 0);
    private float pitch = 0;
    private float yaw = 0;
    private float roll = 0;
    private float moveSpeed = 0.2f;
    private float lookSpeed = 1f;

    public Camera() {

    }

    public void move() {
        if (Keyboard.isKeyDown(GLFW_KEY_W)) {
            position.z -= moveSpeed;
        } else if (Keyboard.isKeyDown(GLFW_KEY_S)) {
            position.z += moveSpeed;
        }

        if (Keyboard.isKeyDown(GLFW_KEY_A)) {
            position.x -= moveSpeed;
        } else if (Keyboard.isKeyDown(GLFW_KEY_D)) {
            position.x += moveSpeed;
        }

        if (Keyboard.isKeyDown(GLFW_KEY_SPACE)) {
            position.y += moveSpeed;
        } else if (Keyboard.isKeyDown(GLFW_KEY_LEFT_SHIFT)) {
            position.y -= moveSpeed;
        }

        if (Keyboard.isKeyDown(GLFW_KEY_UP)) {
            pitch -= lookSpeed;
        } else if (Keyboard.isKeyDown(GLFW_KEY_DOWN)) {
            pitch += lookSpeed;
        }

        if (Keyboard.isKeyDown(GLFW_KEY_LEFT)) {
            yaw -= lookSpeed;
        } else if (Keyboard.isKeyDown(GLFW_KEY_RIGHT)) {
            yaw += lookSpeed;
        }
    }

    public Matrix4f getViewMatrix() {
        Matrix4f viewMatrix = new Matrix4f();
        viewMatrix.identity();
        viewMatrix.rotate(Math.toRadians(pitch), new Vector3f(1, 0, 0));
        viewMatrix.rotate(Math.toRadians(yaw), new Vector3f(0, 1, 0));
        viewMatrix.rotate(Math.toRadians(roll), new Vector3f(0, 0, 1));
        Vector3f negativeCameraPos = new Vector3f(-position.x, -position.y, -position.z);
        viewMatrix.translate(negativeCameraPos);

        return viewMatrix;
    }

    public Vector3f getPosition() {
        return position;
    }

    public float getPitch() {
        return pitch;
    }

    public float getYaw() {
        return yaw;
    }

    public float getRoll() {
        return roll;
    }
}
