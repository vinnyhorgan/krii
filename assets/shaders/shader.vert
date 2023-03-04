#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoord;

out vec2 TexCoord;

uniform mat4 transformationMatrix;
uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;

void main(void){
    gl_Position = projectionMatrix * viewMatrix * transformationMatrix * vec4(aPos, 1.0);
    TexCoord = aTexCoord;
}
