#version 330 core

out vec4 FragColor;

in vec2 TexCoord;
in vec3 Normal;
in vec3 ToLight;
in vec3 ToCamera;

uniform sampler2D modelTexture;
uniform vec3 lightColor;
uniform float shineDamper;
uniform float reflectivity;

void main(void){
    vec3 unitNormal = normalize(Normal);
    vec3 unitToLight = normalize(ToLight);

    float diffuse = max(dot(unitNormal, unitToLight), 0.2); // ambient lighting
    vec3 diffuseColor = diffuse * lightColor;

    vec3 unitToCamera = normalize(ToCamera);
    vec3 lightDirection = -unitToLight;
    vec3 reflectDirection = reflect(lightDirection, unitNormal);
    float specular = pow(max(dot(unitToCamera, reflectDirection), 0.0), shineDamper);
    vec3 specularColor = specular * reflectivity * lightColor;

    FragColor = vec4(diffuseColor, 1.0) * texture(modelTexture, TexCoord) + vec4(specularColor, 1.0);
}
