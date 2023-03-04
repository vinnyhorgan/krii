package graphics;

import org.joml.Matrix4f;
import org.joml.Vector2f;
import org.joml.Vector3f;
import org.joml.Vector4f;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

import static org.lwjgl.opengl.GL33.*;

public class Shader {
    private int programID;

    public Shader(String vertexPath, String fragmentPath) {
        String vertexSource, fragmentSource;

        try {
            vertexSource = new String(Files.readAllBytes(Paths.get(vertexPath)));
            fragmentSource = new String(Files.readAllBytes(Paths.get(fragmentPath)));

            int vertexShader = glCreateShader(GL_VERTEX_SHADER);
            glShaderSource(vertexShader, vertexSource);
            glCompileShader(vertexShader);

            int success = glGetShaderi(vertexShader, GL_COMPILE_STATUS);
            if (success == GL_FALSE) {
                int length = glGetShaderi(vertexShader, GL_INFO_LOG_LENGTH);
                System.out.println("Error compiling vertex shader: " + glGetShaderInfoLog(vertexShader, length));
                System.exit(1);
            }

            int fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
            glShaderSource(fragmentShader, fragmentSource);
            glCompileShader(fragmentShader);

            success = glGetShaderi(fragmentShader, GL_COMPILE_STATUS);
            if (success == GL_FALSE) {
                int length = glGetShaderi(fragmentShader, GL_INFO_LOG_LENGTH);
                System.out.println("Error compiling fragment shader: " + glGetShaderInfoLog(fragmentShader, length));
                System.exit(1);
            }

            programID = glCreateProgram();
            glAttachShader(programID, vertexShader);
            glAttachShader(programID, fragmentShader);
            glLinkProgram(programID);

            success = glGetProgrami(programID, GL_LINK_STATUS);
            if (success == GL_FALSE) {
                int length = glGetProgrami(programID, GL_INFO_LOG_LENGTH);
                System.out.println("Error linking shader program: " + glGetProgramInfoLog(programID, length));
                System.exit(1);
            }

            glDeleteShader(vertexShader);
            glDeleteShader(fragmentShader);
        } catch (IOException e) {
            e.printStackTrace();
            System.exit(1);
        }
    }

    public void bind() {
        glUseProgram(programID);
    }

    public void unbind() {
        glUseProgram(0);
    }

    public void unload() {
        unbind();
        glDeleteProgram(programID);
    }

    public void setInt(String name, int value) {
        glUniform1i(glGetUniformLocation(programID, name), value);
    }

    public void setFloat(String name, float value) {
        glUniform1f(glGetUniformLocation(programID, name), value);
    }

    public void setBoolean(String name, boolean value) {
        glUniform1i(glGetUniformLocation(programID, name), value ? 1 : 0);
    }

    public void setVector2(String name, Vector2f value) {
        glUniform2f(glGetUniformLocation(programID, name), value.x, value.y);
    }

    public void setVector3(String name, Vector3f value) {
        glUniform3f(glGetUniformLocation(programID, name), value.x, value.y, value.z);
    }

    public void setVector4(String name, Vector4f value) {
        glUniform4f(glGetUniformLocation(programID, name), value.x, value.y, value.z, value.w);
    }

    public void setMatrix4(String name, Matrix4f value) {
        glUniformMatrix4fv(glGetUniformLocation(programID, name), false, value.get(new float[16]));
    }
}
