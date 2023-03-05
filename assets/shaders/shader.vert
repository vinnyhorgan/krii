#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoord;
layout (location = 2) in vec3 aNormal;

out vec2 TexCoord;
out vec3 Normal;
out vec3 ToLight;
out vec3 ToCamera;

uniform mat4 transformationMatrix;
uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;
uniform vec3 lightPosition;

void main(void){
    gl_Position = projectionMatrix * viewMatrix * transformationMatrix * vec4(aPos, 1.0);
    TexCoord = aTexCoord;

    Normal = (transformationMatrix * vec4(aNormal, 0.0)).xyz;
    ToLight = lightPosition - (transformationMatrix * vec4(aPos, 1.0)).xyz;
    ToCamera = (inverse(viewMatrix) * vec4(0.0, 0.0, 0.0, 1.0)).xyz - (transformationMatrix * vec4(aPos, 1.0)).xyz;
}
