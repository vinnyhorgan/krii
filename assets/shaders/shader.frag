#version 330 core

out vec4 FragColor;

in vec2 TexCoord;

uniform sampler2D modelTexture;

void main(void){
    FragColor = texture(modelTexture, TexCoord);
}
