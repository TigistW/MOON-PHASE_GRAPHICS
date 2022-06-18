# version 330

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texture;
layout(location = 2) in vec3 normal;

uniform mat4 moon_model;
uniform mat4 projection_view;
uniform mat4 view_display;

uniform mat4 transform;
uniform mat4 light;

out vec2 v_texture;
out vec3 fragNormal;
void main()
{
        fragNormal = (light * transform * vec4(normal, 0.0f)).xyz;
    gl_Position = projection_view * view_display * moon_model * vec4(position, 1.0);
    v_texture = texture;
}